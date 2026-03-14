import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "wahpedia" / "space_wolves" / "wahapedia_migrator.py"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


spec = importlib.util.spec_from_file_location("wahapedia_migrator", MODULE_PATH)
wahapedia_migrator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wahapedia_migrator)


class FixtureExporter(wahapedia_migrator.WahapediaContentsExporter):
    def __init__(self, pages, **kwargs):
        super().__init__(
            faction_url="https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves",
            output_dir=kwargs.pop("output_dir", "."),
            build_complete_doc=True,
            **kwargs,
        )
        self.fixture_pages = {
            key: BeautifulSoup(value, "lxml") if isinstance(value, str) else value
            for key, value in pages.items()
        }

    def fetch_page(self, url):
        if url not in self.fixture_pages:
            raise RuntimeError(f"Fixture not found for {url}")
        return self.fixture_pages[url]


class WahapediaMigratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faction_html = (FIXTURE_DIR / "space_wolves_faction_fixture.html").read_text(
            encoding="utf-8"
        )
        cls.ragnar_html = (FIXTURE_DIR / "ragnar_blackmane_fixture.html").read_text(
            encoding="utf-8"
        )
        cls.pages = {
            "https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves": cls.faction_html,
            "https://wahapedia.ru/wh40k10ed/factions/space-marines/Ragnar-Blackmane": cls.ragnar_html,
        }

    def test_parse_contents_uses_visible_contents_not_army_list(self):
        exporter = FixtureExporter(self.pages)
        exporter.faction_soup = BeautifulSoup(self.faction_html, "lxml")
        entries = exporter.parse_contents_index()

        labels = [entry.label for entry in entries]
        self.assertIn("Books", labels)
        self.assertIn("Introduction", labels)
        self.assertIn("Ragnar Blackmane", labels)
        self.assertNotIn("Ancient", labels)

        gladius = next(entry for entry in entries if entry.label == "Gladius Task Force")
        ragnar = next(entry for entry in entries if entry.label == "Ragnar Blackmane")
        self.assertEqual(gladius.type, "local_anchor")
        self.assertEqual(gladius.depth, 10)
        self.assertEqual(ragnar.type, "external_page")

    def test_assign_output_files_uses_reserved_names_and_deterministic_collision_suffixes(self):
        entry_a = wahapedia_migrator.ContentEntry(
            label="Stratagems",
            type="local_anchor",
            depth=30,
            href="#Stratagems",
            source_url="https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves#Stratagems",
            anchor_id="Stratagems",
            group_codes=[],
        )
        entry_b = wahapedia_migrator.ContentEntry(
            label="Stratagems",
            type="local_anchor",
            depth=30,
            href="#Stratagems-2",
            source_url="https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves#Stratagems-2",
            anchor_id="Stratagems-2",
            group_codes=[],
        )

        exporter = FixtureExporter(self.pages)
        exporter.entries = [entry_a, entry_b]
        exporter.assign_output_files()

        self.assertEqual(entry_a.output_file, "stratagems.md")
        self.assertEqual(entry_b.output_file, "stratagems_2.md")

        exporter = FixtureExporter(self.pages)
        exporter.faction_soup = BeautifulSoup(self.faction_html, "lxml")
        exporter.entries = exporter.parse_contents_index()
        exporter.assign_output_files()

        mapping = {entry.label: entry.output_file for entry in exporter.entries if entry.output_file}
        self.assertEqual(mapping["Introduction"], "introduction.md")
        self.assertEqual(mapping["Army Rules"], "army_rules.md")
        self.assertEqual(mapping["Gladius Task Force"], "detachment_gladius_task_force.md")
        self.assertEqual(mapping["Ragnar Blackmane"], "ragnar_blackmane.md")

    def test_render_outputs_writes_manifest_report_complete_doc_and_skips_failed_placeholders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = FixtureExporter(self.pages, output_dir=tmpdir)
            exporter.fetch_faction_page()
            exporter.entries = exporter.parse_contents_index()
            exporter.assign_output_files()
            exporter.extract_entries()
            exporter.rewrite_cross_links()
            exporter.render_outputs()

            output_path = Path(tmpdir)
            introduction = (output_path / "introduction.md").read_text(encoding="utf-8")
            detachments = (output_path / "detachments.md").read_text(encoding="utf-8")
            manifest = json.loads((output_path / "manifest.json").read_text(encoding="utf-8"))
            complete_doc = (output_path / "space_wolves_complete.md").read_text(encoding="utf-8")

            self.assertIn("Ragnar Blackmane", introduction)
            self.assertIn("(ragnar_blackmane.md)", introduction)
            self.assertIn("Gladius Task Force", detachments)
            self.assertIn("[Back to Contents](#table-of-contents)", complete_doc)
            self.assertIn("## Table of Contents", complete_doc)

            statuses = {item["label"]: item["status"] for item in manifest}
            self.assertEqual(statuses["Missing Page"], "failed")
            self.assertEqual(statuses["Introduction"], "written")
            self.assertFalse((output_path / "missing_page.md").exists())

            report = (output_path / "report.md").read_text(encoding="utf-8")
            self.assertIn("Failed Entries", report)
            self.assertIn("Missing Page", report)


if __name__ == "__main__":
    unittest.main()

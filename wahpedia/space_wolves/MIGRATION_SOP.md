# Wahapedia Faction Migration SOP

This document outlines the standard procedures for migrating Warhammer 40,000 faction data from Wahapedia to Markdown for use in this repository.

---

## Strategy 1: Hub & Spoke (Modular Files)
**Best for:** Active gameplay reference, quick searching, and modular editing.

### **The Workflow**
1.  **Research & Inventory:** Fetch the Faction page and `/datasheets.html`. Compare against existing files to identify missing or outdated content.
2.  **Core Rules:** Create individual files for `introduction.md`, `faq.md`, `crusade_rules.md`, and `boarding_actions.md`.
3.  **Army Rules:** Update/Create `army_rules.md` to include Faction-wide mechanics (e.g., *Strands of Fate*, *Synapse*, etc.).
4.  **Detachments:** Create individual `detachment_[name].md` files. Turn `detachments.md` into a Table of Contents index linking to these files.
5.  **Datacards:** Group unit variants (e.g., weapon platforms, specialized gear) into a single file per datasheet. Use `snake_case.md`.

---

## Strategy 2: Unified (Single Document)
**Best for:** Offline reading, printing/PDF generation, and holistic faction study.

### **The Recommended Order**
1.  **H1: [Faction Name]**
2.  **Table of Contents:** Linked list of internal anchors to all H2 and H3 sections.
3.  **Introduction:** Lore and overview.
4.  **Army Rules:** Core mechanics.
5.  **Detachments:** Grouped rules, stratagems, and enhancements.
6.  **Datacards:** Alphabetical list of units with full stats and weapons.
7.  **Crusade Rules:** Narrative play content.
8.  **Boarding Actions:** Specialized rules.
9.  **FAQ:** Clarifications and errata.

---

## Strategy 3: Consolidation (Modular to Unified)
**Best for:** Converting existing modular "Strategy 1" files into a single "Strategy 2" document.

### **The Workflow**
1.  **Identify Sources:** Gather all `.md` files in the current faction directory.
2.  **Generate TOC:** Create a clickable Table of Contents that maps to internal anchors.
3.  **Re-map Links:** Convert all cross-file links (e.g., `[Unit](unit_name.md)`) into internal document anchors (e.g., `[Unit](#unit-name)`).
4.  **Sequential Append:** Merge the files in the logical order defined in Strategy 2.

### **Repeatable Consolidation Command**
> **Directive: Consolidate [Faction Name] to Unified Document**
> 
> "Take all modular Markdown files in this directory and consolidate them into a single `[faction_name]_complete.md` file following **Strategy 3** of the `MIGRATION_SOP.md`. 
> 1. Use the **Sequential Order** from Strategy 2.
> 2. Convert all existing cross-file links into internal anchor links.
> 3. Add '[Back to Contents](#table-of-contents)' links after every major H2 section.
> 4. Ensure the Table of Contents is fully clickable and links to every datasheet and rule."

---

## Technical Standards
- **Naming:** Always use `snake_case` for filenames and internal anchors.
- **Formatting:** Bold all keywords (e.g., **INFANTRY**, **[BLAST]**).
- **Parity:** Always ensure 1:1 parity with the 10th Edition Wahapedia source.
- **Batched Processing:** Use parallel `web_fetch` and `write_file` batches to maximize speed.

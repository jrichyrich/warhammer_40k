import os
import re
import json
import argparse

def clean_val(text):
    if not text: return ""
    text = re.sub(r'(?i)^Datasheet:\s*', '', text)
    return re.sub(r'[#*_]+', '', text).strip()

def parse_md_table(content):
    rows = []
    for line in content.split('\n'):
        if '|' in line:
            if re.match(r'^[|\s:;-]+$', line.strip()): continue
            cols = [c.strip() for c in line.strip('|').split('|')]
            if cols: rows.append(cols)
    return rows

def extract_section(content, keywords):
    lines = content.split('\n')
    start_idx = -1
    for i, line in enumerate(lines):
        if any(k.lower() in line.lower() for k in keywords) and re.match(r'^(?:#|\*\*|###)', line.strip()):
            start_idx = i + 1
            break
    if start_idx == -1: return ""
    result = []
    for i in range(start_idx, len(lines)):
        line = lines[i]
        if re.match(r'^#+ ', line.strip()): break
        if line.strip() == '---': break
        if re.match(r'(?i)^\s*\*\*?(?:KEYWORDS|FACTION)', line.strip()): break
        result.append(line)
    return '\n'.join(result).strip()

def process_json_unit(data, filename):
    unit_id = filename.replace('.json', '').lower().replace('-', '_')
    chars = data.get("characteristics", {})
    stats = {"M": chars.get("M", "-"), "T": chars.get("T", "-"), "Sv": chars.get("Sv", "-"), "W": chars.get("W", "-"), "Ld": chars.get("Ld", "-"), "OC": chars.get("OC", "-")}
    
    weapons = {"ranged": [], "melee": []}
    w_data = data.get("weapons", {})
    for rw in w_data.get("ranged_weapons", []):
        weapons["ranged"].append({"name": rw.get("name"), "rng": rw.get("range"), "a": rw.get("a"), "skill": rw.get("bs"), "s": rw.get("s"), "ap": rw.get("ap"), "d": rw.get("d"), "tags": rw.get("abilities", [])})
    for mw in w_data.get("melee_weapons", []):
        weapons["melee"].append({"name": mw.get("name"), "rng": mw.get("range"), "a": mw.get("a"), "skill": mw.get("ws"), "s": mw.get("s"), "ap": mw.get("ap"), "d": mw.get("d"), "tags": mw.get("abilities", [])})

    abs_data = data.get("abilities", {})
    core_abs = ", ".join(abs_data.get("core", []))
    fact_abs = ", ".join(abs_data.get("faction", []))
    ds_abs = [f"**{a.get('name', '')}**: {a.get('text', '')}" for a in abs_data.get("datasheet", [])]
    
    damaged = None
    for section in data.get("sections", []):
        if "DAMAGED:" in section.get("title", "").upper():
            title = section["title"].replace("DAMAGED:", "").strip()
            text = "".join([e.get("text", "") for e in section.get("entries", []) if e.get("type") == "text"])
            damaged = f"{title}: {text}"

    comp_list = []
    points_str = "-"
    for entry in data.get("unit_composition", []):
        if entry.get("type") == "list": comp_list.extend(entry.get("items", []))
        if entry.get("type") == "statement": comp_list.append(f"**{entry.get('label')}**: {entry.get('text')}")
        if entry.get("type") == "points":
            points_str = ", ".join([f"{r['label']}: {r['points']}" for r in entry.get("rows", [])])

    return {
        "id": unit_id, "name": data.get("name"), "stats": stats, "invuln": chars.get("Invulnerable Save", "-"),
        "points": points_str, "weapons": weapons, "keywords": ", ".join(data.get("keywords", [])),
        "faction": ", ".join(data.get("faction_keywords", [])), "core_abilities": core_abs,
        "faction_abilities": fact_abs, "abilities_raw": "\n".join(ds_abs),
        "composition_raw": "\n".join([f"* {item}" for item in comp_list]), "damaged_state": damaged
    }

def process_md_unit(content, filename, patches):
    unit_id = filename.replace('.md', '')
    
    if unit_id in patches.get("full_overrides", {}):
        override = patches["full_overrides"][unit_id]
        return {
            "id": unit_id, "file": filename, "name": override.get("name", unit_id.replace('_', ' ').title()),
            "stats": override.get("stats", {"M": "-", "T": "-", "Sv": "-", "W": "-", "Ld": "-", "OC": "-"}),
            "invuln": override.get("invuln", "-"), "points": override.get("points", "-"),
            "weapons": {"ranged": override.get("ranged", []), "melee": override.get("melee", [])},
            "keywords": override.get("keywords", ""), "faction": override.get("faction", ""),
            "abilities_raw": override.get("abilities_raw", ""), "core_abilities": override.get("core_abilities", ""),
            "faction_abilities": override.get("faction_abilities", ""), "composition_raw": override.get("composition_raw", ""),
            "damaged_state": override.get("damaged_state", None)
        }

    name_search = re.search(r'^(?:#+)\s*(.*?)$', content, re.M)
    name = clean_val(name_search.group(1)) if name_search else unit_id.replace('_', ' ').title()
    unit = {"id": unit_id, "file": filename, "name": name, "stats": {}, "invuln": "-", "points": "-",
            "weapons": {"ranged": [], "melee": []}, "keywords": "", "faction": "",
            "abilities_raw": "", "composition_raw": "", "damaged_state": None,
            "core_abilities": "", "faction_abilities": ""}

    s_map = {"m": "M", "t": "T", "sv": "Sv", "w": "W", "ld": "Ld", "oc": "OC"}
    
    # Improved Markdown Stats Parser (Table-aware)
    all_rows = parse_md_table(content)
    for i, row in enumerate(all_rows):
        row_l = [clean_val(c).lower().replace(' ', '') for c in row]
        if 'm' in row_l and 't' in row_l and ('sv' in row_l or 'stat' in row_l):
            data_row = None
            for j in range(i + 1, len(all_rows)):
                if any(re.search(r'\d', str(cell)) for cell in all_rows[j]):
                    data_row = all_rows[j]
                    break
            if data_row:
                for k, h in enumerate(row_l):
                    if h in s_map and k < len(data_row): unit['stats'][s_map[h]] = data_row[k]
                    if ('inv' in h or 'save' in h) and h != 'sv' and k < len(data_row): unit['invuln'] = data_row[k]
            break

    # Fallback to List format
    if len(unit['stats']) < 3:
        header_raw = '\n'.join(content.split('\n')[:15])
        clean_header = header_raw.replace('*', '').replace('#', '').replace('_', '')
        for key_raw, key_pretty in s_map.items():
            m = re.search(r'\b' + key_raw + r'\b\s*[:\s]\s*([^|*\n\s]+)', clean_header, re.I)
            if m: unit['stats'][key_pretty] = m.group(1).strip().strip('"').strip('|')

    if len(unit['stats']) < 3: return None

    # Weapons
    for mode in ['ranged', 'melee']:
        sect = extract_section(content, [f'{mode} weapons'])
        if sect:
            for r in parse_md_table(sect):
                if len(r) >= 7 and any(re.search(r'\d', str(cell)) for cell in r[1:7]):
                    unit["weapons"][mode].append({"name": clean_val(r[0]), "rng": r[1], "a": r[2], "skill": r[3], "s": r[4], "ap": r[5], "d": r[6], "tags": [t.strip() for t in r[7].split(',')] if len(r) > 7 and r[7] != '-' else []})

    unit['abilities_raw'] = extract_section(content, ['abilities'])
    unit['composition_raw'] = extract_section(content, ['unit composition', 'composition'])
    if unit_id in patches.get("points", {}): unit['points'] = patches["points"][unit_id]
    kw = re.search(r'(?i)Keywords:\s*(.*)', content)
    if kw: unit['keywords'] = clean_val(kw.group(1))
    fk = re.search(r'(?i)Faction Keywords:\s*(.*)', content)
    if fk: unit['faction'] = clean_val(fk.group(1))
    return unit

def main(faction_dir, high_fidelity_json_dir=None):
    faction_name = os.path.basename(faction_dir.strip('/'))
    patch_file = os.path.join(faction_dir, 'roster_patches.json')
    patches = {}
    if os.path.exists(patch_file):
        with open(patch_file, 'r') as f: patches = json.load(f)

    db = {"faction": faction_name, "units": []}
    processed_unit_ids = set()

    # 1. High Fidelity JSON
    if high_fidelity_json_dir and os.path.exists(high_fidelity_json_dir):
        for f in sorted(os.listdir(high_fidelity_json_dir)):
            if f.endswith('.json') and f != 'index.json':
                with open(os.path.join(high_fidelity_json_dir, f), 'r') as file:
                    unit = process_json_unit(json.load(file), f)
                    if unit:
                        db["units"].append(unit)
                        processed_unit_ids.add(unit["id"])

    # 2. Markdown Files
    excludes = ['army_rules.md', 'datasheets.md', 'detachments.md', 'faq.md', 'crusade_rules.md', 'boarding_actions.md', 'introduction.md']
    for f in sorted(os.listdir(faction_dir)):
        if f.endswith('.md') and f not in excludes and 'detachment_' not in f:
            unit_id = f.replace('.md', '')
            # Normalization check
            if unit_id not in processed_unit_ids:
                with open(os.path.join(faction_dir, f), 'r') as md_file:
                    unit = process_md_unit(md_file.read(), f, patches)
                    if unit: db["units"].append(unit)

    output_path = os.path.join(faction_dir, f"{faction_name}_database.json")
    with open(output_path, 'w') as f: json.dump(db, f, indent=2)
    print(f"Success! {len(db['units'])} units saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("--json", default=None)
    args = parser.parse_args()
    main(args.dir, args.json)

import os
import re
import json
import argparse

def clean_val(text):
    if not text: return ""
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

def parse_unit(content, filename, patches):
    name_search = re.search(r'^(?:#+)\s*(.*?)$', content, re.M)
    name = clean_val(name_search.group(1)) if name_search else filename.replace('.md', '').replace('_', ' ').title()

    unit = {
        "id": filename.replace('.md', ''),
        "file": filename,
        "name": name,
        "stats": {},
        "invuln": "-",
        "points": "-",
        "weapons": {"ranged": [], "melee": []},
        "keywords": "",
        "faction": "",
        "abilities_raw": "",
        "composition_raw": ""
    }

    # Stats
    s_map = {"m": "M", "t": "T", "sv": "Sv", "w": "W", "ld": "Ld", "oc": "OC"}
    header_raw = '\n'.join(content.split('\n')[:15])
    clean_header = header_raw.replace('*', '').replace('#', '').replace('_', '')
    
    for key_raw, key_pretty in s_map.items():
        m = re.search(r'\b' + key_raw + r'\b\s*[:\s]\s*([^|*\n\s]+)', clean_header, re.I)
        if m: unit['stats'][key_pretty] = m.group(1).strip().strip('"').strip('|')

    # Table Fallback
    if len(unit['stats']) < 4:
        all_rows = parse_md_table(content)
        for i, row in enumerate(all_rows):
            row_l = [clean_val(c).lower() for c in row]
            if 'm' in row_l and ('sv' in row_l or 'stat' in row_l):
                data_row = None
                for j in range(i + 1, len(all_rows)):
                    if any(re.search(r'\d', str(cell)) for cell in all_rows[j]):
                        data_row = all_rows[j]
                        break
                if data_row:
                    for k, h in enumerate(row_l):
                        cl_h = clean_val(h).lower()
                        if cl_h in s_map and k < len(data_row): unit['stats'][s_map[cl_h]] = data_row[k]
                        if ('inv' in cl_h or 'save' in cl_h) and cl_h != 'sv' and k < len(data_row): unit['invuln'] = data_row[k]
                break

    if len(unit['stats']) < 3: return None

    # Invuln Fallback
    if unit['invuln'] == "-":
        inv = re.search(r'(?i)Invulnerable Save:?\s*\*?\s*(\d+\+.*)', content)
        if inv: unit['invuln'] = inv.group(1).split('\n')[0].strip()

    # Weapons
    for mode in ['ranged', 'melee']:
        sect = extract_section(content, [f'{mode} weapons'])
        if sect:
            for r in parse_md_table(sect):
                if len(r) >= 7 and any(re.search(r'\d', str(cell)) for cell in r[1:7]):
                    unit["weapons"][mode].append({
                        "name": clean_val(r[0]), "rng": r[1], "a": r[2], "skill": r[3],
                        "s": r[4], "ap": r[5], "d": r[6],
                        "tags": [t.strip() for t in r[7].split(',')] if len(r) > 7 and r[7] != '-' else []
                    })

    unit['abilities_raw'] = extract_section(content, ['abilities'])
    unit['composition_raw'] = extract_section(content, ['unit composition', 'composition'])

    # Points
    pts_pattern = re.compile(r'(\d+)\s*(?:pts|points)', re.I)
    pts_list = pts_pattern.findall(content)
    if pts_list: unit['points'] = pts_list[-1]

    # Keywords
    kw = re.search(r'(?i)Keywords:\s*(.*)', content)
    if kw: unit['keywords'] = clean_val(kw.group(1))
    fk = re.search(r'(?i)Faction Keywords:\s*(.*)', content)
    if fk: unit['faction'] = clean_val(fk.group(1))

    # Apply Patches
    base_id = unit['id']
    if base_id in patches.get("points", {}): unit['points'] = patches["points"][base_id]
    if base_id in patches.get("stats", {}): unit['stats'].update(patches["stats"][base_id])
    if base_id in patches.get("abilities", {}): unit['abilities_raw'] = patches["abilities"][base_id]
    if base_id in patches.get("composition", {}): unit['composition_raw'] = patches["composition"][base_id]

    return unit

def main(faction_dir):
    faction_name = os.path.basename(faction_dir.strip('/'))
    print(f"Processing Faction: {faction_name}")
    
    # Load Patches
    patch_file = os.path.join(faction_dir, 'roster_patches.json')
    patches = {"points": {}, "stats": {}, "abilities": {}, "composition": {}}
    if os.path.exists(patch_file):
        with open(patch_file, 'r') as f:
            patches = json.load(f)

    db = {"faction": faction_name, "units": []}
    
    excludes = ['army_rules.md', 'datasheets.md', 'detachments.md', 'faq.md', 'crusade_rules.md', 'boarding_actions.md', 'introduction.md']
    
    for f in sorted(os.listdir(faction_dir)):
        if f.endswith('.md') and f not in excludes and 'detachment_' not in f:
            with open(os.path.join(faction_dir, f), 'r') as md_file:
                unit = parse_unit(md_file.read(), f, patches)
                if unit: db["units"].append(unit)

    output_path = os.path.join(faction_dir, f"{faction_name}_database.json")
    with open(output_path, 'w') as f:
        json.dump(db, f, indent=2)
    
    print(f"Success! {len(db['units'])} units saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Directory containing faction markdown files")
    args = parser.parse_args()
    main(args.dir)

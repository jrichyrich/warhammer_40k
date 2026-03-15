import os
import re
import json

DIR = '/Users/jasricha/Documents/Github_Personal/warhammer_40k/wahpedia/aeldari'
output_file = os.path.join(DIR, 'aeldari_datacards_print.html')

# Load Patches
patch_file = os.path.join(DIR, 'roster_patches.json')
patches = {"points": {}, "stats": {}, "abilities": {}, "composition": {}}
if os.path.exists(patch_file):
    with open(patch_file, 'r') as f:
        patches = json.load(f)

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

def parse_unit(content, filename):
    excludes = ['army_rules.md', 'datasheets.md', 'detachments.md', 'faq.md', 'crusade_rules.md', 'boarding_actions.md', 'introduction.md', 'aeldari_full_roster.html', 'aeldari_datacards_print.html', 'map_files.py', 'audit_mapping.json', 'roster_patches.json', 'find_missing.py', 'test_regex.py', 'test_parse.py']
    if filename in excludes or 'detachment_' in filename.lower() or '_styled' in filename: return None
    
    name_search = re.search(r'^(?:#+)\s*(.*?)$', content, re.M)
    name = clean_val(name_search.group(1)) if name_search else filename.replace('.md', '').replace('_', ' ').title()

    unit = {
        "file": filename, "name": name, "stats": {}, "invuln": "-", "points": "-",
        "ranged": [], "melee": [], "keywords": "", "faction": "Asuryani",
        "abilities_raw": "", "composition_raw": ""
    }

    # --- FORMATTING-BLIND STATS PARSING ---
    s_map = {"m": "M", "t": "T", "sv": "Sv", "w": "W", "ld": "Ld", "oc": "OC"}
    
    # 1. Clean the header lines
    header_raw = '\n'.join(content.split('\n')[:15])
    clean_header = header_raw.replace('*', '').replace('#', '').replace('_', '')
    
    # 2. Extract stats using simple pattern
    for key_raw, key_pretty in s_map.items():
        # Match "M: 7" or "M 7" (case-insensitive boundary)
        m = re.search(r'\b' + key_raw + r'\b\s*[:\s]\s*([^|*\n\s]+)', clean_header, re.I)
        if m:
            unit['stats'][key_pretty] = m.group(1).strip().strip('"').strip('|')

    # 3. Table Fallback if Regex failed or got incomplete data
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

    if len(unit['stats']) < 3:
        # print(f"Skipping {filename} - Found: {unit['stats']}")
        return None

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
                    unit[mode].append({
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
    base_name = filename.replace('.md', '')
    if base_name in patches.get("points", {}): unit['points'] = patches["points"][base_name]
    if base_name in patches.get("stats", {}): unit['stats'].update(patches["stats"][base_name])
    if base_name in patches.get("abilities", {}): unit['abilities_raw'] = patches["abilities"][base_name]
    if base_name in patches.get("composition", {}): unit['composition_raw'] = patches["composition"][base_name]

    return unit

datasheets = []
for f in sorted(os.listdir(DIR)):
    if f.endswith('.md'):
        with open(os.path.join(DIR, f), 'r') as file:
            p = parse_unit(file.read(), f)
            if p: datasheets.append(p)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aeldari Roster - Verified Data Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@700;900&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --ink-black: #1a1a1a; --ink-grey: #f4f4f4; --link-color: #2b5757; }
        * { box-sizing: border-box; scroll-behavior: smooth; }
        body { font-family: 'Roboto Condensed', sans-serif; background: #bbb; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 30px; }
        .toc-container { width: 1000px; background: white; border: 1.5px solid var(--ink-black); padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .toc-title { font-family: 'Exo 2', sans-serif; font-size: 28px; text-transform: uppercase; font-weight: 900; margin-top: 0; border-bottom: 2px solid var(--ink-black); padding-bottom: 10px; margin-bottom: 20px; }
        .toc-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .toc-link { color: var(--link-color); text-decoration: none; font-weight: 700; font-size: 13.5px; padding: 3px 6px; border-radius: 4px; }
        .toc-link:hover { background: var(--ink-grey); text-decoration: underline; }
        .back-to-top { position: fixed; bottom: 20px; right: 20px; background: var(--ink-black); color: white; padding: 10px 15px; text-decoration: none; font-weight: bold; border-radius: 5px; opacity: 0.8; z-index: 1000; }
        .datasheet { width: 1000px; background: white; border: 1.5px solid var(--ink-black); position: relative; page-break-inside: avoid; box-shadow: 0 5px 15px rgba(0,0,0,0.2); scroll-margin-top: 20px; }
        .header { border-bottom: 2.5px solid var(--ink-black); padding: 10px 25px; height: 60px; display: flex; align-items: center; }
        .header h1 { margin: 0; font-family: 'Exo 2', sans-serif; font-size: 30px; text-transform: uppercase; font-weight: 900; }
        .stats-bar { display: flex; padding: 12px 25px; gap: 10px; }
        .stat-box { border: 1.5px solid var(--ink-black); clip-path: polygon(8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px), 0 8px); width: 70px; text-align: center; padding: 5px 0; }
        .stat-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #444; }
        .stat-val { font-family: 'Exo 2', sans-serif; font-size: 22px; font-weight: 900; }
        .invuln-badge { margin-left: 25px; margin-bottom: 10px; border: 1.5px solid var(--ink-black); display: inline-flex; align-items: center; padding: 4px 12px; font-weight: 800; font-size: 12px; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%); }
        .invuln-val { font-size: 18px; font-weight: 900; margin-right: 8px; border-right: 1px solid #ccc; padding-right: 8px; }
        .grid { display: grid; grid-template-columns: 1.6fr 1.4fr; border-top: 1.5px solid var(--ink-black); }
        .left-col { border-right: 1.5px solid var(--ink-black); }
        .section-header { background: var(--ink-grey); padding: 5px 20px; text-transform: uppercase; font-weight: 800; font-size: 15px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--ink-black); }
        .weapon-labels { display: flex; gap: 20px; font-size: 9px; font-weight: 700; opacity: 0.7; }
        .weapon-labels span { width: 35px; text-align: center; }
        .weapon-row { padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 0.5px solid #ddd; }
        .weapon-info b { font-size: 16px; display: block; }
        .tag { border: 1px solid #999; padding: 1px 4px; font-size: 9px; font-weight: 700; text-transform: uppercase; margin-right: 3px; display: inline-block; margin-top: 2px; }
        .weapon-stats { display: flex; gap: 20px; font-family: 'Exo 2', sans-serif; font-size: 18px; font-weight: 900; text-align: center; }
        .weapon-stats span { width: 35px; }
        .md-content { padding: 15px 20px; font-size: 13.5px; line-height: 1.4; }
        .md-content p, .md-content ul { margin: 0 0 10px 0; }
        .md-content ul { padding-left: 20px; }
        .comp-box { padding: 15px 20px; position: relative; min-height: 100px; font-size: 13.5px; }
        .points { position: absolute; bottom: 15px; right: 15px; border: 2.5px solid var(--ink-black); padding: 6px 15px; font-weight: 900; font-size: 24px; clip-path: polygon(10% 0, 100% 0, 90% 100%, 0 100%); }
        .footer { padding: 8px 25px; display: grid; grid-template-columns: 1fr 1fr; font-size: 11px; border-top: 1.5px solid var(--ink-black); background: #f9f9f9; }
        .footer b { text-transform: uppercase; font-weight: 800; }
        @media print { body { background: white; padding: 0; gap: 15px; } .datasheet { width: 100%; box-shadow: none; border-width: 1px; } .toc-container, .back-to-top { display: none; } }
    </style>
</head>
<body id="top">
<div class="toc-container">
    <h2 class="toc-title">Aeldari Army Roster</h2>
    <div class="toc-grid" id="toc-grid"></div>
</div>
<div id="roster"></div>
<a href="#top" class="back-to-top">↑ Top</a>
<script>
    const units = """ + json.dumps(datasheets) + """;
    units.forEach(u => { u.domId = 'unit-' + u.name.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase(); });
    document.getElementById('toc-grid').innerHTML = units.map(u => `<a href="#${u.domId}" class="toc-link">${u.name}</a>`).join('');
    document.getElementById('roster').innerHTML = units.map(u => `
        <div class="datasheet" id="${u.domId}">
            <div class="header"><h1>${u.name}</h1></div>
            <div class="stats-bar">
                ${['M','T','Sv','W','Ld','OC'].map(s => `<div class="stat-box"><div class="stat-label">${s}</div><div class="stat-val">${u.stats[s] || '-'}</div></div>`).join('')}
            </div>
            ${u.invuln !== '-' ? `<div class="invuln-badge"><span class="invuln-val">${u.invuln}</span> INVULNERABLE SAVE</div>` : '<div style="height:12px"></div>'}
            <div class="grid">
                <div class="left-col">
                    ${u.ranged.length ? `<div class="section-header"><span>Ranged Weapons</span><div class="weapon-labels"><span>RNG</span><span>A</span><span>BS</span><span>S</span><span>AP</span><span>D</span></div></div>${u.ranged.map(w => renderWeapon(w)).join('')}` : ''}
                    ${u.melee.length ? `<div class="section-header"><span>Melee Weapons</span><div class="weapon-labels"><span>RNG</span><span>A</span><span>WS</span><span>S</span><span>AP</span><span>D</span></div></div>${u.melee.map(w => renderWeapon(w)).join('')}` : ''}
                </div>
                <div class="right-col">
                    <div class="section-header">Abilities</div>
                    <div class="md-content">${marked.parse(u.abilities_raw)}</div>
                    <div class="section-header">Unit Composition</div>
                    <div class="comp-box">
                        <div class="md-content" style="padding:0">${marked.parse(u.composition_raw)}</div>
                        <div class="points">${u.points}</div>
                    </div>
                </div>
            </div>
            <div class="footer"><div><b>Keywords:</b> ${u.keywords}</div><div style="border-left:1px solid #ddd;padding-left:15px"><b>Faction:</b> ${u.faction}</div></div>
        </div>
    `).join('');
    function renderWeapon(w) {
        return `<div class="weapon-row"><div class="weapon-info"><b>${w.name}</b><div>${w.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div></div><div class="weapon-stats"><span>${w.rng}</span><span>${w.a}</span><span>${w.skill}</span><span>${w.s}</span><span>${w.ap}</span><span>${w.d}</span></div></div>`;
    }
</script>
</body>
</html>
"""
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Success: Final Compilation Complete. Total Units: {len(datasheets)}")

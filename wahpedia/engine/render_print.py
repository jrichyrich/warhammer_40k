import os
import json
import argparse

def main(db_path):
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    faction = data['faction']
    units = data['units']
    output_path = db_path.replace('_database.json', '_datacards_print.html')

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{FACTION}} Roster - Print Edition</title>
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
        @media print { body { background: white; padding: 0; gap: 15px; } .datasheet { width: 100%; box-shadow: none; } .toc-container, .back-to-top { display: none; } }
    </style>
</head>
<body id="top">
<div class="toc-container">
    <h2 class="toc-title">{{FACTION}} Army Roster</h2>
    <div class="toc-grid" id="toc-grid"></div>
</div>
<div id="roster"></div>
<a href="#top" class="back-to-top">↑ Top</a>
<script>
    const units = {{UNITS_JSON}};
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
                    ${u.weapons.ranged.length ? `<div class="section-header"><span>Ranged Weapons</span><div class="weapon-labels"><span>RNG</span><span>A</span><span>BS</span><span>S</span><span>AP</span><span>D</span></div></div>${u.weapons.ranged.map(w => renderWeapon(w)).join('')}` : ''}
                    ${u.weapons.melee.length ? `<div class="section-header"><span>Melee Weapons</span><div class="weapon-labels"><span>RNG</span><span>A</span><span>WS</span><span>S</span><span>AP</span><span>D</span></div></div>${u.weapons.melee.map(w => renderWeapon(w)).join('')}` : ''}
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
    final_html = html_template.replace("{{FACTION}}", faction).replace("{{UNITS_JSON}}", json.dumps(units))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Success: Rendered {len(units)} units to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db", help="Path to the database.json file")
    args = parser.parse_args()
    main(args.db)

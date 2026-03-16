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
    <title>{{FACTION}} Roster - High Fidelity Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@700;900&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --ink-black: #000000; --ink-grey: #eeeeee; --white: #ffffff; }
        * { box-sizing: border-box; -webkit-print-color-adjust: exact; }
        body { font-family: 'Roboto Condensed', sans-serif; background: #999; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 40px; }
        
        /* --- DATACARD CONTAINER --- */
        .datasheet { width: 1050px; background: white; border: 2px solid var(--ink-black); position: relative; page-break-inside: avoid; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        
        /* --- HEADER --- */
        .ds-header { border-bottom: 3px solid var(--ink-black); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .ds-header h1 { margin: 0; font-family: 'Exo 2'; font-size: 38px; font-weight: 900; text-transform: uppercase; letter-spacing: -1px; }

        /* --- STATS BAR (Official Style) --- */
        .stats-bar { display: flex; padding: 15px 30px; gap: 15px; align-items: flex-start; }
        .stat-box { display: flex; flex-direction: column; align-items: center; min-width: 75px; }
        .stat-label { font-size: 12px; font-weight: 900; text-transform: uppercase; border-bottom: 1.5px solid #000; width: 100%; text-align: center; margin-bottom: 5px; padding-bottom: 2px; }
        .stat-val { font-family: 'Exo 2'; font-size: 28px; font-weight: 900; }

        /* --- INVULN SHIELD --- */
        .invuln-container { display: flex; align-items: center; margin-left: 30px; margin-bottom: 15px; gap: 10px; }
        .shield-icon { 
            background: #fdfdfd; border: 2px solid black; width: 50px; height: 50px; 
            clip-path: polygon(0 0, 100% 0, 100% 70%, 50% 100%, 0 70%);
            display: flex; align-items: center; justify-content: center;
            font-family: 'Exo 2'; font-size: 22px; font-weight: 900;
        }
        .invuln-label { font-weight: 900; font-size: 14px; text-transform: uppercase; }

        /* --- MAIN GRID --- */
        .main-grid { display: grid; grid-template-columns: 1.6fr 1.4fr; border-top: 3px solid var(--ink-black); }
        .left-col { border-right: 3px solid var(--ink-black); }
        
        .section-header { background: var(--ink-grey); padding: 8px 25px; text-transform: uppercase; font-weight: 900; font-size: 18px; border-bottom: 2px solid var(--ink-black); display: flex; justify-content: space-between; }
        .weapon-row { padding: 12px 25px; border-bottom: 1px solid #ccc; display: flex; justify-content: space-between; align-items: center; }
        .weapon-name { font-size: 18px; font-weight: 900; text-transform: uppercase; }
        .weapon-tags { font-size: 10px; font-weight: 700; border: 1px solid #666; padding: 1px 4px; display: inline-block; margin-top: 4px; }
        .weapon-stats { display: flex; gap: 20px; font-family: 'Exo 2'; font-size: 22px; font-weight: 900; min-width: 320px; justify-content: space-between; }
        .weapon-stats span { width: 40px; text-align: center; }
        .stat-labels-tiny { display: flex; gap: 20px; font-size: 10px; font-weight: 900; opacity: 0.6; min-width: 320px; justify-content: space-between; margin-bottom: -5px; padding-right: 25px; padding-top: 5px; }
        .stat-labels-tiny span { width: 40px; text-align: center; }

        /* --- ABILITIES --- */
        .abilities-box { padding: 20px 25px; font-size: 15px; line-height: 1.3; }
        .ability-item { margin-bottom: 12px; }
        .ability-item b { text-transform: uppercase; }
        .core-faction-line { border-bottom: 1px solid #ddd; padding-bottom: 8px; margin-bottom: 12px; font-weight: 900; text-transform: uppercase; font-size: 14px; }

        /* --- DAMAGED BLOCK --- */
        .damaged-block { background: #333; color: white; padding: 12px 25px; display: flex; align-items: center; gap: 20px; }
        .damaged-block b { font-family: 'Exo 2'; text-transform: uppercase; font-size: 15px; display: block; }
        .damaged-block p { margin: 0; font-size: 14px; }
        .skull { font-size: 24px; }

        /* --- UNIT COMPOSITION & POINTS --- */
        .comp-container { padding: 20px 25px; position: relative; min-height: 120px; }
        .points-badge { 
            position: absolute; bottom: 15px; right: 15px; 
            border: 4px solid black; padding: 10px 20px; 
            font-size: 32px; font-weight: 900; font-family: 'Exo 2';
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0 100%);
            background: white;
        }

        /* --- FOOTER --- */
        .ds-footer { border-top: 3px solid var(--ink-black); padding: 10px 30px; display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; background: #f9f9f9; }
        .footer-label { font-weight: 900; text-transform: uppercase; margin-right: 5px; }

        @media print {
            body { background: white; padding: 0; }
            .datasheet { width: 100%; box-shadow: none; border-width: 1px; }
            .toc-container { display: none; }
        }
    </style>
</head>
<body>

<div id="roster"></div>

<script>
    const units = {{UNITS_JSON}};
    
    document.getElementById('roster').innerHTML = units.map(u => {
        // High fidelity keyword cleanup
        const cleanInvuln = (u.invuln || "").replace(':', '').trim();
        
        return `
        <div class="datasheet">
            <div class="ds-header">
                <h1>${u.name}</h1>
            </div>
            
            <div class="stats-bar">
                ${['M','T','Sv','W','Ld','OC'].map(s => `
                    <div class="stat-box">
                        <div class="stat-label">${s}</div>
                        <div class="stat-val">${u.stats[s] || '-'}</div>
                    </div>
                `).join('')}
            </div>

            ${cleanInvuln && cleanInvuln !== '-' ? `
                <div class="invuln-container">
                    <div class="shield-icon">${cleanInvuln}</div>
                    <div class="invuln-label">Invulnerable Save</div>
                </div>
            ` : '<div style="height:20px"></div>'}

            <div class="main-grid">
                <div class="left-col">
                    ${u.weapons.ranged.length ? `
                        <div class="section-header">
                            <span>Ranged Weapons</span>
                            <div class="stat-labels-tiny">
                                <span>RNG</span><span>A</span><span>BS</span><span>S</span><span>AP</span><span>D</span>
                            </div>
                        </div>
                        ${u.weapons.ranged.map(w => renderWeapon(w, 'BS')).join('')}
                    ` : ''}
                    
                    ${u.weapons.melee.length ? `
                        <div class="section-header">
                            <span>Melee Weapons</span>
                            <div class="stat-labels-tiny">
                                <span>RNG</span><span>A</span><span>WS</span><span>S</span><span>AP</span><span>D</span>
                            </div>
                        </div>
                        ${u.weapons.melee.map(w => renderWeapon(w, 'WS')).join('')}
                    ` : ''}
                </div>
                
                <div class="right-col">
                    <div class="section-header">Abilities</div>
                    <div class="abilities-box">
                        ${u.core_abilities ? `<div class="core-faction-line">Core: ${u.core_abilities}</div>` : ''}
                        ${u.faction_abilities ? `<div class="core-faction-line">Faction: ${u.faction_abilities}</div>` : ''}
                        <div class="md-content">${marked.parse(u.abilities_raw)}</div>
                    </div>

                    ${u.damaged_state ? `
                        <div class="damaged-block">
                            <span class="skull">💀</span>
                            <div>
                                <b>DAMAGED: ${u.damaged_state.split(':')[0]}</b>
                                <p>${u.damaged_state.split(':').slice(1).join(':').trim()}</p>
                            </div>
                        </div>
                    ` : ''}

                    <div class="section-header">Unit Composition</div>
                    <div class="comp-container">
                        <div class="md-content">${marked.parse(u.composition_raw)}</div>
                        <div class="points-badge">${u.points}</div>
                    </div>
                </div>
            </div>

            <div class="ds-footer">
                <div><span class="footer-label">Keywords:</span> ${u.keywords.toUpperCase()}</div>
                <div style="border-left: 2px solid #ccc; padding-left: 20px;"><span class="footer-label">Faction:</span> ${u.faction.toUpperCase()}</div>
            </div>
        </div>
        `;
    }).join('');

    function renderWeapon(w, skillType) {
        return `
            <div class="weapon-row">
                <div>
                    <div class="weapon-name">${w.name}</div>
                    ${(w.tags || []).map(t => `<span class="weapon-tags">${t}</span>`).join(' ')}
                </div>
                <div class="weapon-stats">
                    <span>${w.rng || w.range}</span>
                    <span>${w.a || w.attacks}</span>
                    <span>${w.skill || w.bs || w.ws}</span>
                    <span>${w.s || w.strength}</span>
                    <span>${w.ap}</span>
                    <span>${w.d || w.damage}</span>
                </div>
            </div>
        `;
    }
</script>
</body>
</html>
"""
    final_html = html_template.replace("{{FACTION}}", faction.replace('_', ' ').title()).replace("{{UNITS_JSON}}", json.dumps(units))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Success: Rendered {len(units)} units to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db", help="Path to the database.json file")
    args = parser.parse_args()
    main(args.db)

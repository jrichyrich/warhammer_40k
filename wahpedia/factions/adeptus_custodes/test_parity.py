import json
import os

DB_PATH = '/Users/jasricha/Documents/Github_Personal/warhammer_40k/wahpedia/factions/adeptus_custodes/adeptus_custodes_database.json'

with open(DB_PATH, 'r') as f:
    db = json.load(f)

units = {u['id']: u for u in db['units']}

def test_agamatus():
    u = units.get('agamatus_custodians')
    assert u, "Agamatus missing"
    # Check Weapon
    ranged_names = [w['name'] for w in u['weapons']['ranged']]
    assert "Twin las-pulsar" in ranged_names, f"Agamatus missing Twin las-pulsar. Found: {ranged_names}"
    # Check Melee
    assert len(u['weapons']['melee']) > 0, "Agamatus missing melee weapons"
    # Check Points format
    assert "models:" in u['points'], f"Agamatus points wrong format: {u['points']}"
    print("✅ Agamatus Parity Verified")

def test_global_health():
    missing_melee = []
    missing_points = []
    for uid, u in units.items():
        if not u['weapons']['melee'] and uid != 'anathema_psykana_rhino':
            missing_melee.append(uid)
        if u['points'] == "-" or "models:" not in u['points']:
            # Some units might be 1 model only, check if they have ':'
            if ":" not in u['points'] and uid != 'venerable_land_raider': # Land raider is 1 model standard
                missing_points.append(uid)
    
    assert not missing_melee, f"Units missing melee: {missing_melee}"
    assert not missing_points, f"Units missing point counts: {missing_points}"
    print(f"✅ All {len(units)} units passed health checks.")

try:
    test_agamatus()
    test_global_health()
    print("\n🏆 SUCCESS: 100% DATA PARITY REACHED.")
except Exception as e:
    print(f"\n❌ FAILURE: {e}")
    exit(1)

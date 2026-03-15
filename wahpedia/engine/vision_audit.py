import os
import json
import argparse

def main(faction_dir, image_dir):
    faction_name = os.path.basename(faction_dir.strip('/'))
    db_path = os.path.join(faction_dir, f"{faction_name}_database.json")
    
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found. Run ingest.py first.")
        return

    with open(db_path, 'r') as f:
        db = json.load(f)

    # 1. Identify units missing points
    missing = []
    for unit in db['units']:
        if unit['points'] == "-" or unit['points'] == "0":
            # Try to find a matching image
            img_name = unit['name'].replace(' ', '-').replace('(', '').replace(')', '') + ".png"
            img_path = os.path.join(image_dir, img_name)
            
            # Fuzzy match fallback
            if not os.path.exists(img_path):
                # Try underscores
                img_name = unit['id'] + ".png"
                img_path = os.path.join(image_dir, img_name)

            missing.append({
                "id": unit['id'],
                "name": unit['name'],
                "image_exists": os.path.exists(img_path),
                "image_path": img_path if os.path.exists(img_path) else "MISSING"
            })

    if not missing:
        print("✅ All units have points! No audit needed.")
        return

    # 2. Generate the "Audit Request" for the AI
    print(f"\n🚨 Found {len(missing)} units missing points.")
    print("-" * 30)
    
    audit_request = {
        "instruction": "Extract the point cost from the slanted red badge in the bottom-right corner of these images.",
        "units_to_audit": [m for m in missing if m['image_exists']]
    }

    request_file = os.path.join(faction_dir, "pending_vision_audit.json")
    with open(request_file, 'w') as f:
        json.dump(audit_request, f, indent=2)

    print(f"📝 Audit request saved to: {request_file}")
    print(f"👉 You can now pass this file to a Vision AI to get the missing points.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("faction_dir")
    parser.add_argument("image_dir")
    args = parser.parse_args()
    main(args.faction_dir, args.image_dir)

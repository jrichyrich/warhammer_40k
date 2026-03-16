import os
import json
import argparse

def main(faction_dir, image_dir):
    faction_name = os.path.basename(faction_dir.strip('/'))
    db_path = os.path.join(faction_dir, f"{faction_name}_database.json")
    
    with open(db_path, 'r') as f:
        db = json.load(f)

    images = os.listdir(image_dir)
    missing = []
    
    for unit in db['units']:
        if unit['points'] == "-" or unit['points'] == "0":
            clean_name = unit['name'].replace('Datasheet:', '').strip()
            slug = clean_name.replace(' ', '-').replace('(', '').replace(')', '').replace(':', '')
            img_name = slug + ".png"
            
            match = None
            # 1. Direct Slug Match
            for img in images:
                if img.lower() == img_name.lower():
                    match = img
                    break
            
            # 2. Contains Match
            if not match:
                for img in images:
                    img_clean = img.replace('.png', '').replace('-', ' ').lower()
                    if clean_name.lower() in img_clean or img_clean in clean_name.lower():
                        match = img
                        break

            missing.append({
                "id": unit['id'],
                "name": unit['name'],
                "image_exists": match is not None,
                "image_path": os.path.join(image_dir, match) if match else "MISSING"
            })

    audit_request = {
        "instruction": "Extract the point cost from the slanted red badge in the bottom-right corner.",
        "units_to_audit": [m for m in missing if m['image_exists']]
    }

    request_file = os.path.join(faction_dir, "pending_vision_audit.json")
    with open(request_file, 'w') as f:
        json.dump(audit_request, f, indent=2)

    print(f"🚨 Found {len(audit_request['units_to_audit'])} units matching images out of {len(missing)} missing points.")
    if len(audit_request['units_to_audit']) < len(missing):
        unmatched = [m['name'] for m in missing if not m['image_exists']]
        print(f"⚠️ Unmatched: {unmatched[:5]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("faction_dir")
    parser.add_argument("image_dir")
    args = parser.parse_args()
    main(args.faction_dir, args.image_dir)

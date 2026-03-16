import json
import os

DIR = '/Users/jasricha/Documents/Github_Personal/warhammer_40k/wahpedia/factions/adeptus_custodes'
PATCH_FILE = os.path.join(DIR, 'roster_patches.json')

full_data = {
    "agamatus_custodians": {
        "stats": {"M": "12\"", "T": "6", "Sv": "2+", "W": "4", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "3 models: 225, 6 models: 450",
        "ranged": [
            {"name": "Adrathic devastator", "rng": "18\"", "a": "1", "skill": "2+", "s": "7", "ap": "-2", "d": "3", "tags": []},
            {"name": "Lastrum bolt cannon", "rng": "36\"", "a": "3", "skill": "2+", "s": "6", "ap": "-1", "d": "1", "tags": ["Sustained Hits 1"]},
            {"name": "Twin las-pulsar", "rng": "24\"", "a": "2", "skill": "2+", "s": "9", "ap": "-1", "d": "2", "tags": ["Twin-linked"]}
        ],
        "melee": [{"name": "Interceptor lance", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": ["Lance"]}],
        "abilities_raw": "### Faction\n* Martial Ka'tah\n\n### Datasheet\n* **Turbo-boost**: Each time this unit Advances, do not make an Advance roll. Instead, until the end of the phase, add 6\" to the Move characteristic of models in this unit.\n* **Implacable Vanguard**: Once per battle, in your Shooting phase, after this unit has shot, if it is not within Engagement Range of one or more enemy units, it can make a Normal move of up to 6\". If it does, until the end of the turn, this unit is not eligible to declare a charge.",
        "composition_raw": "* 3-6 Agamatus Custodians\n* Every model is equipped with: lastrum bolt cannon; interceptor lance.",
        "keywords": "MOUNTED, FLY, IMPERIUM, AGAMATUS CUSTODES", "faction": "ADEPTUS CUSTODES"
    },
    "aleya": {
        "stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "4", "Ld": "6+", "OC": "1"},
        "invuln": "5+", "points": "1 model: 65",
        "ranged": [],
        "melee": [{"name": "Somnus", "rng": "Melee", "a": "4", "skill": "2+", "s": "6", "ap": "-3", "d": "3", "tags": ["Anti-Psyker 5+", "Devastating Wounds"]}],
        "abilities_raw": "### Core\n* Feel No Pain 5+, Leader, Scouts 6\"\n\n### Datasheet\n* **Tactical Perception**: Models in unit have Fights First.\n* **Tenacious Spirit**: +1 to Hit if below starting strength, +1 to Wound if below half.",
        "composition_raw": "1 Aleya - Epic Hero", "keywords": "CHARACTER, EPIC HERO, ANATHEMA PSYKANA", "faction": "ADEPTUS CUSTODES"
    },
    "allarus_custodians": {
        "stats": {"M": "5\"", "T": "7", "Sv": "2+", "W": "4", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "2 models: 110, 3 models: 165, 5 models: 275, 6 models: 330",
        "ranged": [
            {"name": "Balistus grenade launcher", "rng": "18\"", "a": "D6", "skill": "2+", "s": "4", "ap": "-1", "d": "1", "tags": ["Blast"]},
            {"name": "Guardian spear", "rng": "24\"", "a": "2", "skill": "2+", "s": "4", "ap": "-1", "d": "2", "tags": ["Assault"]}
        ],
        "melee": [{"name": "Guardian spear", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "### Faction\n* Martial Ka'tah\n\n### Datasheet\n* **Slayers of Tyrants**: Re-roll Wound rolls against Character, Monster or Vehicle.",
        "composition_raw": "2-6 Models", "keywords": "INFANTRY, TERMINATOR, ADEPTUS CUSTODES", "faction": "ADEPTUS CUSTODES"
    },
    "aquilon_custodians": {
        "stats": {"M": "5\"", "T": "7", "Sv": "2+", "W": "4", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "3 models: 195, 6 models: 390",
        "ranged": [{"name": "Lastrum storm bolter", "rng": "24\"", "a": "2", "skill": "2+", "s": "5", "ap": "-1", "d": "1", "tags": ["Rapid Fire 2"]}],
        "melee": [{"name": "Solerite power gauntlet", "rng": "Melee", "a": "5", "skill": "2+", "s": "8", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "Heavy Assault Infantry: Re-roll Wound roll of 1 against closest target.",
        "composition_raw": "3-6 Models", "keywords": "INFANTRY, TERMINATOR", "faction": "ADEPTUS CUSTODES"
    },
    "ares_gunship": {
        "stats": {"M": "20+\"", "T": "12", "Sv": "2+", "W": "22", "Ld": "6+", "OC": "0"},
        "invuln": "5+", "points": "1 model: 580",
        "ranged": [{"name": "Arachnus magna-blaze cannon", "rng": "48\"", "a": "3", "skill": "2+", "s": "18", "ap": "-4", "d": "D6+6", "tags": []}],
        "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "9", "skill": "4+", "s": "9", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Infernus Firebombs: Select enemy unit moved over, mortal wounds on 6s.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, AIRCRAFT, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "blade_champion": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "6", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 120",
        "ranged": [],
        "melee": [{"name": "Vaultswords - Victus", "rng": "Melee", "a": "5", "skill": "2+", "s": "6", "ap": "-3", "d": "3", "tags": ["Devastating Wounds"]}],
        "abilities_raw": "Swift Onslaught: Re-roll Charge rolls.",
        "composition_raw": "1 Model", "keywords": "INFANTRY, CHARACTER", "faction": "ADEPTUS CUSTODES"
    },
    "caladius_grav_tank": {
        "stats": {"M": "12\"", "T": "11", "Sv": "2+", "W": "14", "Ld": "6+", "OC": "5"},
        "invuln": "5+", "points": "1 model: 215",
        "ranged": [{"name": "Twin arachnus heavy blaze cannon", "rng": "48\"", "a": "4", "skill": "2+", "s": "12", "ap": "-3", "d": "D6+2", "tags": ["Twin-linked"]}],
        "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "4", "skill": "4+", "s": "6", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Advanced Firepower: Lethal Hits against specific targets.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "contemptor_achillus_dreadnought": {
        "stats": {"M": "9\"", "T": "9", "Sv": "2+", "W": "10", "Ld": "6+", "OC": "3"},
        "invuln": "5+", "points": "1 model: 155",
        "ranged": [{"name": "Twin adrathic destructor", "rng": "18\"", "a": "1", "skill": "2+", "s": "6", "ap": "-2", "d": "3", "tags": ["Twin-linked"]}],
        "melee": [{"name": "Achillus dreadspear", "rng": "Melee", "a": "5", "skill": "2+", "s": "12", "ap": "-2", "d": "D6+1", "tags": ["Lance"]}],
        "abilities_raw": "Dread Foe: Mortal wounds in melee.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, WALKER", "faction": "ADEPTUS CUSTODES"
    },
    "contemptor_galatus_dreadnought": {
        "stats": {"M": "9\"", "T": "9", "Sv": "2+", "W": "10", "Ld": "6+", "OC": "3"},
        "invuln": "4+", "points": "1 model: 165",
        "ranged": [{"name": "Galatus warblade", "rng": "12\"", "a": "D6", "skill": "N/A", "s": "6", "ap": "-1", "d": "1", "tags": ["Torrent"]}],
        "melee": [{"name": "Galatus warblade", "rng": "Melee", "a": "8", "skill": "2+", "s": "8", "ap": "-2", "d": "3", "tags": []}],
        "abilities_raw": "Galatus Shield: -1 to Wound in melee.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, WALKER", "faction": "ADEPTUS CUSTODES"
    },
    "coronus_grav_carrier": {
        "stats": {"M": "12\"", "T": "12", "Sv": "3+", "W": "16", "Ld": "6+", "OC": "5"},
        "invuln": "5+", "points": "1 model: 200",
        "ranged": [{"name": "Twin lastrum bolt cannon", "rng": "36\"", "a": "3", "skill": "2+", "s": "6", "ap": "-1", "d": "1", "tags": ["Sustained Hits 1"]}],
        "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "6", "skill": "4+", "s": "8", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Fire Support: Re-roll wounds for disembarked units.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, TRANSPORT, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "custodian_guard_with_adrasite_and_pyrithite_spears": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "3", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "5 models: 250",
        "ranged": [{"name": "Adrasite spear", "rng": "18\"", "a": "1", "skill": "2+", "s": "5", "ap": "-2", "d": "3", "tags": []}],
        "melee": [{"name": "Adrasite spear", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "Stand Vigil: Objective control bonuses.",
        "composition_raw": "5 Models", "keywords": "INFANTRY", "faction": "ADEPTUS CUSTODES"
    },
    "custodian_wardens": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "3", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "4 models: 210, 5 models: 260",
        "ranged": [{"name": "Guardian spear", "rng": "24\"", "a": "2", "skill": "2+", "s": "4", "ap": "-1", "d": "2", "tags": ["Assault"]}],
        "melee": [{"name": "Guardian spear", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "Living Fortress: Once per battle FNP 4+.",
        "composition_raw": "4-5 Models", "keywords": "INFANTRY", "faction": "ADEPTUS CUSTODES"
    },
    "knight_centura": {
        "stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "4", "Ld": "6+", "OC": "1"},
        "invuln": "5+", "points": "1 model: 55",
        "ranged": [{"name": "Witchseeker flamer", "rng": "12\"", "a": "D6", "skill": "N/A", "s": "4", "ap": "0", "d": "1", "tags": ["Torrent"]}],
        "melee": [{"name": "Executioner greatblade", "rng": "Melee", "a": "3", "skill": "2+", "s": "5", "ap": "-2", "d": "2", "tags": ["Anti-Psyker 5+"]}],
        "abilities_raw": "Seeker's Instincts: Speed and Charge bonuses.",
        "composition_raw": "1 Model", "keywords": "INFANTRY, CHARACTER, ANATHEMA PSYKANA", "faction": "ADEPTUS CUSTODES"
    },
    "orion_assault_dropship": {
        "stats": {"M": "20+\"", "T": "12", "Sv": "2+", "W": "22", "Ld": "6+", "OC": "0"},
        "invuln": "5+", "points": "1 model: 690",
        "ranged": [{"name": "Arachnus heavy blaze cannon", "rng": "36\"", "a": "4", "skill": "2+", "s": "12", "ap": "-3", "d": "D6+1", "tags": []}],
        "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "9", "skill": "4+", "s": "9", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Assault Dropship: Charge after disembark.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, AIRCRAFT, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "pallas_grav_attack": {
        "stats": {"M": "12\"", "T": "10", "Sv": "2+", "W": "10", "Ld": "6+", "OC": "2"},
        "invuln": "5+", "points": "1 model: 105",
        "ranged": [{"name": "Twin arachnus blaze cannon", "rng": "24\"", "a": "8", "skill": "2+", "s": "5", "ap": "-1", "d": "1", "tags": ["Twin-linked"]}],
        "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "3", "skill": "4+", "s": "6", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Merciless Hunter: +1 to Wound against weak units.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "prosecutors": {
        "stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "1", "Ld": "6+", "OC": "2"},
        "points": "4 models: 40, 5 models: 50, 9 models: 75, 10 models: 85",
        "ranged": [{"name": "Boltgun", "rng": "24\"", "a": "1", "skill": "3+", "s": "4", "ap": "0", "d": "1", "tags": ["Rapid Fire 1"]}],
        "melee": [{"name": "Close combat weapon", "rng": "Melee", "a": "2", "skill": "3+", "s": "3", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Purity of Execution: Anti-Psyker bonuses.",
        "composition_raw": "4-10 Models", "keywords": "INFANTRY, ANATHEMA PSYKANA", "faction": "ADEPTUS CUSTODES"
    },
    "sagittarum_custodians": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "3", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "5 models: 225",
        "ranged": [{"name": "Adrastus bolt caliver", "rng": "36\"", "a": "3", "skill": "2+", "s": "5", "ap": "-1", "d": "2", "tags": ["Sustained Hits 1"]}],
        "melee": [{"name": "Misericordia", "rng": "Melee", "a": "4", "skill": "2+", "s": "5", "ap": "-2", "d": "1", "tags": []}],
        "abilities_raw": "Saturation Volleys: Suppress enemy units.",
        "composition_raw": "5 Models", "keywords": "INFANTRY", "faction": "ADEPTUS CUSTODES"
    },
    "shield_captain": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "6", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 120",
        "ranged": [{"name": "Guardian spear", "rng": "24\"", "a": "2", "skill": "2+", "s": "4", "ap": "-1", "d": "2", "tags": ["Assault"]}],
        "melee": [{"name": "Guardian spear", "rng": "Melee", "a": "7", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "Strategic Mastery: 0CP Stratagem use.",
        "composition_raw": "1 Model", "keywords": "INFANTRY, CHARACTER", "faction": "ADEPTUS CUSTODES"
    },
    "shield_captain_in_allarus_terminator_armour": {
        "stats": {"M": "5\"", "T": "7", "Sv": "2+", "W": "7", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 130",
        "ranged": [{"name": "Balistus grenade launcher", "rng": "18\"", "a": "D6", "skill": "2+", "s": "4", "ap": "-1", "d": "1", "tags": ["Blast"]}],
        "melee": [{"name": "Guardian spear", "rng": "Melee", "a": "7", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": []}],
        "abilities_raw": "Auramite and Adamantine: Reduce damage to 1.",
        "composition_raw": "1 Model", "keywords": "INFANTRY, CHARACTER, TERMINATOR", "faction": "ADEPTUS CUSTODES"
    },
    "shield_captain_on_dawneagle_jetbike": {
        "stats": {"M": "12\"", "T": "6", "Sv": "2+", "W": "9", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 150",
        "ranged": [{"name": "Salvo launcher", "rng": "24\"", "a": "1", "skill": "2+", "s": "10", "ap": "-3", "d": "D6+1", "tags": ["Twin-linked"]}],
        "melee": [{"name": "Interceptor lance", "rng": "Melee", "a": "6", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": ["Lance"]}],
        "abilities_raw": "Sweeping Advance: Move after fighting.",
        "composition_raw": "1 Model", "keywords": "MOUNTED, CHARACTER, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "telemon_heavy_dreadnought": {
        "stats": {"M": "8\"", "T": "12", "Sv": "2+", "W": "14", "Ld": "6+", "OC": "4"},
        "invuln": "4+", "points": "1 model: 235",
        "ranged": [{"name": "Iliastus accelerator culverin", "rng": "48\"", "a": "4", "skill": "2+", "s": "9", "ap": "-1", "d": "3", "tags": []}],
        "melee": [{"name": "Telemon caestus", "rng": "Melee", "a": "5", "skill": "2+", "s": "12", "ap": "-2", "d": "3", "tags": []}],
        "abilities_raw": "Guardian Eternal: -1 Damage received.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, WALKER", "faction": "ADEPTUS CUSTODES"
    },
    "trajann_valoris": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "7", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 140",
        "ranged": [{"name": "Eagle's Scream", "rng": "24\"", "a": "2", "skill": "2+", "s": "5", "ap": "-2", "d": "3", "tags": ["Assault"]}],
        "melee": [{"name": "Watcher's Axe", "rng": "Melee", "a": "6", "skill": "2+", "s": "10", "ap": "-2", "d": "3", "tags": []}],
        "abilities_raw": "Moment Shackle: 2+ Invuln or 12 Attacks.",
        "composition_raw": "1 Model", "keywords": "CHARACTER, EPIC HERO", "faction": "ADEPTUS CUSTODES"
    },
    "valerian": {
        "stats": {"M": "6\"", "T": "6", "Sv": "2+", "W": "6", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "1 model: 110",
        "ranged": [{"name": "Gnosis", "rng": "24\"", "a": "3", "skill": "2+", "s": "4", "ap": "-1", "d": "2", "tags": ["Assault"]}],
        "melee": [{"name": "Gnosis", "rng": "Melee", "a": "7", "skill": "2+", "s": "8", "ap": "-3", "d": "2", "tags": []}],
        "abilities_raw": "Hero of Lion's Gate: Change roll to 6.",
        "composition_raw": "1 Model", "keywords": "CHARACTER, EPIC HERO", "faction": "ADEPTUS CUSTODES"
    },
    "venatari_custodians": {
        "stats": {"M": "10\"", "T": "6", "Sv": "2+", "W": "3", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "3 models: 165, 6 models: 330",
        "ranged": [{"name": "Venatari lance", "rng": "24\"", "a": "2", "skill": "2+", "s": "4", "ap": "-1", "d": "2", "tags": ["Assault"]}],
        "melee": [{"name": "Venatari lance", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": ["Lance"]}],
        "abilities_raw": "Swooping Dive: Rapid Ingress for 0CP.",
        "composition_raw": "3-6 Models", "keywords": "INFANTRY, JUMP PACK, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "venerable_contemptor_dreadnought": {
        "stats": {"M": "9\"", "T": "9", "Sv": "2+", "W": "10", "Ld": "6+", "OC": "3"},
        "invuln": "5+", "points": "1 model: 170",
        "ranged": [{"name": "Multi-melta", "rng": "18\"", "a": "2", "skill": "2+", "s": "9", "ap": "-4", "d": "D6", "tags": ["Melta 2"]}],
        "melee": [{"name": "Contemptor combat weapon", "rng": "Melee", "a": "5", "skill": "2+", "s": "12", "ap": "-2", "d": "3", "tags": []}],
        "abilities_raw": "Unyielding Ancient: Come back to life on 2+.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, WALKER", "faction": "ADEPTUS CUSTODES"
    },
    "venerable_land_raider": {
        "stats": {"M": "10\"", "T": "12", "Sv": "2+", "W": "16", "Ld": "6+", "OC": "5"},
        "points": "1 model: 220",
        "ranged": [{"name": "Godhammer lascannon", "rng": "48\"", "a": "2", "skill": "2+", "s": "12", "ap": "-3", "d": "D6+1", "tags": []}],
        "melee": [{"name": "Armoured tracks", "rng": "Melee", "a": "6", "skill": "4+", "s": "8", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Assault Ramp: Charge after move.",
        "composition_raw": "1 Model", "keywords": "VEHICLE, TRANSPORT", "faction": "ADEPTUS CUSTODES"
    },
    "vertus_praetors": {
        "stats": {"M": "12\"", "T": "6", "Sv": "2+", "W": "4", "Ld": "6+", "OC": "2"},
        "invuln": "4+", "points": "2 models: 150, 3 models: 225",
        "ranged": [{"name": "Salvo launcher", "rng": "24\"", "a": "1", "skill": "2+", "s": "10", "ap": "-3", "d": "D6+1", "tags": ["Twin-linked"]}],
        "melee": [{"name": "Interceptor lance", "rng": "Melee", "a": "5", "skill": "2+", "s": "7", "ap": "-2", "d": "2", "tags": ["Lance"]}],
        "abilities_raw": "Quicksilver Execution: Mortals after move.",
        "composition_raw": "2-3 Models", "keywords": "MOUNTED, FLY", "faction": "ADEPTUS CUSTODES"
    },
    "vigilators": {
        "stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "1", "Ld": "6+", "OC": "2"},
        "points": "4 models: 45, 5 models: 55, 9 models: 90, 10 models: 100",
        "ranged": [],
        "melee": [{"name": "Executioner greatblade", "rng": "Melee", "a": "2", "skill": "3+", "s": "5", "ap": "-2", "d": "2", "tags": ["Anti-Psyker 5+", "Devastating Wounds"]}],
        "abilities_raw": "Deft Parry: -1 to Hit against unit.",
        "composition_raw": "4-10 Models", "keywords": "INFANTRY, ANATHEMA PSYKANA", "faction": "ADEPTUS CUSTODES"
    },
    "witchseekers": {
        "stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "1", "Ld": "6+", "OC": "2"},
        "points": "4 models: 45, 5 models: 55, 9 models: 90, 10 models: 100",
        "ranged": [{"name": "Witchseeker flamer", "rng": "12\"", "a": "D6", "skill": "N/A", "s": "4", "ap": "0", "d": "1", "tags": ["Torrent"]}],
        "melee": [{"name": "Close combat weapon", "rng": "Melee", "a": "2", "skill": "3+", "s": "3", "ap": "0", "d": "1", "tags": []}],
        "abilities_raw": "Sanctified Flames: Force Battle-shock tests.",
        "composition_raw": "4-10 Models", "keywords": "INFANTRY, ANATHEMA PSYKANA", "faction": "ADEPTUS CUSTODES"
    },
    "coronus_grav_carrier": {"stats": {"M": "12\"", "T": "12", "Sv": "3+", "W": "16", "Ld": "6+", "OC": "5"}, "points": "1 model: 200", "melee": [{"name": "Armoured hull", "rng": "Melee", "a": "6", "skill": "4+", "s": "8", "ap": "0", "d": "1", "tags": []}], "ranged": [{"name": "Twin lastrum bolt cannon", "rng": "36\"", "a": "3", "skill": "2+", "s": "6", "ap": "-1", "d": "1", "tags": ["Sustained Hits 1"]}]},
    "prosecutors": {"stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "1", "Ld": "6+", "OC": "2"}, "points": "4 models: 40, 5 models: 50, 9 models: 75, 10 models: 85", "melee": [{"name": "Close combat weapon", "rng": "Melee", "a": "2", "skill": "3+", "s": "3", "ap": "0", "d": "1", "tags": []}], "ranged": [{"name": "Boltgun", "rng": "24\"", "a": "1", "skill": "3+", "s": "4", "ap": "0", "d": "1", "tags": ["Rapid Fire 1"]}]}
}

# Add missing ones
full_data["prosecutors"] = {"stats": {"M": "6\"", "T": "3", "Sv": "3+", "W": "1", "Ld": "6+", "OC": "2"}, "points": "4 models: 40, 5 models: 50, 9 models: 75, 10 models: 85", "melee": [{"name": "Close combat weapon", "rng": "Melee", "a": "2", "skill": "3+", "s": "3", "ap": "0", "d": "1", "tags": []}], "ranged": [{"name": "Boltgun", "rng": "24\"", "a": "1", "skill": "3+", "s": "4", "ap": "0", "d": "1", "tags": ["Rapid Fire 1"]}]}

with open(PATCH_FILE, 'w') as f:
    json.dump({"full_overrides": full_data}, f, indent=2)
print("Consolidated 31 units into roster_patches.json")

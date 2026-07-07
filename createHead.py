"""
createHead.py — VMH Behavior/Resource Pack Generator
=====================================================
Reads HeadsToCreate.csv and generates all required pack files for every
head listed.  Each row in the CSV fully describes one head:

  name, sound, model, texture, looting_chance, looting_mult, loot_entity, killed_by_player

Run:
    python createHead.py

Output folders VMH_BP/ and VMH_RP/ are written next to this script.
See HeadsToCreate.csv for full column documentation.
"""

import csv
import json
import os
import re
import shutil

# ============================================================
# CONFIGURATION
# ============================================================

# Input file — relative to this script
HEADS_CSV = "HeadsToCreate.csv"

# Heads that ship with fully hand-crafted block/attachable files inside
# the templates folder.  The generator skips auto-creating those file
# types for these names so the hand-crafted versions stay intact.
SPECIAL_HEADS = {"Slime", "Charged_Creeper", "Bogged", "Stray", "Sulfur_Cube"}

# Default values used when a CSV column is blank
DEFAULTS = {
    "sound":            "",
    "model":            "head",
    "texture":          "textures/blocks/skulls/missing",
    "looting_chance":   0.025,
    "looting_mult":     0.01,
    "loot_entity":      None,   # None → auto-derived from name
    "killed_by_player": False,
}

# ============================================================
# TEMPLATE REGISTRY
# Maps a logical template type to its source file and output path.
# [lower custom name] is replaced at generation time.
# ============================================================
TEMPLATE_REGISTRY = {
    "items_rp": {
        "template_file": "templates/items_rp.json",
        "file_path":     "VMH_RP/items/[lower custom name]_head.json",
    },
    "items_bp": {
        "template_file": "templates/items_bp.json",
        "file_path":     "VMH_BP/items/[lower custom name]_head.json",
    },
    "block": {
        "template_file": "templates/block.json",
        "file_path":     "VMH_BP/blocks/[lower custom name]_head.json",
    },
    "recipe_toBlock": {
        "template_file": "templates/recipe_toBlock.json",
        "file_path":     "VMH_BP/recipes/[lower custom name]_toBlock.json",
    },
    "recipe_toHead": {
        "template_file": "templates/recipe_toHead.json",
        "file_path":     "VMH_BP/recipes/[lower custom name]_toHead.json",
    },
    "attachable": {
        "template_file": "templates/attachable.json",
        "file_path":     "VMH_RP/attachables/[lower custom name]_head.json",
    },
}


# ============================================================
# CSV PARSING
# ============================================================

def parse_heads_csv(file_path):
    """
    Reads HeadsToCreate.csv and returns a list of head definition dicts.
    Lines starting with # are treated as comments and skipped.
    Missing or blank columns fall back to DEFAULTS.
    """
    heads = []

    with open(file_path, "r", encoding="utf-8") as f:
        cleaned_lines = [line for line in f if not line.lstrip().startswith("#")]

    reader = csv.DictReader(cleaned_lines)

    for row_num, row in enumerate(reader, start=2):
        name = row.get("name", "").strip()
        if not name:
            print(f"  WARNING: row {row_num} has no name — skipping.")
            continue

        def get(key, cast=str):
            val = row.get(key, "").strip()
            if not val:
                return DEFAULTS[key]
            try:
                return cast(val)
            except (ValueError, TypeError):
                print(f"  WARNING: row {row_num} ({name}): invalid '{key}' "
                      f"value '{val}' — using default {DEFAULTS[key]!r}.")
                return DEFAULTS[key]

        loot_entity_raw = row.get("loot_entity", "").strip()
        loot_entity = loot_entity_raw if loot_entity_raw else name.lower()

        heads.append({
            "name":             name,
            "sound":            get("sound") or DEFAULTS["sound"],
            "model":            get("model") or DEFAULTS["model"],
            "texture":          get("texture") or DEFAULTS["texture"],
            "looting_chance":   get("looting_chance", float),
            "looting_mult":     get("looting_mult", float),
            "loot_entity":      loot_entity,
            "killed_by_player": bool(int(get("killed_by_player", int) or 0)),
        })

    return heads


# ============================================================
# TEMPLATE-BASED FILE GENERATION
# ============================================================

def create_json_from_template(template_type, head_name,
                               model_name=None, texture_path=None):
    """
    Loads a JSON template, substitutes placeholders, and writes the result
    to the correct output path.

    Placeholders inside templates:
        [custom name]       → head_name (original casing)
        [lower custom name] → head_name.lower()
        [custom model name] → model_name
        [texture path]      → texture_path
    """
    lower_head_name = head_name.lower()

    if template_type not in TEMPLATE_REGISTRY:
        print(f"  ERROR: Unknown template type '{template_type}'.")
        return

    info = TEMPLATE_REGISTRY[template_type]
    template_path = info["template_file"]
    file_path = info["file_path"].replace("[lower custom name]", lower_head_name)

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_str = json.dumps(json.load(f))
    except Exception as e:
        print(f"  ERROR loading template '{template_path}': {e}")
        return

    template_str = template_str.replace("[custom name]",       head_name)
    template_str = template_str.replace("[lower custom name]", lower_head_name)
    template_str = template_str.replace("[custom model name]", model_name or "")
    template_str = template_str.replace("[texture path]",      texture_path or "")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json.loads(template_str), f, indent=4)
        print(f"  Created: {file_path}")
    except IOError as e:
        print(f"  ERROR writing '{file_path}': {e}")


# ============================================================
# LOOT TABLE GENERATION
# ============================================================

def create_loot_table_creeper(head_name, loot_entity):
    """
    Writes a simple (unconditional) loot table used by the charged-creeper
    kill mechanic.

    Output path: VMH_BP/loot_tables/vmh_creeper/<loot_entity>.json
    Item dropped: vmh:<lower_head_name>_head_block
    """
    lower_name = head_name.lower()
    file_path = f"VMH_BP/loot_tables/vmh_creeper/{loot_entity}.json"

    loot_data = {
        "pools": [
            {
                "rolls": 1,
                "entries": [
                    {
                        "type":   "item",
                        "name":   f"vmh:{lower_name}_head_block",
                        "weight": 1,
                    }
                ],
            }
        ]
    }

    _write_loot_table(file_path, loot_data)


def create_loot_table_looting(head_name, loot_entity,
                               looting_chance, looting_mult,
                               killed_by_player):
    """
    Writes a looting loot table for the standard kill mechanic.

    Output path: VMH_BP/loot_tables/vmh_looting/<loot_entity>.json
    Item dropped: vmh:<lower_head_name>_head_block

    Parameters
    ----------
    looting_chance   Base drop probability (0.0 – 1.0).
    looting_mult     Extra probability added per Looting enchantment level.
    killed_by_player When True, a killed_by_player condition is added.
                     Use this for passive mobs (e.g. Turtle) so the head
                     only drops when a player lands the killing blow.
    """
    lower_name = head_name.lower()
    file_path = f"VMH_BP/loot_tables/vmh_looting/{loot_entity}.json"

    conditions = []
    if killed_by_player:
        conditions.append({"condition": "killed_by_player"})
    conditions.append({
        "condition":          "random_chance_with_looting",
        "chance":             looting_chance,
        "looting_multiplier": looting_mult,
    })

    loot_data = {
        "pools": [
            {
                "rolls": 1,
                "entries": [
                    {
                        "type":   "item",
                        "name":   f"vmh:{lower_name}_head_block",
                        "weight": 1,
                    }
                ],
                "conditions": conditions,
            }
        ]
    }

    _write_loot_table(file_path, loot_data)


def _write_loot_table(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {file_path}")
    except IOError as e:
        print(f"  ERROR writing '{file_path}': {e}")


# ============================================================
# index.js UPDATE
# ============================================================

def update_index_js(head_name, sound):
    """
    Appends a [item_id, block_id, key, sound] tuple to the headArray
    inside VMH_BP/scripts/index.js.
    """
    file_name = "VMH_BP/scripts/index.js"
    lower_name = head_name.lower()
    lower_sound = sound.lower() if sound else "default"

    new_element = (
        f'["vmh:{lower_name}_head", "vmh:{lower_name}_head_block", '
        f'"{lower_name}_head", "{lower_sound}"]'
    )

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  ERROR: {file_name} not found.")
        return

    match = re.search(r"const headArray = \[.*?\];", content, re.DOTALL)
    if not match:
        print(f"  ERROR: {file_name} does not contain the expected headArray definition.")
        return

    existing = match.group(0)[match.group(0).find("[") + 1 :
                               match.group(0).rfind("]")].strip()
    if existing:
        updated = f"const headArray = [\n    {existing},\n    {new_element}\n];"
    else:
        updated = f"const headArray = [\n    {new_element}\n];"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content[: match.start()] + updated + content[match.end() :])

    print(f"  Updated: {file_name}  (+{head_name})")


# ============================================================
# SHARED / AGGREGATE FILE GENERATION
# ============================================================

def create_terrain_texture(head_names, head_textures):
    """Writes the combined terrain texture atlas JSON."""
    if len(head_names) != len(head_textures):
        raise ValueError("head_names and head_textures must be the same length.")

    file_name = "VMH_RP/textures/terrain_texture.json"
    texture_data = {
        f"{name.lower()}_head": {"textures": path}
        for name, path in zip(head_names, head_textures)
    }
    # Hard-coded overlays that are always present
    texture_data.update({
        "stray_head_overlay": {
            "textures": "textures/entity/skeleton/stray_overlay"
        },
        "bogged_head_overlay": {
            "textures": "textures/entity/skeleton/bogged_clothes"
        },
        "charged_creeper_head_overlay": {
            "textures": "textures/blocks/skulls/creeper/creeper_armor"
        },
        "sulfur_cube_head_inner": {
            "textures": "textures/entity/sulfur_cube/sulfur_cube_inner"
        },
    })

    final = {
        "num_mip_levels":     4,
        "padding":            8,
        "resource_pack_name": "vmh_head",
        "texture_name":       "atlas.terrain",
        "texture_data":       texture_data,
    }

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)
    print(f"\nCreated: {file_name}")


def create_place_sounds(head_names):
    """Writes blocks.json, assigning a place-sound to every head block."""
    file_name = "VMH_RP/blocks.json"
    data = {"format_version": "1.21.40"}
    for name in head_names:
        data[f"vmh:{name.lower()}_head_block"] = {"sound": "stone"}

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Created: {file_name}")


def create_lang_file(head_names):
    """Writes en_US.lang with display names for every head."""
    file_name = "VMH_RP/texts/en_US.lang"
    lines = []
    for name in head_names:
        lower   = name.lower()
        display = name.replace("_", " ") + " Head"
        lines.append(f"tile.vmh:{lower}_head_block.name={display}")
        lines.append(f"item.vmh:{lower}_head={display}")

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Created: {file_name}")


# ============================================================
# FOLDER COPY HELPER
# ============================================================

def copy_folder(src, dst):
    """Recursively copies src → dst, merging into any existing dst."""
    if not os.path.exists(src):
        print(f"  WARNING: Source folder does not exist: {src}")
        return
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print(f"Copied template: {src}  →  {dst}")


# ============================================================
# MAIN
# ============================================================

def main():
    # 1. Seed output folders from templates
    print("=" * 60)
    print("Step 1: Copying template pack folders")
    print("=" * 60)
    copy_folder("templates/VMH_RP", "VMH_RP")
    copy_folder("templates/VMH_BP", "VMH_BP")

    # 2. Parse input CSV
    print("\n" + "=" * 60)
    print(f"Step 2: Reading {HEADS_CSV}")
    print("=" * 60)
    heads = parse_heads_csv(HEADS_CSV)
    print(f"  Loaded {len(heads)} head definitions.\n")

    head_names    = []
    head_textures = []

    # 3. Generate per-head files
    print("=" * 60)
    print("Step 3: Generating per-head files")
    print("=" * 60)

    for head in heads:
        name             = head["name"]
        sound            = head["sound"]
        model            = head["model"]
        texture          = head["texture"]
        looting_chance   = head["looting_chance"]
        looting_mult     = head["looting_mult"]
        loot_entity      = head["loot_entity"]
        killed_by_player = head["killed_by_player"]

        print(f"\n[{name}]  loot_entity={loot_entity}  "
              f"chance={looting_chance}  mult={looting_mult}"
              + ("  killed_by_player" if killed_by_player else ""))

        # index.js entry
        update_index_js(name, sound)

        # Item and recipe files (generated for every head)
        create_json_from_template("items_rp",       name)
        create_json_from_template("items_bp",       name)
        create_json_from_template("recipe_toBlock", name)
        create_json_from_template("recipe_toHead",  name)

        # Block and attachable — skipped for special hand-crafted heads
        if name not in SPECIAL_HEADS:
            create_json_from_template("block",      name, model)
            create_json_from_template("attachable", name, model, texture)

        # Loot tables for both drop mechanisms
        create_loot_table_creeper(name, loot_entity)
        create_loot_table_looting(name, loot_entity,
                                  looting_chance, looting_mult,
                                  killed_by_player)

        head_names.append(name)
        head_textures.append(texture)

    # 4. Aggregate / shared files
    print("\n" + "=" * 60)
    print("Step 4: Writing shared pack files")
    print("=" * 60)
    create_place_sounds(head_names)
    create_lang_file(head_names)
    create_terrain_texture(head_names, head_textures)

    print("\n" + "=" * 60)
    print(f"Done!  Generated files for {len(head_names)} heads.")
    print("=" * 60)


if __name__ == "__main__":
    main()

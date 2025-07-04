import json
import os
import re
import shutil

# Template Registry (Mapping template types to their structures and paths)
TEMPLATE_REGISTRY = {
    "items_rp": {
        "template_file": "templates/items_rp.json",
        "file_path": "VMH_RP/items/[lower custom name]_head.json"
    },
    "items_bp": {
        "template_file": "templates/items_bp.json",
        "file_path": "VMH_BP/items/[lower custom name]_head.json"
    },
    "block": {
        "template_file": "templates/block.json",
        "file_path": "VMH_BP/blocks/[lower custom name]_head.json"
    },
    "recipe_toBlock": {
        "template_file": "templates/recipe_toBlock.json",
        "file_path": "VMH_BP/recipes/[lower custom name]_toBlock.json"
    },
    "recipe_toHead": {
        "template_file": "templates/recipe_toHead.json",
        "file_path": "VMH_BP/recipes/[lower custom name]_toHead.json"
    },
    "attachable": {
        "template_file": "templates/attachable.json",
        "file_path": "VMH_RP/attachables/[lower custom name]_head.json"
    }
}
def update_index_js(custom_name, sound):
    file_name = "VMH_BP/scripts/index.js"
    formatted_custom_name = custom_name.lower()
    formatted_sound = sound.lower()

    new_element = f'["vmh:{formatted_custom_name}_head", "vmh:{formatted_custom_name}_head_block", "{formatted_custom_name}_head", "{formatted_sound}"]'

    try:
        with open(file_name, "r") as file:
            content = file.read()

        match = re.search(r"const headArray = \[.*?\];", content, re.DOTALL)

        if match:
            before_array = content[:match.start()]
            after_array = content[match.end():]

            # Extract the existing array contents
            existing_elements = match.group(0)[match.group(0).find('[')+1:match.group(0).rfind(']')].strip()

            # Safely append the new element
            if existing_elements:
                updated_array = f'const headArray = [\n    {existing_elements},\n    {new_element}\n];'
            else:
                updated_array = f'const headArray = [\n    {new_element}\n];'

            with open(file_name, "w") as file:
                file.write(before_array + updated_array + after_array)

            print(f"Added new element for {custom_name} with sound {sound} to {file_name}")
        else:
            print(f"Error: {file_name} does not contain the expected headArray definition.")

    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_json_from_template(template_type, head_name, model_name=None, texture_path=None):

    lower_head_name = head_name.lower()

    if template_type not in TEMPLATE_REGISTRY:
        print(f"Error: Invalid template type '{template_type}'.")
        return

    template_info = TEMPLATE_REGISTRY[template_type]
    file_path_template = template_info["file_path"]
    template_path = template_info["template_file"]

    # Load the template from file
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = json.load(f)
    except Exception as e:
        print(f"Error loading template '{template_path}': {e}")
        return

    # Perform placeholder substitution
    json_str = json.dumps(template)
    json_str = json_str.replace("[custom name]", head_name)
    json_str = json_str.replace("[lower custom name]", lower_head_name)
    json_str = json_str.replace("[custom model name]", model_name or "")
    json_str = json_str.replace("[texture path]", texture_path or "")
    customized_template = json.loads(json_str)

    file_name = file_path_template
    file_name = file_name.replace("[lower custom name]", lower_head_name)

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(customized_template, file, indent=4)
        print(f"Successfully created {file_name} from the {template_type} template.")
    except IOError as e:
        print(f"Error writing file {file_name}: {e}")


# Creates Texture Atlas
def create_terrain_texture(head_names, head_textures):
    file_name = "VMH_RP/textures/terrain_texture.json"

    if len(head_names) != len(head_textures):
        raise ValueError("head_names and texture_paths must be the same length")

    texture_data = {
        f"{head.lower()}_head": {"textures": path}
        for head, path in zip(head_names, head_textures)
    }
    texture_data.update({
        "stray_head_overlay": {
            "textures": "textures/entity/skeleton/stray_overlay"
        },
        "bogged_head_overlay": {
            "textures": "textures/entity/skeleton/bogged_clothes"
        },
        "charged_creeper_head_overlay": {
            "textures": "textures/blocks/skulls/creeper/creeper_armor"
        }
    })

    final_json = {
        "num_mip_levels": 4,
        "padding": 8,
        "resource_pack_name": "vmh_head",
        "texture_name": "atlas.terrain",
        "texture_data": texture_data
    }

    with open(file_name, "w") as f:
        json.dump(final_json, f, indent=4)

    print(f"JSON file successfully written to '{file_name}'")

# Creates Sounds File
def create_place_sounds(head_names):
    file_name = "VMH_RP/blocks.json"

    # Start with format version
    data = {
        "format_version": "1.21.40"
    }

    for head_name in head_names:
        lower_head_name = head_name.lower()
        block_name = f"vmh:{lower_head_name}_head_block"
        data[block_name] = {"sound": "stone"}

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Successfully created {file_name} with block sounds.")
    except Exception as e:
        print(f"Error writing {file_name}: {e}")


# Creates the Language File
def create_lang_file(all_head_names):
    file_name = "VMH_RP/texts/en_US.lang"
    lines = []

    for head_name in all_head_names:
        lower_head_name = head_name.lower()
        display_name = head_name.replace("_", " ") + " Head"

        block_line = f"tile.vmh:{lower_head_name}_head_block.name={display_name}"
        item_line = f"item.vmh:{lower_head_name}_head={display_name}"

        lines.extend([block_line, item_line])

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Successfully created {file_name} with language entries.")
    except Exception as e:
        print(f"Error writing {file_name}: {e}")


# Creates RP and BP Folders
def copy_folder(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        return

    os.makedirs(destination_folder, exist_ok=True)

    for item in os.listdir(source_folder):
        src_path = os.path.join(source_folder, item)
        dst_path = os.path.join(destination_folder, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)

    print(f"Copied '{source_folder}' to '{destination_folder}'")


# Read Create Heads File
def parse_entity_data(file_path):
    entities = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    i = 0
    while i < len(lines):
        entity_name = lines[i]
        entity_sound = lines[i+1] if i+1 < len(lines) else "n"
        entity_model = lines[i+2] if i+2 < len(lines) else "n"
        entity_texture = lines[i+3] if i+3 < len(lines) else "n"
        
        entities[entity_name] = {
            "sound": entity_sound if entity_sound != "n" else None,
            "model": entity_model if entity_model != "n" else None,
            "texture": entity_texture if entity_texture != "n" else None,
        }
        
        i += 4
    
    return entities


def main():
    copy_folder("templates/VMH_RP", "VMH_RP")
    copy_folder("templates/VMH_BP", "VMH_BP")

    file_path = "HeadsToCreate.txt"
    entity_data = parse_entity_data(file_path)
    head_names = []
    head_textures = []

    for head_name, data in entity_data.items():
        sound_name = data["sound"] if data["sound"] else "default"
        model_name = data["model"] if data["model"] else "head"
        texture_path = data["texture"] if data["texture"] else "textures/blocks/skulls/missing"

        update_index_js(head_name, sound_name)
        create_json_from_template("items_rp", head_name)
        create_json_from_template("items_bp", head_name)
        create_json_from_template("recipe_toBlock", head_name)
        create_json_from_template("recipe_toHead", head_name)

        if head_name not in {"Slime", "Charged_Creeper", "Bogged", "Stray"}:
            create_json_from_template("block", head_name, model_name)
            create_json_from_template("attachable", head_name, model_name, texture_path)

        head_names.append(head_name)
        head_textures.append(texture_path)

    create_place_sounds(head_names)
    create_lang_file(head_names)
    create_terrain_texture(head_names, head_textures)

if __name__ == "__main__":
    main()
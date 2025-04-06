import json
import os
import re

# Template Registry (Mapping template types to their structures and paths)
TEMPLATE_REGISTRY = {
    "attachable": {
        "template": {
            "format_version": "1.10.0",
            "minecraft:attachable": {
                "description": {
                    "identifier": "vmh:[lower custom name]_head", 
                    "materials": {
                        "default": "armor",
                        "enchanted": "armor_enchanted"
                    },
                    "textures": {
                        "default": "textures/blocks/skulls/[custom name]",
                        "enchanted": "textures/misc/enchanted_item_glint"
                    },
                    "geometry": {
                        "default": "geometry.[custom model name]_attachable"
                    },
                    "render_controllers": [
                        "controller.render.item_default"
                    ]
                }
            }
        },
        "file_path": "VMH_RP/attachables/[lower custom name]_head.json"
    },
    "items_rp": {
        "template": {
            "format_version": "1.10",
            "minecraft:item": {
                "description": {
                    "identifier": "vmh:[lower custom name]_head_block",
                    "category": "null"
                },
                "components": {
                    "minecraft:rarity": "uncommon"
                }
            }
        },
        "file_path": "VMH_RP/items/[lower custom name]_head.json"
    },
    "items_bp": {
       "template": {
            "format_version": "1.21.40",
            "minecraft:item": {
                "description": {
                    "identifier": "vmh:[lower custom name]_head",
                    "menu_category": {
                        "category": "items",
                        "group": "itemGroup.name.skull"
                    }
                },
                "components": {
                    "minecraft:block_placer": {
                        "block": "vmh:[lower custom name]_head_block"
                    },
                    "minecraft:max_stack_size": {
                        "value": 1
                    },
                    "minecraft:wearable": {
                        "slot": "slot.armor.head"
                    },
                    "minecraft:rarity": "uncommon"
                }
            }
        },
        "file_path": "VMH_BP/items/[lower custom name]_head.json"
    },
    "block": {
        "template": {
            "format_version": "1.21.60",
            "minecraft:block": {
                "description": {
                    "identifier": "vmh:[lower custom name]_head_block",
                    "menu_category": {
                        "category": "none",
                        "is_hidden_in_commands": True
                    },
                    "traits": {
                        "minecraft:placement_position": {
                            "enabled_states": [
                                "minecraft:block_face"
                            ]
                        }
                    },
                    "states": {
                        "vmh:head_rotation": {
                            "values": {
                                "min": 0,
                                "max": 15
                            }
                        }
                    }
                },
                "components": {
                    "minecraft:liquid_detection": {
                        "detection_rules": [
                            {
                                "can_contain_liquid": True
                            }
                        ]
                    },
                    "minecraft:destructible_by_mining": {
                        "seconds_to_destroy": 1.5
                    },
                    "minecraft:collision_box": {
                        "origin": [
                            -4,
                            0,
                            -4
                        ],
                        "size": [
                            8,
                            8,
                            8
                        ]
                    },
                    "minecraft:selection_box": {
                        "origin": [
                            -4,
                            0,
                            -4
                        ],
                        "size": [
                            8,
                            8,
                            8
                        ]
                    },
                    "minecraft:geometry": {
                        "identifier": "geometry.[custom model name]",
                        "bone_visibility": {
                            "up_0": "q.block_state('minecraft:block_face') == 'up' && math.mod(q.block_state('vmh:head_rotation'), 4) == 0",
                            "up_22_5": "q.block_state('minecraft:block_face') == 'up' && math.mod(q.block_state('vmh:head_rotation'), 4) == 1",
                            "up_45": "q.block_state('minecraft:block_face') == 'up' && math.mod(q.block_state('vmh:head_rotation'), 4) == 2",
                            "up_67_5": "q.block_state('minecraft:block_face') == 'up' && math.mod(q.block_state('vmh:head_rotation'), 4) == 3",
                            "side": "q.block_state('minecraft:block_face') != 'up'"
                        }
                    },
                    "minecraft:custom_components": [
                        "vmh:rotation_comp",
                        "vmh:check_noteblock"
                    ],
                    "minecraft:tick": {
                        "interval_range": [10, 20],
                        "looping": True
                    },
                    "minecraft:material_instances": {
                        "*": {
                            "texture": "[lower custom name]_head",
                            "ambient_occlusion": False,
                            "render_method": "alpha_test"
                        },
                        "custom_down": {
                            "texture": "[lower custom name]_head",
                            "ambient_occlusion": False,
                            "render_method": "alpha_test"
                        },
                        "down": {
                            "texture": "soul_sand",
                            "render_method": "alpha_test"
                        }
                    },
                    "minecraft:light_dampening": 0,
                    "minecraft:placement_filter": {
                        "conditions": [
                            {
                                "allowed_faces": [
                                    "up",
                                    "side"
                                ]
                            }
                        ]
                    }
                },
                "permutations": [
                    {
                        "condition": "q.block_state('vmh:head_rotation') >= 4 || q.block_state('minecraft:block_face') == 'east'",
                        "components": {
                            "minecraft:transformation": {
                                "rotation": [
                                    0,
                                    -90,
                                    0
                                ]
                            }
                        }
                    },
                    {
                        "condition": "q.block_state('vmh:head_rotation') >= 8 || q.block_state('minecraft:block_face') == 'south'",
                        "components": {
                            "minecraft:transformation": {
                                "rotation": [
                                    0,
                                    180,
                                    0
                                ]
                            }
                        }
                    },
                    {
                        "condition": "q.block_state('vmh:head_rotation') >= 12 || q.block_state('minecraft:block_face') == 'west'",
                        "components": {
                            "minecraft:transformation": {
                                "rotation": [
                                    0,
                                    90,
                                    0
                                ]
                            }
                        }
                    },
                    {
                        "condition": "q.block_state('minecraft:block_face') != 'up'",
                        "components": {
                            "minecraft:collision_box": {
                                "origin": [
                                    -4,
                                    4,
                                    0
                                ],
                                "size": [
                                    8,
                                    8,
                                    8
                                ]
                            },
                            "minecraft:selection_box": {
                                "origin": [
                                    -4,
                                    4,
                                    0
                                ],
                                "size": [
                                    8,
                                    8,
                                    8
                                ]
                            }
                        }
                    }
                ]
            }
        },
        "file_path": "VMH_BP/blocks/[lower custom name]_head.json"
    },
}

def setDataArgs(c, d):
    args = {
        "a": c,
        "b": d
    }

    fileData = {
        "format_version": "1.20.10",
        "minecraft:recipe_shaped": {
            "description": {
                "identifier": "vmh:%s" %(args["a"])
            },
            "tags": [ 
                "crafting_table" 
            ],
            "group": "itemGroup.name.skull",
            "pattern": [
                "#"
            ],
            "key": {
                "#": {
                    "item": "vmh:%s" %(args["b"])
                }
            },
            "unlock": [
                {
                    "item": "vmh:%s" %(args["b"])
                }
            ],
            "result": {
                "item": "vmh:%s" %(args["a"]),
                "count": 1
            }
        }
    }

    return fileData

def createRecipes(headName):

    lowerHeadName = headName.lower()

    fileData = setDataArgs("%s_head" %(lowerHeadName), "%s_head_block" %(lowerHeadName))

    recipeTypes = ["toHead", "toBlock"]
    for recipeType in recipeTypes:
        with open("VMH_BP/recipes/%s_%s.json" %(lowerHeadName, recipeType), "w") as file:
            json_object = json.dumps(fileData, indent=4)
            file.write(json_object)

            fileData = setDataArgs("%s_head_block" %(lowerHeadName), "%s_head" %(lowerHeadName))


def update_index_js(custom_name, sound):
    file_name = "VMH_BP/scripts/index.js"
    formatted_custom_name = custom_name.lower()
    formatted_sound = sound.lower()

    # The new array element to append
    new_element = f'["vmh:{formatted_custom_name}_head", "vmh:{formatted_custom_name}_head_block", "{formatted_custom_name}_head", "{formatted_sound}"]'

    try:
        # Read the existing content from the index.js file
        with open(file_name, "r") as file:
            content = file.read()

        # Find the position of the headArray definition
        match = re.search(r"const headArray = \[.*?\];", content, re.DOTALL)

        if match:
            # Extract the part before and after the array to append the new element
            before_array = content[:match.start()]
            after_array = content[match.end():]

            # Append the new element inside the array
            updated_array = f'const headArray = [\n    ' + match.group(0)[match.group(0).find('[')+1:match.group(0).rfind(']')].strip() + ',\n    ' + new_element + '\n];'

            # Write the updated content back to the file
            with open(file_name, "w") as file:
                file.write(before_array + updated_array + after_array)

            print(f"Added new element for {custom_name} with sound {sound} to {file_name}")

        else:
            print(f"Error: {file_name} does not contain the expected headArray definition.")
    
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_json_from_template(template_type, head_name, model_name = None):
    """
    Creates a JSON file from a template, customized with the provided head name and model name.

    :param template_type: The type of template ("attachable", "item", "block", etc.).
    :param head_name: The custom name for the head.
    :param model_name: The custom model name (used for "attachable" templates).
    """
    lower_head_name = head_name.lower()

    # Check if the template type exists in the registry
    if template_type not in TEMPLATE_REGISTRY:
        print(f"Error: Invalid template type '{template_type}'.")
        return

    # Retrieve the template and file path from the registry
    template = TEMPLATE_REGISTRY[template_type]["template"]
    file_path_template = TEMPLATE_REGISTRY[template_type]["file_path"]

    # Replace placeholders in the template and file path
    customized_template = json.loads(json.dumps(template).replace("[custom name]", head_name).replace("[lower custom name]",lower_head_name).replace("[custom model name]", model_name or ""))

    # Define the file path using the head name
    file_name = file_path_template.replace("[lower custom name]", lower_head_name)

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    # Write the customized template to the JSON file
    try:
        with open(file_name, "w") as file:
            json.dump(customized_template, file, indent=4)

        print(f"Successfully created {file_name} from the {template_type} template.")

    except IOError as e:
        print(f"Error writing file {file_name}: {e}")

def update_json(file_name, key, update_data, nested_field=None):
    """
    General-purpose function to update a JSON file with new data.

    :param file_name: Path to the JSON file.
    :param key: The key to be added or updated in the JSON data.
    :param update_data: The data to associate with the key.
    :param nested_field: The nested field in the JSON where the update should be applied (optional).
    """
    try:
        # Open the file and load the JSON
        with open(file_name, "r") as file:
            data = json.load(file)

        # Update the data
        if nested_field:
            if nested_field in data:
                data[nested_field].update({key: update_data})
            else:
                print(f"Error: '{nested_field}' field not found in the JSON file.")
                return
        else:
            data.update({key: update_data})

        # Write the updated JSON back to the file
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Successfully updated {file_name} with key '{key}'.")

    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {file_name} as JSON.")


def update_place_sounds(head_name):
    """Updates the block placement sounds in the blocks.json file."""
    lower_head_name = head_name.lower()
    file_name = "VMH_RP/blocks.json"
    block_name = f"vmh:{lower_head_name}_head_block"
    new_block = {"sound": "stone"}

    update_json(file_name, block_name, new_block)


def update_lang_file(head_name):
    file_name = "VMH_RP/texts/en_US.lang"
    lower_head_name = head_name.lower()

    # Define the lines to add
    block_name = f"tile.vmh:{lower_head_name}_head_block.name={head_name.replace("_", " ")} Head"
    item_name = f"item.vmh:{lower_head_name}_head={head_name.replace("_", " ")} Head"
    lines_to_add = [block_name, item_name]

    try:
        with open(file_name, "a") as file:
            file.write("\n".join(lines_to_add) + "\n")

    except FileNotFoundError:
        print(f"Error: {file_name} not found.")


def parse_player_data(file_path):
    players = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    i = 0
    while i < len(lines):
        player_name = lines[i]
        player_sound = lines[i+1] if i+1 < len(lines) else "n"
        player_model = lines[i+2] if i+2 < len(lines) else "n"
        
        players[player_name] = {
            "sound": player_sound if player_sound != "n" else None,
            "model": player_model if player_model != "n" else None
        }
        
        i += 3
    
    return players


def main():
    file_path = "HeadsToCreate.txt"
    player_data = parse_player_data(file_path)
    
    for head_name, data in player_data.items():
        sound_name = data["sound"] if data["sound"] else "default"
        model_name = data["model"] if data["model"] else "head"

        update_index_js(head_name, sound_name)
        create_json_from_template("attachable", head_name, model_name)
        create_json_from_template("items_rp", head_name)
        create_json_from_template("items_bp", head_name)
        create_json_from_template("block", head_name, model_name)
        update_lang_file(head_name)
        update_place_sounds(head_name)
        createRecipes(head_name)

if __name__ == "__main__":
    main()
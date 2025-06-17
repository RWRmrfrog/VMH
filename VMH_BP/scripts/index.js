import { world, system, ItemStack } from "@minecraft/server";

/* 
    Arrays
*/

const blockMap = new Map();
const chargedCreepers = new Map();
const AngryMobs = new Map();
const blacklistMobs = [
    "minecraft:player",
    "minecraft:wither_skeleton",
    "minecraft:snowball",
    "minecraft:ender_eye",
    "minecraft:ender_pearl",
    "minecraft:splash_potion",
    "minecraft:xp_bottle",
    "minecraft:fireball",
    "minecraft:dragon_fireball",
    "minecraft:egg"
];
const variantMobs = [
    "minecraft:wolf",
    "minecraft:cat",
    "minecraft:fox",
    "minecraft:horse",
    "minecraft:llama",
    "minecraft:trader_llama",
    "minecraft:mooshroom",
    "minecraft:panda",
    "minecraft:parrot",
    "minecraft:rabbit",
    "minecraft:frog",
    "minecraft:axolotl"
];
const vanillaHeads = [
    "minecraft:creeper",
    "minecraft:skeleton",
    "minecraft:zombie",
    "minecraft:wither_skeleton",
    "minecraft:piglin",
    "minecraft:ender_dragon"
];
const headArray = [
    ,
];

function runCommand(command) {
    system.run(() => {
        world.getDimension("overworld").runCommand(command);
    });
}

/* 
    Track Charged Creepers, Angry Mobs, and Spawn Creaking Head
*/

world.beforeEvents.entityRemove.subscribe(({ removedEntity }) => {
    if (removedEntity.typeId == "minecraft:creeper" && removedEntity.getComponent('is_charged')) 
    {
        chargedCreepers.set(removedEntity.id, true);
    } 
    if (removedEntity.typeId === "minecraft:creaking") {
        const {x, y, z} = removedEntity.location;
        const command = `loot spawn ${x} ${y} ${z} loot \"vmh_looting/creaking\"`;
        runCommand(command);
    }
})

world.afterEvents.entityHurt.subscribe((event) => {
    const {hurtEntity, damageSource, damage} = event;
    if ((hurtEntity.typeId == "minecraft:wolf" || hurtEntity.typeId == "minecraft:bee") && hurtEntity.getComponent("health").currentValue >= damage && damageSource.damagingEntity.typeId == "minecraft:player") {
        AngryMobs.set(hurtEntity.id, true);
    } 
})

/* 
    Mobs Drop Heads
*/

world.afterEvents.entityDie.subscribe((event) => {
    const {damageSource, deadEntity} = event;
    const damagingEntity = damageSource.damagingEntity;

    if (blacklistMobs.includes(deadEntity.typeId)) { return; };

    const deadEntitySplit = deadEntity.typeId.split(":");
    let entity = deadEntitySplit[1];
    let tableLocation = "vmh_looting";

    entity = modEntityName(deadEntity, entity);

    // Drop 100% rate if killed by charged creeper

    if (chargedCreepers.has(damagingEntity.id))
    {
        chargedCreepers.delete(damagingEntity.id);  
        tableLocation = "vmh_creeper";
    }

    if (!(tableLocation == "vmh_creeper" && vanillaHeads.includes(deadEntity.typeId)))
    {
        const {x, y, z} = deadEntity.location;
        const command = `loot spawn ${x} ${y + 0.5} ${z} loot \"${tableLocation}/${entity}\"`;
        runCommand(command);

        // console.warn(`${command}`);
    }
});

function modEntityName(deadEntity, entity) {
    if (deadEntity.typeId == "minecraft:creeper" && deadEntity.getComponent('is_charged')) {
        entity = "charged_creeper";
    }
    else if (deadEntity.typeId == "minecraft:trader_llama") {
        entity = "llama";
    }
    else if (deadEntity.typeId == "minecraft:strider" && deadEntity.getComponent('is_shaking')) {
        entity = "suffocated_strider";
    }
    else if (deadEntity.typeId == "minecraft:happy_ghast" && deadEntity.getComponent('is_baby')) {
        entity = "ghastling";
    }
    else if (deadEntity.typeId == "minecraft:sheep") {
        const color = deadEntity.getComponent('color');
        entity += `_${color.value}`;
    }

    // Add Angry
    
    if (AngryMobs.has(deadEntity.id)) {
        AngryMobs.delete(deadEntity.id);
        entity = "angry_" + entity;
    }

    // Append Variant Number

    if (variantMobs.includes(deadEntity.typeId)) {
        const variant = deadEntity.getComponent('variant');
        if (!variant)
        {
            entity += `_0`;
        }
        else
        {
            entity += `_${variant.value}`;
        }
    }
    else if (deadEntity.typeId == "minecraft:cow" || deadEntity.typeId == "minecraft:chicken" || deadEntity.typeId == "minecraft:pig") {
        const variant = deadEntity.getProperty('minecraft:climate_variant');
        entity += `_${variant}`;
    }

    return entity;
}

/* 
    Block Rotation
*/

function getPreciseRotation(playerYRotation) {
    if (playerYRotation < 0) playerYRotation += 360;
    const rotation = Math.round(playerYRotation / 22.5);

    return rotation !== 16 ? rotation : 0;
};

const RotationBlockComponent = {
    beforeOnPlayerPlace(event) {
        const { player } = event;
        if (!player) return;

        const blockFace = event.permutationToPlace.getState("minecraft:block_face");
        if (blockFace !== "up") return;

        const playerYRotation = player.getRotation().y;
        const rotation = getPreciseRotation(playerYRotation);

        event.permutationToPlace = event.permutationToPlace.withState("vmh:head_rotation", rotation);
    }
};

world.beforeEvents.worldInitialize.subscribe(({ blockComponentRegistry }) => {
    blockComponentRegistry.registerCustomComponent("vmh:rotation_comp", RotationBlockComponent);
});


/* 
    Noteblock Functionality
*/

// Redstone power
world.beforeEvents.worldInitialize.subscribe(eventData =>{eventData.blockComponentRegistry.registerCustomComponent('vmh:check_noteblock', {
    onTick(event) { 
    const block = event.block;
    const blockBelow = block.below();
    const currentRedstonePower = blockBelow.getRedstonePower();
    const { x, y, z } = blockBelow.location
    const blockKey = `${x}*${y}*${z}`
    const blockObject = blockMap.get(blockKey) ?? {};
    const { previousRedstonePower } = blockObject;

    if (blockBelow.typeId == "minecraft:noteblock" && currentRedstonePower > 0 && currentRedstonePower != previousRedstonePower) {
        const location = blockBelow.location;
        for (let i = 0; i < headArray.length; i++) {
            if (block.typeId == headArray[i][1]) {
                world.playSound(headArray[i][3], location)
                break;
            }
        }
    }
    blockObject.previousRedstonePower = currentRedstonePower;
    blockMap.set(blockKey, blockObject)
}
})});

// Noteblock interaction
world.afterEvents.playerInteractWithBlock.subscribe((eventData) => {
    const { player } = eventData;
    if (!player) return;

    const item = player.getComponent('equippable')?.getEquipment('Mainhand');

    if(!(player.isSneaking))
    {
      const block = eventData.block;
      const blockAbove = block.dimension.getBlock({ x: block.location.x, y: (block.location.y) + 1, z: block.location.z });
      if (block.typeId == "minecraft:noteblock") {
          const location = block.location;
          for (let i = 0; i < headArray.length; i++) {
              if (blockAbove.typeId == headArray[i][1]) {
                  world.playSound(headArray[i][3], location)
                  break;
              }
          }
      }
    }
});
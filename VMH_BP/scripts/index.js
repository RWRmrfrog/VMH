import { world, system, ItemStack } from "@minecraft/server";

const blockMap = new Map();
const chargedCreepers = new Map();

const headArray = [
    
];

function runCommand(command) {
    system.run(() => {
        world.getDimension("overworld").runCommand(command);
    });
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

/* 
    Noteblock Functionality
*/

//Redstone power
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

//Noteblock interaction
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

world.beforeEvents.worldInitialize.subscribe(({ blockComponentRegistry }) => {
    blockComponentRegistry.registerCustomComponent("vmh:rotation_comp", RotationBlockComponent);
});

//Creaking Loot
world.beforeEvents.entityRemove.subscribe(({ removedEntity }) => {
    if (removedEntity.typeId === "minecraft:creaking") {
        const {x, y, z} = removedEntity.location;
        const command = `loot spawn ${x} ${y} ${z} loot \"entities/creaking\"`;
        runCommand(command);
    }
})
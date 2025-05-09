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
    ["vmh:aggressive_panda_head", "vmh:aggressive_panda_head_block", "aggressive_panda_head", "mob.panda.idle.aggressive"],
    ["vmh:allay_head", "vmh:allay_head_block", "allay_head", "mob.allay.idle"],
    ["vmh:angry_ashen_wolf_head", "vmh:angry_ashen_wolf_head_block", "angry_ashen_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_bee_head", "vmh:angry_bee_head_block", "angry_bee_head", "mob.bee.hurt"],
    ["vmh:angry_black_wolf_head", "vmh:angry_black_wolf_head_block", "angry_black_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_chestnut_wolf_head", "vmh:angry_chestnut_wolf_head_block", "angry_chestnut_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_pale_wolf_head", "vmh:angry_pale_wolf_head_block", "angry_pale_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_rusty_wolf_head", "vmh:angry_rusty_wolf_head_block", "angry_rusty_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_snowy_wolf_head", "vmh:angry_snowy_wolf_head_block", "angry_snowy_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_spotted_wolf_head", "vmh:angry_spotted_wolf_head_block", "angry_spotted_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_striped_wolf_head", "vmh:angry_striped_wolf_head_block", "angry_striped_wolf_head", "mob.wolf.growl"],
    ["vmh:angry_woods_wolf_head", "vmh:angry_woods_wolf_head_block", "angry_woods_wolf_head", "mob.wolf.growl"],
    ["vmh:arctic_fox_head", "vmh:arctic_fox_head_block", "arctic_fox_head", "mob.fox.ambient"],
    ["vmh:armadillo_head", "vmh:armadillo_head_block", "armadillo_head", "mob.armadillo.ambient"],
    ["vmh:ashen_wolf_head", "vmh:ashen_wolf_head_block", "ashen_wolf_head", "mob.wolf.bark"],
    ["vmh:bat_head", "vmh:bat_head_block", "bat_head", "mob.bat.idle"],
    ["vmh:bee_head", "vmh:bee_head_block", "bee_head", "mob.bee.hurt"],
    ["vmh:black_cat_head", "vmh:black_cat_head_block", "black_cat_head", "mob.cat.meow"],
    ["vmh:black_horse_head", "vmh:black_horse_head_block", "black_horse_head", "mob.horse.idle"],
    ["vmh:black_rabbit_head", "vmh:black_rabbit_head_block", "black_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:black_wolf_head", "vmh:black_wolf_head_block", "black_wolf_head", "mob.wolf.bark"],
    ["vmh:blaze_head", "vmh:blaze_head_block", "blaze_head", "mob.blaze.breathe"],
    ["vmh:blue_axolotl_head", "vmh:blue_axolotl_head_block", "blue_axolotl_head", "mob.axolotl.idle"],
    ["vmh:blue_parrot_head", "vmh:blue_parrot_head_block", "blue_parrot_head", "mob.parrot.idle"],
    ["vmh:blue_wither_head", "vmh:blue_wither_head_block", "blue_wither_head", "mob.wither.ambient"],
    ["vmh:blue_wither_projectile_head", "vmh:blue_wither_projectile_head_block", "blue_wither_projectile_head", "mob.wither.shoot"],
    ["vmh:bogged_head", "vmh:bogged_head_block", "bogged_head", "mob.bogged.ambient"],
    ["vmh:breeze_head", "vmh:breeze_head_block", "breeze_head", "mob.breeze.idle_ground"],
    ["vmh:british_cat_head", "vmh:british_cat_head_block", "british_cat_head", "mob.cat.meow"],
    ["vmh:brown_horse_head", "vmh:brown_horse_head_block", "brown_horse_head", "mob.horse.idle"],
    ["vmh:brown_llama_head", "vmh:brown_llama_head_block", "brown_llama_head", "mob.llama.idle"],
    ["vmh:brown_mooshroom_head", "vmh:brown_mooshroom_head_block", "brown_mooshroom_head", "mob.cow.say"],
    ["vmh:brown_panda_head", "vmh:brown_panda_head_block", "brown_panda_head", "mob.panda.idle"],
    ["vmh:brown_rabbit_head", "vmh:brown_rabbit_head_block", "brown_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:calico_cat_head", "vmh:calico_cat_head_block", "calico_cat_head", "mob.cat.meow"],
    ["vmh:camel_head", "vmh:camel_head_block", "camel_head", "mob.camel.ambient"],
    ["vmh:cave_spider_head", "vmh:cave_spider_head_block", "cave_spider_head", "mob.spider.say"],
    ["vmh:chestnut_horse_head", "vmh:chestnut_horse_head_block", "chestnut_horse_head", "mob.horse.idle"],
    ["vmh:chestnut_wolf_head", "vmh:chestnut_wolf_head_block", "chestnut_wolf_head", "mob.wolf.bark"],
    ["vmh:chicken_head", "vmh:chicken_head_block", "chicken_head", "mob.chicken.say"],
    ["vmh:cod_head", "vmh:cod_head_block", "cod_head", "mob.fish.flop"],
    ["vmh:cold_chicken_head", "vmh:cold_chicken_head_block", "cold_chicken_head", "mob.chicken.say"],
    ["vmh:cold_cow_head", "vmh:cold_cow_head_block", "cold_cow_head", "mob.cow.say"],
    ["vmh:cold_frog_head", "vmh:cold_frog_head_block", "cold_frog_head", "mob.frog.ambient"],
    ["vmh:cold_pig_head", "vmh:cold_pig_head_block", "cold_pig_head", "mob.pig.say"],
    ["vmh:cow_head", "vmh:cow_head_block", "cow_head", "mob.cow.say"],
    ["vmh:creaking_head", "vmh:creaking_head_block", "creaking_head", "mob.creaking.ambient"],
    ["vmh:creamy_horse_head", "vmh:creamy_horse_head_block", "creamy_horse_head", "mob.horse.idle"],
    ["vmh:creamy_llama_head", "vmh:creamy_llama_head_block", "creamy_llama_head", "mob.llama.idle"],
    ["vmh:cyan_axolotl_head", "vmh:cyan_axolotl_head_block", "cyan_axolotl_head", "mob.axolotl.idle"],
    ["vmh:cyan_parrot_head", "vmh:cyan_parrot_head_block", "cyan_parrot_head", "mob.parrot.idle"],
    ["vmh:dark_brown_horse_head", "vmh:dark_brown_horse_head_block", "dark_brown_horse_head", "mob.horse.idle"],
    ["vmh:desert_rabbit_head", "vmh:desert_rabbit_head_block", "desert_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:dolphin_head", "vmh:dolphin_head_block", "dolphin_head", "mob.dolphin.idle"],
    ["vmh:donkey_head", "vmh:donkey_head_block", "donkey_head", "mob.horse.donkey.idle"],
    ["vmh:drowned_head", "vmh:drowned_head_block", "drowned_head", "mob.drowned.say"],
    ["vmh:elder_guardian_head", "vmh:elder_guardian_head_block", "elder_guardian_head", "mob.elderguardian.curse"],
    ["vmh:enderman_head", "vmh:enderman_head_block", "enderman_head", "mob.endermen.idle"],
    ["vmh:endermite_head", "vmh:endermite_head_block", "endermite_head", "mob.endermite.say"],
    ["vmh:evoker_head", "vmh:evoker_head_block", "evoker_head", "mob.evocation_illager.prepare_wololo"],
    ["vmh:fox_head", "vmh:fox_head_block", "fox_head", "mob.fox.ambient"],
    ["vmh:ghast_head", "vmh:ghast_head_block", "ghast_head", "mob.ghast.moan"],
    ["vmh:glow_squid_head", "vmh:glow_squid_head_block", "glow_squid_head", "mob.glow_squid.ambient"],
    ["vmh:goat_head", "vmh:goat_head_block", "goat_head", "mob.goat.ambient"],
    ["vmh:gold_axolotl_head", "vmh:gold_axolotl_head_block", "gold_axolotl_head", "mob.axolotl.idle"],
    ["vmh:gray_horse_head", "vmh:gray_horse_head_block", "gray_horse_head", "mob.horse.idle"],
    ["vmh:gray_llama_head", "vmh:gray_llama_head_block", "gray_llama_head", "mob.llama.idle"],
    ["vmh:gray_parrot_head", "vmh:gray_parrot_head_block", "gray_parrot_head", "mob.parrot.idle"],
    ["vmh:green_parrot_head", "vmh:green_parrot_head_block", "green_parrot_head", "mob.parrot.idle"],
    ["vmh:guardian_head", "vmh:guardian_head_block", "guardian_head", "mob.guardian.ambient"],
    ["vmh:hoglin_head", "vmh:hoglin_head_block", "hoglin_head", "mob.hoglin.ambient"],
    ["vmh:husk_head", "vmh:husk_head_block", "husk_head", "mob.husk.ambient"],
    ["vmh:iron_golem_head", "vmh:iron_golem_head_block", "iron_golem_head", "mob.irongolem.hit"],
    ["vmh:jellie_cat_head", "vmh:jellie_cat_head_block", "jellie_cat_head", "mob.cat.meow"],
    ["vmh:lazy_panda_head", "vmh:lazy_panda_head_block", "lazy_panda_head", "mob.panda.idle"],
    ["vmh:lucy_axolotl_head", "vmh:lucy_axolotl_head_block", "lucy_axolotl_head", "mob.axolotl.idle"],
    ["vmh:magma_cube_head", "vmh:magma_cube_head_block", "magma_cube_head", "mob.magmacube.jump"],
    ["vmh:mooshroom_head", "vmh:mooshroom_head_block", "mooshroom_head", "mob.cow.say"],
    ["vmh:mule_head", "vmh:mule_head_block", "mule_head", "mob.horse.donkey.idle"],
    ["vmh:ocelot_head", "vmh:ocelot_head_block", "ocelot_head", "mob.ocelot.idle"],
    ["vmh:pale_wolf_head", "vmh:pale_wolf_head_block", "pale_wolf_head", "mob.wolf.bark"],
    ["vmh:panda_head", "vmh:panda_head_block", "panda_head", "mob.panda.idle"],
    ["vmh:persian_cat_head", "vmh:persian_cat_head_block", "persian_cat_head", "mob.cat.meow"],
    ["vmh:phantom_head", "vmh:phantom_head_block", "phantom_head", "mob.phantom.idle"],
    ["vmh:pig_head", "vmh:pig_head_block", "pig_head", "mob.pig.say"],
    ["vmh:piglin_brute_head", "vmh:piglin_brute_head_block", "piglin_brute_head", "mob.piglin_brute.ambient"],
    ["vmh:pillager_head", "vmh:pillager_head_block", "pillager_head", "mob.pillager.idle"],
    ["vmh:playful_panda_head", "vmh:playful_panda_head_block", "playful_panda_head", "mob.panda.idle"],
    ["vmh:polar_bear_head", "vmh:polar_bear_head_block", "polar_bear_head", "mob.polarbear.idle"],
    ["vmh:pufferfish_head", "vmh:pufferfish_head_block", "pufferfish_head", "mob.fish.flop"],
    ["vmh:ragdoll_cat_head", "vmh:ragdoll_cat_head_block", "ragdoll_cat_head", "mob.cat.meow"],
    ["vmh:ravager_head", "vmh:ravager_head_block", "ravager_head", "mob.ravager.ambient"],
    ["vmh:red_cat_head", "vmh:red_cat_head_block", "red_cat_head", "mob.cat.meow"],
    ["vmh:red_parrot_head", "vmh:red_parrot_head_block", "red_parrot_head", "mob.parrot.idle"],
    ["vmh:rusty_wolf_head", "vmh:rusty_wolf_head_block", "rusty_wolf_head", "mob.wolf.bark"],
    ["vmh:salmon_head", "vmh:salmon_head_block", "salmon_head", "mob.fish.flop"],
    ["vmh:salt_rabbit_head", "vmh:salt_rabbit_head_block", "salt_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:sheep_head", "vmh:sheep_head_block", "sheep_head", "mob.sheep.say"],
    ["vmh:shulker_head", "vmh:shulker_head_block", "shulker_head", "mob.shulker.ambient"],
    ["vmh:siamese_cat_head", "vmh:siamese_cat_head_block", "siamese_cat_head", "mob.cat.meow"],
    ["vmh:silverfish_head", "vmh:silverfish_head_block", "silverfish_head", "mob.silverfish.say"],
    ["vmh:skeleton_horse_head", "vmh:skeleton_horse_head_block", "skeleton_horse_head", "mob.horse.skeleton.idle"],
    ["vmh:slime_head", "vmh:slime_head_block", "slime_head", "mob.slime.jump"],
    ["vmh:sniffer_head", "vmh:sniffer_head_block", "sniffer_head", "mob.sniffer.idle"],
    ["vmh:snow_golem_head", "vmh:snow_golem_head_block", "snow_golem_head", "mob.snowgolem.hurt"],
    ["vmh:snowy_wolf_head", "vmh:snowy_wolf_head_block", "snowy_wolf_head", "mob.wolf.bark"],
    ["vmh:spider_head", "vmh:spider_head_block", "spider_head", "mob.spider.say"],
    ["vmh:splotched_rabbit_head", "vmh:splotched_rabbit_head_block", "splotched_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:spotted_wolf_head", "vmh:spotted_wolf_head_block", "spotted_wolf_head", "mob.wolf.bark"],
    ["vmh:squid_head", "vmh:squid_head_block", "squid_head", "mob.squid.ambient"],
    ["vmh:stray_head", "vmh:stray_head_block", "stray_head", "mob.stray.ambient"],
    ["vmh:strider_head", "vmh:strider_head_block", "strider_head", "mob.strider.idle"],
    ["vmh:striped_wolf_head", "vmh:striped_wolf_head_block", "striped_wolf_head", "mob.wolf.bark"],
    ["vmh:suffocated_strider_head", "vmh:suffocated_strider_head_block", "suffocated_strider_head", "mob.strider.idle"],
    ["vmh:tabby_cat_head", "vmh:tabby_cat_head_block", "tabby_cat_head", "mob.cat.meow"],
    ["vmh:tadpole_head", "vmh:tadpole_head_block", "tadpole_head", "mob.tadpole.hurt"],
    ["vmh:temperate_frog_head", "vmh:temperate_frog_head_block", "temperate_frog_head", "mob.frog.ambient"],
    ["vmh:tropical_fish_head", "vmh:tropical_fish_head_block", "tropical_fish_head", "mob.fish.flop"],
    ["vmh:turtle_head", "vmh:turtle_head_block", "turtle_head", "mob.turtle.ambient"],
    ["vmh:tuxedo_cat_head", "vmh:tuxedo_cat_head_block", "tuxedo_cat_head", "mob.cat.meow"],
    ["vmh:vex_head", "vmh:vex_head_block", "vex_head", "mob.vex.charge"],
    ["vmh:villager_head", "vmh:villager_head_block", "villager_head", "mob.villager.idle"],
    ["vmh:vindicator_head", "vmh:vindicator_head_block", "vindicator_head", "mob.vindicator.idle"],
    ["vmh:wandering_trader_head", "vmh:wandering_trader_head_block", "wandering_trader_head", "mob.wanderingtrader.idle"],
    ["vmh:warden_head", "vmh:warden_head_block", "warden_head", "mob.warden.idle"],
    ["vmh:warm_chicken_head", "vmh:warm_chicken_head_block", "warm_chicken_head", "mob.chicken.say"],
    ["vmh:warm_cow_head", "vmh:warm_cow_head_block", "warm_cow_head", "mob.cow.say"],
    ["vmh:warm_frog_head", "vmh:warm_frog_head_block", "warm_frog_head", "mob.frog.ambient"],
    ["vmh:warm_pig_head", "vmh:warm_pig_head_block", "warm_pig_head", "mob.pig.say"],
    ["vmh:weak_panda_head", "vmh:weak_panda_head_block", "weak_panda_head", "mob.panda.sneeze"],
    ["vmh:white_cat_head", "vmh:white_cat_head_block", "white_cat_head", "mob.cat.meow"],
    ["vmh:white_horse_head", "vmh:white_horse_head_block", "white_horse_head", "mob.horse.idle"],
    ["vmh:white_llama_head", "vmh:white_llama_head_block", "white_llama_head", "mob.llama.idle"],
    ["vmh:white_rabbit_head", "vmh:white_rabbit_head_block", "white_rabbit_head", "mob.rabbit.hurt"],
    ["vmh:wild_axolotl_head", "vmh:wild_axolotl_head_block", "wild_axolotl_head", "mob.axolotl.idle"],
    ["vmh:witch_head", "vmh:witch_head_block", "witch_head", "mob.witch.ambient"],
    ["vmh:wither_head", "vmh:wither_head_block", "wither_head", "mob.wither.ambient"],
    ["vmh:wither_projectile_head", "vmh:wither_projectile_head_block", "wither_projectile_head", "mob.wither.shoot"],
    ["vmh:woods_wolf_head", "vmh:woods_wolf_head_block", "woods_wolf_head", "mob.wolf.bark"],
    ["vmh:worried_panda_head", "vmh:worried_panda_head_block", "worried_panda_head", "mob.panda.idle.worried"],
    ["vmh:zoglin_head", "vmh:zoglin_head_block", "zoglin_head", "mob.zoglin.idle"],
    ["vmh:zombie_villager_head", "vmh:zombie_villager_head_block", "zombie_villager_head", "mob.zombie_villager.say"],
    ["vmh:zombified_piglin_head", "vmh:zombified_piglin_head_block", "zombified_piglin_head", "mob.zombiepig.zpig"]
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

        console.warn(`${command}`);
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
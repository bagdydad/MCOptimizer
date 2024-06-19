import os
import yaml
from time import sleep

os.system('@echo off')
os.system('title ' + 'MCSO v1.2 - oTuin')
os.system('cls')

print('!WARNING! If you do not know what this application does, do not run it on your server!')
print('!WARNING! You should know that WE ARE NOT RESPONSIBLE FOR ANY PROBLEMS!')
print('!WARNING! There will never be a guide that will give you perfect results. Each server has their own needs and '
      'limits on how much you can or are willing to sacrifice. Tinkering around with the options to fine tune them to '
      'your servers needs is what it is all about. This guide only aims to help you understand what options have '
      'impact on performance and what exactly they change. If you think you found inaccurate information within this '
      'guide, you are free to open an issue or set up a pull request to correct it.')
print('!WARNING! If you want to see whats will change to your server and set the option yourself you can access guide '
      'from this link: https://github.com/YouHaveTrouble/minecraft-optimization')
print('!WARNING! This application may contain some different regulations other than the guide, use it at your own risk!')
print('!WARNING! MAKE SURE YOU HAVE GET A BACKUP OF YOUR SERVER BEFORE RUNNING THIS!')
input('!WARNING! Press Enter to continue...')
print('!WARNING! Ok! Well you know.')
sleep(3)
os.system('cls')
print('Starting minecraft server optimization...')
sleep(3)


def log(text):
    print(text)
    with open('optimizer.log', 'a') as f:
        f.write(text + "\n")


def error_log(text):
    print(text)
    with open('optimizer_changes.log', 'a') as f:
        f.write(text + "\n")


def change_yaml_value(file, keys, value):
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
        keys = keys.split('.')
        current = data
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        if keys[-1] not in current:
            error_log('[\'' + file + '\']' + str(keys) + ' -> ' + str(value) + ' (New key added!)')
        else:
            log('[\'' + file + '\']' + str(keys) + ' -> ' + str(value))
        current[keys[-1]] = value
        with open(file, 'w') as f:
            yaml.dump(data, f)
    except Exception as e:
        error_log(str(e) + ' not found!')


def change_property_value(file, keys, value):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        key_parts = keys.split('.')
        for i, line in enumerate(lines):
            if line.startswith(key_parts[0]):
                parts = line.split('=')
                if parts[0] == keys:
                    lines[i] = f'{keys}={value}\n'
                    log('[\'' + file + '\']' + str(keys) + ' -> ' + str(value))
                    break
                elif len(key_parts) > 1:
                    sub_dict = parts[1].strip()
                    sub_file = os.path.join(os.path.dirname(file), f'{sub_dict}.yml')
                    if os.path.exists(sub_file):
                        change_property_value(sub_file, '.'.join(key_parts[1:]), value)
                        break
                    else:
                        error_log(f'Sub-dictionary file {sub_file} not found.')
                        raise ValueError(f'Sub-dictionary file {sub_file} not found.')
        with open(file, 'w') as f:
            f.writelines(lines)
    except Exception as e:
        error_log(str(e) + ' not found!')


if os.path.isfile('server.properties'):
    print('Settings are being optimized... (server.properties)')
    change_property_value('server.properties', 'sync-chunk-writes', False)
    change_property_value('server.properties', 'network-compression-threshold', 256)
    change_property_value('server.properties', 'simulation-distance', 4)
    change_property_value('server.properties', 'view-distance', 7)
    #change_property_value('server.properties', 'entity-broadcast-range-percentage', 50)
else:
    error_log('server.properties not found!')

if os.path.isfile('bukkit.yml'):
    print('Settings are being optimized... (bukkit.yml)')
    change_yaml_value('bukkit.yml', 'spawn-limits.monsters', 20)
    change_yaml_value('bukkit.yml', 'spawn-limits.animals', 5)
    change_yaml_value('bukkit.yml', 'spawn-limits.water-animals', 2)
    change_yaml_value('bukkit.yml', 'spawn-limits.water-ambient', 2)
    change_yaml_value('bukkit.yml', 'spawn-limits.water-underground-creature', 3)
    change_yaml_value('bukkit.yml', 'spawn-limits.axolotls', 3)
    change_yaml_value('bukkit.yml', 'spawn-limits.ambient', 1)
    change_yaml_value('bukkit.yml', 'ticks-per.monster-spawns', 10)
    change_yaml_value('bukkit.yml', 'ticks-per.animal-spawns', 400)
    change_yaml_value('bukkit.yml', 'ticks-per.water-spawns', 400)
    change_yaml_value('bukkit.yml', 'ticks-per.water-ambient-spawns', 400)
    change_yaml_value('bukkit.yml', 'ticks-per.water-underground-creature-spawns', 400)
    change_yaml_value('bukkit.yml', 'ticks-per.axolotl-spawns', 400)
    change_yaml_value('bukkit.yml', 'ticks-per.ambient-spawns', 400)
else:
    error_log('bukkit.yml not found!')

if os.path.isfile('spigot.yml'):
    print('Settings are being optimized... (spigot.yml)')
    change_yaml_value('spigot.yml', 'world-settings.default.view-distance', 'default')
    change_yaml_value('spigot.yml', 'world-settings.default.mob-spawn-range', 3)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.animals', 16)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.monsters', 24)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.raiders', 48)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.misc', 8)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.water', 8)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.villagers', 16)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.flying-monsters', 48)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-activation-range.tick-inactive-villagers', False)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-tracking-range.players', 48)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-tracking-range.animals', 48)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-tracking-range.monsters', 48)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-tracking-range.misc', 32)
    change_yaml_value('spigot.yml', 'world-settings.default.entity-tracking-range.other', 64)
    #change_yaml_value('spigot.yml', 'world-settings.default.nerf-spawner-mobs', True)
    change_yaml_value('spigot.yml', 'world-settings.default.merge-radius.item', 3.5)
    change_yaml_value('spigot.yml', 'world-settings.default.merge-radius.exp', 4.0)
    #change_yaml_value('spigot.yml', 'world-settings.default.ticks-per.hopper-check', 8)
    change_yaml_value('spigot.yml', 'world-settings.default.ticks-per.hopper-transfer', 8)
    change_yaml_value('spigot.yml', 'world-settings.default.hopper-can-load-chunks', False)
else:
    error_log('spigot.yml not found!')

if os.path.isfile('config/paper-world-defaults.yml'):
    print('Settings are being optimized... (config/paper-world-defaults.yml)')
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.delay-chunk-unloads-by', '10s')
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.max-auto-save-chunks-per-tick', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.prevent-moving-into-unloaded-chunks', True)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.area_effect_cloud', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.arrow', 16)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.dragon_fireball', 3)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.egg', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.ender_pearl', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.experience_bottle', 3)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.experience_orb', 16)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.eye_of_ender', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.fireball', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.firework_rocket', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.llama_spit', 3)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.potion', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.shulker_bullet', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.small_fireball', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.snowball', 8)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.spectral_arrow', 16)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.trident', 16)
    change_yaml_value('config/paper-world-defaults.yml', 'chunks.entity-per-chunk-save-limit.wither_skull', 4)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.behavior.spawner-nerfed-mobs-should-jump', True)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.ambient.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.ambient.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.axolotls.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.axolotls.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.creature.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.creature.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.misc.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.misc.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.monster.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.monster.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.underground_water_creature.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.underground_water_creature.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.water_ambient.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.water_ambient.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.water_creature.hard', 90)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.despawn-ranges.water_creature.soft', 30)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.per-player-mob-spawns', True)
    change_yaml_value('config/paper-world-defaults.yml', 'collisions.max-entity-collisions', 2)
    change_yaml_value('config/paper-world-defaults.yml', 'misc.update-pathfinding-on-block-update', False)
    change_yaml_value('config/paper-world-defaults.yml', 'collisions.fix-climbing-bypassing-cramming-rule', True)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.armor-stands.do-collision-entity-lookups', False)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.armor-stands.tick', False)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.enabled', True)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.cobblestone', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.netherrack', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.sand', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.red_sand', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.gravel', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.dirt', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.grass_block', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.pumpkin', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.melon_slice', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.kelp', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.bamboo', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.sugar_cane', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.twisting_vines', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.weeping_vines', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.oak_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.spruce_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.birch_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.jungle_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.acacia_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.dark_oak_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.mangrove_leaves', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.cactus', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.diorite', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.granite', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.andesite', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.scaffolding', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.basalt', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.blackstone', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.magma_block', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.tuff', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.deepslate', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.alt-item-despawn-rate.items.pointed_dripstone', 600)
    change_yaml_value('config/paper-world-defaults.yml', 'misc.redstone-implementation', 'ALTERNATE_CURRENT')
    #change_yaml_value('config/paper-world-defaults.yml', 'hopper.disable-move-event', True)
    change_yaml_value('config/paper-world-defaults.yml', 'hopper.cooldown-when-full', True)
    change_yaml_value('config/paper-world-defaults.yml', 'hopper.ignore-occluding-blocks', True)
    change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.mob-spawner', 2)
    change_yaml_value('config/paper-world-defaults.yml', 'environment.optimize-explosions', True)
    change_yaml_value('config/paper-world-defaults.yml', 'environment.treasure-maps.enabled', False)
    change_yaml_value('config/paper-world-defaults.yml', 'environment.treasure-maps.find-already-discovered.loot-tables', True)
    change_yaml_value('config/paper-world-defaults.yml', 'environment.treasure-maps.find-already-discovered.villager-trade', True)
    change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.grass-spread', 4)
    change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.container-update', 1)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.non-player-arrow-despawn-rate', 20)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.spawning.creative-arrow-despawn-rate', 20)
    change_yaml_value('config/paper-world-defaults.yml', 'environment.nether-ceiling-void-damage-height', 127)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.behavior.allow-spider-world-border-climbing', False)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.behavior.disable-chest-cat-detection', True)
    change_yaml_value('config/paper-world-defaults.yml', 'entities.behavior.parrots-are-unaffected-by-player-movement', True)
    change_yaml_value('config/paper-world-defaults.yml', 'feature-seeds.generate-random-seeds-for-all', True)
    #change_yaml_value('config/paper-world-defaults.yml', 'fixes.fix-items-merging-through-walls', True)

    res = ''
    hiddenBlocks = [
        'copper_ore', 'deepslate_copper_ore', 'raw_copper_block',
        'diamond_ore', 'deepslate_diamond_ore', 'gold_ore',
        'deepslate_gold_ore', 'iron_ore', 'deepslate_iron_ore',
        'raw_iron_block', 'lapis_ore', 'deepslate_lapis_ore',
        'redstone_ore', 'deepslate_redstone_ore'
    ]

    print('[AntiXRay-World] Should the air block be hidden? (It may cause fps loss for players with low system.)')
    while True:
        res = input('Please type yes/y or no/n: ').lower()

        if res in ['y', 'e', 'yes', 'evet']:
            hiddenBlocks.append('air')
            break
        elif res in ['n', 'h', 'no', 'hayır', 'hayir']:
            break
        else:
            print('Invalid input. Please type yes/y or no/n.')

    replacementBlocks = [
        'chest', 'amethyst_block', 'andesite', 'budding_amethyst', 'calcite',
        'coal_ore', 'deepslate_coal_ore', 'deepslate', 'diorite', 'dirt',
        'emerald_ore', 'deepslate_emerald_ore', 'granite', 'gravel',
        'oak_planks', 'smooth_basalt', 'stone', 'tuff'
    ]

    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.enabled', True)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.engine-mode', 2)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.hidden-blocks', hiddenBlocks)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.lava-obscures', True)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.max-block-height', 256)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.replacement-blocks', replacementBlocks)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.update-radius', 2)
    change_yaml_value('config/paper-world-defaults.yml', 'anticheat.anti-xray.use-permission', False)
else:
    error_log('config/paper-world-defaults.yml not found!')

if os.path.isfile('world_nether/paper-world.yml'):
    print('Settings are being optimized... (world_nether/paper-world.yml)')

    res = ''
    hiddenBlocks = [
        'ancient_debris', 'bone_block', 'glowstone',
        'magma_block', 'nether_bricks', 'nether_gold_ore',
        'nether_quartz_ore', 'polished_blackstone_bricks'
    ]

    print('[AntiXRay-Nether] Should the air block be hidden? (It may cause fps loss for players with low system.)')
    while True:
        res = input('Please type yes/y or no/n: ').lower()

        if res in ['y', 'e', 'yes', 'evet']:
            hiddenBlocks.append('air')
            break
        elif res in ['n', 'h', 'no', 'hayır', 'hayir']:
            break
        else:
            print('Invalid input. Please type yes/y or no/n.')

    replacementBlocks = [
        'basalt', 'blackstone', 'gravel', 'netherrack',
        'soul_sand', 'soul_soil'
    ]

    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.enabled', True)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.engine-mode', 2)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.hidden-blocks', hiddenBlocks)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.lava-obscures', True)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.max-block-height', 128)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.replacement-blocks', replacementBlocks)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.update-radius', 2)
    change_yaml_value('world_nether/paper-world.yml', 'anticheat.anti-xray.use-permission', False)
else:
    error_log('world_nether/paper-world.yml not found!')

if os.path.isfile('world_the_end/paper-world.yml'):
    print('Settings are being optimized... (world_the_end/paper-world.yml)')
    change_yaml_value('world_the_end/paper-world.yml', 'anticheat.anti-xray.enabled', False)
else:
    error_log('world_the_end/paper-world.yml not found!')

if os.path.isfile('pufferfish.yml'):
    print('Settings are being optimized... (pufferfish.yml)')
    change_yaml_value('pufferfish.yml', 'dab.enabled', True)
    change_yaml_value('pufferfish.yml', 'dab.max-tick-freq', 20)
    change_yaml_value('pufferfish.yml', 'dab.activation-dist-mod', 7)
    change_yaml_value('pufferfish.yml', 'enable-async-mob-spawning', True)
    change_yaml_value('pufferfish.yml', 'enable-suffocation-optimization', True)
    change_yaml_value('pufferfish.yml', 'inactive-goal-selector-throttle', True)
    change_yaml_value('pufferfish.yml', 'projectile.max-loads-per-projectile', 8)
    change_yaml_value('pufferfish.yml', 'misc.disable-method-profiler', True)
else:
    error_log('pufferfish.yml not found!')
    if os.path.isfile('config/paper-world-defaults.yml'):
        print('Settings are being optimized... (config/paper-world-defaults.yml)')
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.behavior.villager.validatenearbypoi', 60)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.behavior.villager.acquirepoi', 120)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.sensor.villager.secondarypoisensor', 80)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.sensor.villager.nearestbedsensor', 80)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.sensor.villager.villagerbabiessensor', 40)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.sensor.villager.playersensor', 40)
        change_yaml_value('config/paper-world-defaults.yml', 'tick-rates.sensor.villager.nearestlivingentitysensor', 40)
    else:
        error_log('config/paper-world-defaults.yml not found!')

if os.path.isfile('purpur.yml'):
    print('Settings are being optimized... (purpur.yml)')
    #change_yaml_value('purpur.yml', 'settings.use-alternate-keepalive', True) # Has known incompatibility with TCPShield.
    change_yaml_value('purpur.yml', 'world-settings.default.mobs.zombie.aggressive-towards-villager-when-lagging', False)
    change_yaml_value('purpur.yml', 'world-settings.default.gameplay-mechanics.entities-can-use-portals', False)
    #change_yaml_value('purpur.yml', 'world-settings.default.mobs.villager.lobotomize.enabled', True)
    change_yaml_value('purpur.yml', 'world-settings.default.mobs.dolphin.disable-treasure-searching', True)
    change_yaml_value('purpur.yml', 'world-settings.default.gameplay-mechanics.player.teleport-if-outside-border', True)
    change_yaml_value('purpur.yml', 'world-settings.default.gameplay-mechanics.player.fix-stuck-in-portal', True)
    change_yaml_value('purpur.yml', 'world-settings.default.mobs.villager.search-radius.acquire-poi', 16)
    change_yaml_value('purpur.yml', 'world-settings.default.mobs.villager.search-radius.nearest-bed-sensor', 16)
else:
    error_log('purpur.yml not found!')

print('Successfully finished. You can find the changes made in the "optimizer.log" and "optimizer_changes.log" files.')
input('Press Enter to exit.')

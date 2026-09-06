ServerEvents.recipes((event) => {
  event.recipes.gtceu
    .macerator('gtceu:obsidian_dust')
    .itemInputs('minecraft:obsidian')
    .itemOutputs('gtceu:obsidian_dust')
    .EUt(2)
    .duration(100)

  if (Platform.isLoaded('extendedae_plus')) {
    event.remove({
      id: 'extendedae_plus:network/crafting/4x_crafting_accelerator',
    })
    event.remove({
      id: 'extendedae_plus:network/crafting/16x_crafting_accelerator',
    })
    event.remove({
      id: 'extendedae_plus:network/crafting/64x_crafting_accelerator',
    })
    event.remove({
      id: 'extendedae_plus:network/crafting/256x_crafting_accelerator',
    })

    event.shaped('extendedae_plus:4x_crafting_accelerator', ['A', 'B', 'A'], {
      A: 'ae2:crafting_accelerator',
      B: 'ae2:cell_component_4k',
    })
    event.shaped('extendedae_plus:16x_crafting_accelerator', ['A', 'B', 'A'], {
      A: 'ae2:crafting_accelerator',
      B: 'ae2:cell_component_16k',
    })
    event.shaped('extendedae_plus:64x_crafting_accelerator', ['A', 'B', 'A'], {
      A: 'ae2:crafting_accelerator',
      B: 'ae2:cell_component_64',
    })
    event.shaped('extendedae_plus:256x_crafting_accelerator', ['A', 'B', 'A'], {
      A: 'ae2:crafting_accelerator',
      B: 'ae2:cell_component_256k',
    })
  }
})

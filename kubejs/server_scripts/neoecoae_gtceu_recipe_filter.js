// Neo ECO provides several GTCEu recipes for its own materials. Keep those,
// but remove only the recipes that duplicate GTCEu's existing material chain.
//
// Do not broaden this to a tag/type-based removal: ECO's unique materials also
// use GTCEu machine recipe types and may consume normal GT materials.
ServerEvents.recipes(event => {
  if (!Platform.isLoaded('neoecoae') || !Platform.isLoaded('gtceu')) return

  const duplicateGtceuRecipes = [
    // #forge:ingots/iron -> neoecoae:iron_dust
    'neoecoae:macerator/iron_dust',
    // #forge:ingots/aluminum -> neoecoae:aluminum_dust
    'neoecoae:macerator/aluminum_dust',
    // #forge:ingots/tungsten -> neoecoae:tungsten_dust
    'neoecoae:macerator/tungsten_dust'
  ]

  duplicateGtceuRecipes.forEach(function(id) {
    event.remove({ id: id })
  })
})

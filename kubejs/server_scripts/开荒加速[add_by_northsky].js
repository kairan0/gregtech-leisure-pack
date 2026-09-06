ServerEvents.recipes((event) => {
  //八个任意原木合成四个箱子
  event.shaped('4x minecraft:chest', ['AAA', 'A A', 'AAA'], {
    A: '#minecraft:logs',
  })

  //两个任意原木合成16个木棍
  event.shapeless('16x minecraft:stick', ['#minecraft:logs', '#minecraft:logs'])

  //高炉熔炼加速：
  event.forEachRecipe({ type: 'minecraft:blasting' }, (recipe) => {
    let input = recipe.originalRecipeIngredients
    let output = recipe.originalRecipeResult
    let input_ids = input[0].getItemIds()
    let oldId = recipe.getId()

    event.remove({ id: recipe.getId() })

    // input.forEach((ing, index) => {
    //   console.log('  items:', ing.getItemIds())
    // })

    let isOre = input_ids.some((id) => id.endsWith('_ore'))

    event
      .blasting(output, input)
      .cookingTime(1)
      .xp(isOre ? 4.5 : 0.5)
      .id(`fastblasting:${oldId.replace(':', '/')}`)
  })

  //熔炉：铁锭->锻铁锭
  event.recipes.minecraft.smelting(
    'gtceu:wrought_iron_ingot',
    Ingredient.of('minecraft:iron_ingot'),
    0.7,
    40,
  )
  //高炉：铁锭->锻铁锭 （高炉温度高，能熔炼东西很合理XD）
  event.recipes.minecraft.blasting(
    'gtceu:wrought_iron_ingot',
    Ingredient.of('minecraft:iron_ingot'),
    0.7,
    1,
  )
  //高炉：青铜粉->青铜锭
  event.recipes.minecraft.blasting(
    'gtceu:bronze_ingot',
    Ingredient.of('gtceu:bronze_dust'),
    0.7,
    1,
  )
  //高炉：青铜粉->青铜锭
  event.recipes.minecraft.blasting(
    'gtceu:coke_oven_brick',
    Ingredient.of('gtceu:compressed_coke_clay'),
    0.7,
    1,
  )
  //高炉：粘土球->砖块
  event.recipes.minecraft.blasting(
    'minecraft:brick',
    Ingredient.of('minecraft:clay_ball'),
    0.3,
    1,
  )
  //高炉：压缩耐火粘土->耐火砖
  event.recipes.minecraft.blasting(
    'gtceu:firebrick',
    Ingredient.of('gtceu:compressed_fireclay'),
    0.3,
    1,
  )
  //高炉：沙子->玻璃
  event.recipes.minecraft.blasting(
    'minecraft:glass',
    Ingredient.of('minecraft:sand'),
    0.3,
    1,
  )

  //合金炉：三个粗铜和一个粗锡->四个青铜锭
  event.recipes.gtceu
    .alloy_smelter('gtceu:bronze_ingot')
    .itemInputs('3x minecraft:raw_copper', 'gtceu:raw_tin')
    .itemOutputs('4x gtceu:bronze_ingot')
    .EUt(16)
    .duration(80)

  //提取机：富集硅岩粉->144mB液态富集硅岩
  event.recipes.gtceu
    .extractor('gtceu:enriched_naquadah')
    .itemInputs('gtceu:enriched_naquadah_dust')
    .outputFluids('gtceu:enriched_naquadah 144')
    .EUt(480)
    .duration(10)
})

// 无限元件
function infinityCell(fluidId) {
  return Item.of('expatternprovider:infinity_cell', {
    record: {
      '#c': 'ae2:f',
      id: fluidId,
    },
    CustomModelData: 1024,
  })
}

ServerEvents.recipes((event) => {
  const BuiltInRegistries = Java.loadClass(
    'net.minecraft.core.registries.BuiltInRegistries',
  )
  const allFluidIds = BuiltInRegistries.FLUID.keySet()

  allFluidIds.forEach((fluidId) => {
    if (!fluidId) return

    const ns = fluidId.namespace
    const path = fluidId.path
    const currentFullId = String(fluidId.toString())

    // 1. 过滤逻辑
    if (path.endsWith('_flowing') || path === 'empty' || ns === 'ad_astra')
      return

    // 检查桶是否存在（作为研究的基础物品）
    let bucketId = `${ns}:${path}_bucket`
    let bucket = Item.of(bucketId)
    if (bucket.isEmpty()) return

    // 2. 注册装配线配方
    event.recipes.gtceu
      .assembly_line(`infinity_cell_${currentFullId.replace(':', '_')}`)
      .itemInputs(
        '4096x #gtceu:circuits/max',
        'gtlcore:cell_component_256m',
        '1024x kubejs:quantum_chromodynamic_charge',
        '1024x kubejs:eternity_catalyst',
        '1024x avaritia:eternal_singularity',
        '1024x kubejs:entangled_singularity',
      )
      .inputFluids(
        Fluid.of(currentFullId, 2147483647),
        'gtceu:eternity 65536',
        'gtceu:infinity 65536',
        'gtceu:miracle 65536',
      )
      .itemOutputs(infinityCell(currentFullId))
      .EUt(GTValues.VA[GTValues.UXV])
      .duration(65536)
      .stationResearch((b) =>
        b
          .researchStack(bucket)
          .dataStack(Item.of('gtceu:data_module'))
          .EUt(GTValues.VA[GTValues.MAX])
          .CWUt(148),
      )
  })
})

// ServerEvents.tags('item', (event) => {
//   event.add('ae2:all_storage_cells', 'kubejs:gt_infinity_cell')
//   event.add('ae2:all_fluid_storage_cells', 'kubejs:gt_infinity_cell')
// })

// 无限元件
// const InfinityCells = [
//   'minecraft:lava',
//   'gtceu:oil_medium',
//   'gtceu:oil_heavy',
//   'gtceu:steam',
//   'gtceu:liquid_helium',
//   'gtceu:sulfuric_acid',
//   'gtceu:hydrochloric_acid',
//   'gtceu:nitric_acid',
// ]

// ServerEvents.recipes((event) => {
//   InfinityCells.forEach((fluid) => {
//     // 构造量子缸NBT
//     let quantumTank = Item.of('gtceu:uiv_quantum_tank', {
//       cache: {
//         isDistinct: 0,
//         lockedFluid: {
//           Amount: 0,
//           FluidName: 'minecraft:empty',
//         },
//         storages: [
//           {
//             p: {
//               Amount: 4096000000,
//               FluidName: fluid,
//             },
//             t: 11,
//           },
//         ],
//       },
//       stored: {
//         Amount: 4096000000,
//         FluidName: fluid,
//       },
//     }).weakNBT() // 使用弱匹配，防止因为多余的 NBT 标签导致合成失效

//     event
//       .shaped(
//         Item.of('expatternprovider:infinity_cell', {
//           record: { '#c': 'ae2:f', id: fluid },
//         }),
//         ['ABA', 'BCB', 'DDD'],
//         {
//           A: 'ae2:quartz_glass',
//           B: quantumTank,
//           C: 'ae2:cell_component_16k',
//           D: 'minecraft:diamond',
//         },
//       )
//       .id(`infinitycell:${fluid.replace(':', '_')}`)
//   })
// })

//// 太无脑了，把下面ban了
// 构造量子缸NBT
// let quantumTank = Item.of('gtceu:uiv_quantum_tank', {
//   cache: {
//     isDistinct: 0,
//     lockedFluid: { Amount: 0, FluidName: 'minecraft:empty' },
//     storages: [
//       {
//         p: { Amount: 4096000000, FluidName: fullId },
//         t: 11,
//       },
//     ],
//   },
//   stored: { Amount: 4096000000, FluidName: fullId },
// }).weakNBT()

// const bucketId = `${ns}:${path}_bucket`

// 注册配方
// event
//   .shaped(
//     Item.of('expatternprovider:infinity_cell', {
//       record: { '#c': 'ae2:f', id: fullId },
//     }),
//     ['ABA', 'BCB', 'DDD'],
//     {
//       A: 'ae2:quartz_glass',
//       B: quantumTank,
//       // B: bucketId,
//       C: 'ae2:cell_component_16k',
//       D: 'minecraft:diamond',
//     },
//   )
//   .id(`infinitycell:${fullId.replace(':', '_').replace('/', '_')}`)
//   })
// })

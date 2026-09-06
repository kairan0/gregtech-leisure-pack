// StartupEvents.modifyCreativeTab('expatternprovider:tab_main', (e) => {
//   const Inf_Fluid = [
//     // 流体
//     'minecraft:lava',
//     'gtceu:oil_medium',
//     'gtceu:oil_heavy',
//     'gtceu:steam',
//     'gtceu:liquid_helium',
//     'gtceu:sulfuric_acid',
//     'gtceu:hydrochloric_acid',
//     'gtceu:nitric_acid',
//   ]

//   Inf_Fluid.forEach((f) => {
//     e.add(
//       Item.of(
//         'expatternprovider:infinity_cell',
//         `{record:{"#c":"ae2:f",id:"${f}"}}`,
//       ),
//     )
//   })

//   // const Inf_Item = [
//   //   // 物品
//   //   'minecraft:deepslate',
//   // ]

//   // Inf_Item.forEach((i) => {
//   //   e.add(
//   //     Item.of(
//   //       'expatternprovider:infinity_cell',
//   //       `{record:{"#c":"ae2:i",id:"${i}"}}`,
//   //     ),
//   //   )
//   // })
// })

// // 1. 在 KJS 6 中使用 Java.loadClass 来引用类
// const BuiltInRegistries = Java.loadClass(
//   'net.minecraft.core.registries.BuiltInRegistries',
// )

// // 2. 获取流体注册表及其 ID 集合
// const fluidRegistry = BuiltInRegistries.FLUID
// const allFluidIds = fluidRegistry.keySet() // 返回 Set<ResourceLocation>

// // 3. 打印到 logs/kubejs/startup.txt
// console.info(`[KJS] 扫描到流体总数: ${allFluidIds.size()}`)

ForgeEvents.onEvent(
  'net.minecraftforge.event.entity.player.ItemTooltipEvent',
  (event) => {
    const itemStack = event.getItemStack()

    // 1. 基础检查
    if (itemStack.id != 'expatternprovider:infinity_cell') return

    // 2. 获取 NBT 数据
    let nbt = itemStack.nbt
    if (nbt && nbt.record && nbt.record.id) {
      let fluidId = nbt.record.id.toString()

      let rawName = fluidId.split(':')[1] || 'Unknown'
      let displayName = rawName.replace(/_/g, ' ').toUpperCase()

      // 3. 字体布局优化
      event.getToolTip().add(Component.literal('§b§l“ 万 籁 此 俱 寂 ”'))
      event.getToolTip().add(Component.literal('§8' + '—'.repeat(12)))
      event
        .getToolTip()
        .add(Component.literal('§7▶ 存储内容: §f' + displayName))

      // 4. 特殊彩蛋 (如果是格雷流体)
      if (fluidId.includes('gtceu')) {
        event.getToolTip().add(Component.literal('§d§o“ 但 余 钟 磬 音 ”'))
        event
          .getToolTip()
          .add(Component.literal('§c§l[ 宇宙大爆炸时遗留的产物... ]'))
      }
    }
  },
)

function infinityCell(fluidId) {
  return Item.of('expatternprovider:infinity_cell', {
    record: {
      '#c': 'ae2:f',
      id: fluidId,
    },
    CustomModelData: 1024,
  })
}

StartupEvents.modifyCreativeTab('expatternprovider:tab_main', (e) => {
  const BuiltInRegistries = Java.loadClass(
    'net.minecraft.core.registries.BuiltInRegistries',
  )
  const allFluidIds = BuiltInRegistries.FLUID.keySet()
  // console.info(`[KJS] 原始流体总数: ${allFluidIds.size()}`)

  allFluidIds.forEach((fluidId) => {
    const ns = fluidId.namespace
    const path = fluidId.path
    const fullId = fluidId.toString()

    // 1. 基础过滤：排除流动、空流体，以及与 Server 脚本同步过滤 ad_astra
    if (path.endsWith('_flowing') || path === 'empty' || ns === 'ad_astra')
      return

    // 2. 进阶过滤：只有具备“桶”形态的流体才会被添加
    // 使用变量拼接时，确保它是字符串
    let bucket = Item.of(`${ns}:${path}_bucket`)
    if (bucket.isEmpty()) return

    // 3. 添加到创造栏
    e.add(infinityCell(fullId))
  })
})

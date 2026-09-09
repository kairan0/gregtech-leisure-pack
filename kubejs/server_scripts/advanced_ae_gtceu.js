// Add GTCEu machine routes for AdvancedAE without replacing its native recipes.
// Recipe quantities follow AdvancedAE 1.3.5; GT tiers, durations and solder are
// pack-side balancing choices for GregTech Leisure.
ServerEvents.recipes(event => {
  if (!Platform.isLoaded('advanced_ae') || !Platform.isLoaded('gtceu')) return

  const gtr = event.recipes.gtceu
  const HV = 480
  const EV = 1920
  const IV = 7680

  // Core material and processor chain.
  gtr.mixer('gtl_compat:advanced_ae/mixer/shattered_singularity')
    .itemInputs('ae2:singularity', '2x #forge:dusts/ender_pearl', '2x ae2:sky_dust')
    .inputFluids('minecraft:lava 100')
    .itemOutputs('2x advanced_ae:shattered_singularity')
    .duration(400)
    .EUt(HV)

  gtr.macerator('gtl_compat:advanced_ae/macerator/quantum_infused_dust')
    .itemInputs('advanced_ae:shattered_singularity')
    .itemOutputs('advanced_ae:quantum_infused_dust')
    .duration(100)
    .EUt(HV)

  gtr.chemical_reactor('gtl_compat:advanced_ae/chemical_reactor/quantum_infusion_source')
    .itemInputs('advanced_ae:quantum_infused_dust')
    .inputFluids('minecraft:water 4000')
    .outputFluids('advanced_ae:quantum_infusion_source 1000')
    .duration(40)
    .EUt(HV)

  gtr.mixer('gtl_compat:advanced_ae/mixer/quantum_alloy')
    .itemInputs('4x #forge:ingots/copper', '4x advanced_ae:shattered_singularity', '4x ae2:singularity')
    .inputFluids('advanced_ae:quantum_infusion_source 1000')
    .itemOutputs('advanced_ae:quantum_alloy')
    .duration(100)
    .EUt(EV)

  // Deliberately preserve the native 8:1 alloy-to-plate ratio.
  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_alloy_plate')
    .itemInputs('8x advanced_ae:quantum_alloy', '2x #forge:ingots/netherite', 'minecraft:nether_star')
    .inputFluids('advanced_ae:quantum_infusion_source 1000')
    .itemOutputs('advanced_ae:quantum_alloy_plate')
    .duration(500)
    .EUt(EV)

  gtr.forming_press('gtl_compat:advanced_ae/forming_press/quantum_processor_press')
    .notConsumable('ae2:logic_processor_press')
    .notConsumable('ae2:engineering_processor_press')
    .itemInputs('advanced_ae:shattered_singularity')
    .itemOutputs('advanced_ae:quantum_processor_press')
    .duration(200)
    .EUt(HV)

  gtr.forming_press('gtl_compat:advanced_ae/forming_press/printed_quantum_processor')
    .notConsumable('advanced_ae:quantum_processor_press')
    .itemInputs('advanced_ae:quantum_alloy')
    .itemOutputs('advanced_ae:printed_quantum_processor')
    .duration(200)
    .EUt(HV)

  gtr.forming_press('gtl_compat:advanced_ae/forming_press/quantum_processor')
    .itemInputs('advanced_ae:printed_quantum_processor', 'ae2:printed_silicon', '#forge:dusts/redstone')
    .itemOutputs('advanced_ae:quantum_processor')
    .duration(200)
    .EUt(HV)

  // AE network devices.
  gtr.assembler('gtl_compat:advanced_ae/assembler/reaction_chamber')
    .itemInputs('4x ae2:fluix_dust', 'ae2:condenser', 'ae2:vibration_chamber', 'minecraft:bucket', '#forge:dusts/glowstone')
    .inputFluids('gtceu:soldering_alloy 144')
    .itemOutputs('advanced_ae:reaction_chamber')
    .duration(200)
    .EUt(HV)

  if (Platform.isLoaded('expatternprovider')) {
    gtr.assembler('gtl_compat:advanced_ae/assembler/advanced_pattern_provider')
      .itemInputs('expatternprovider:ex_pattern_provider', '#forge:dusts/redstone', 'minecraft:ender_pearl', 'ae2:logic_processor')
      .inputFluids('gtceu:soldering_alloy 144')
      .itemOutputs('advanced_ae:adv_pattern_provider')
      .duration(200)
      .EUt(HV)
  }

  gtr.assembler('gtl_compat:advanced_ae/assembler/small_advanced_pattern_provider')
    .itemInputs('ae2:pattern_provider', '#forge:dusts/redstone', 'minecraft:ender_pearl', 'ae2:logic_processor')
    .inputFluids('gtceu:soldering_alloy 72')
    .itemOutputs('advanced_ae:small_adv_pattern_provider')
    .duration(100)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/advanced_pattern_encoder')
    .itemInputs('4x ae2:charged_certus_quartz_crystal', '4x #forge:dusts/redstone', 'ae2:engineering_processor')
    .inputFluids('gtceu:soldering_alloy 144')
    .itemOutputs('advanced_ae:adv_pattern_encoder')
    .duration(200)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/pattern_provider_upgrade')
    .itemInputs('#forge:ingots/iron', '#forge:dusts/redstone', 'minecraft:ender_pearl', 'ae2:logic_processor')
    .inputFluids('gtceu:soldering_alloy 72')
    .itemOutputs('advanced_ae:adv_pattern_provider_upgrade')
    .duration(100)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/pattern_provider_capacity_upgrade')
    .itemInputs('#forge:ingots/iron', '2x ae2:capacity_card', 'ae2:engineering_processor')
    .inputFluids('gtceu:soldering_alloy 144')
    .itemOutputs('advanced_ae:adv_pattern_provider_capacity_upgrade')
    .duration(200)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/import_export_bus')
    .itemInputs('ae2:import_bus', 'ae2:logic_processor', 'ae2:export_bus')
    .inputFluids('gtceu:soldering_alloy 144')
    .itemOutputs('advanced_ae:import_export_bus_part')
    .duration(200)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/stock_export_bus')
    .itemInputs('ae2:calculation_processor', 'ae2:export_bus', 'ae2:logic_processor')
    .inputFluids('gtceu:soldering_alloy 144')
    .itemOutputs('advanced_ae:stock_export_bus_part')
    .duration(200)
    .EUt(HV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/advanced_io_bus')
    .itemInputs('4x ae2:speed_card', '3x advanced_ae:quantum_processor', 'advanced_ae:import_export_bus_part', 'advanced_ae:stock_export_bus_part')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:advanced_io_bus_part')
    .duration(300)
    .EUt(EV)

  // Quantum crafting computer. The first six recipes are EV; the four most
  // advanced components are IV to keep the native progression meaningful.
  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_storage_component')
    .itemInputs('4x advanced_ae:quantum_processor', '3x ae2:cell_component_256k', 'ae2:spatial_cell_component_2', 'ae2:quartz_vibrant_glass')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_storage_component')
    .duration(300)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_unit')
    .itemInputs('ae2:crafting_unit', 'ae2:singularity', '2x advanced_ae:quantum_processor')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_unit')
    .duration(300)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_structure')
    .itemInputs('4x ae2:quartz_glass', '4x ae2:sky_stone_block')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_structure')
    .duration(300)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_accelerator')
    .itemInputs('4x advanced_ae:shattered_singularity', '4x advanced_ae:quantum_processor', 'advanced_ae:quantum_unit')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_accelerator')
    .duration(400)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_crafter')
    .itemInputs('4x advanced_ae:shattered_singularity', 'advanced_ae:quantum_accelerator', '2x ae2:cell_component_64k', 'advanced_ae:quantum_unit')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_crafter')
    .duration(400)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_storage_128')
    .itemInputs('4x advanced_ae:shattered_singularity', '4x advanced_ae:quantum_storage_component', 'advanced_ae:quantum_unit')
    .inputFluids('gtceu:soldering_alloy 288')
    .itemOutputs('advanced_ae:quantum_storage_128')
    .duration(400)
    .EUt(EV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_storage_256')
    .itemInputs('advanced_ae:shattered_singularity', '2x advanced_ae:quantum_storage_128', 'advanced_ae:quantum_unit')
    .inputFluids('gtceu:soldering_alloy 576')
    .itemOutputs('advanced_ae:quantum_storage_256')
    .duration(400)
    .EUt(IV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_core')
    .itemInputs('4x ae2:singularity', '2x advanced_ae:shattered_singularity', 'advanced_ae:quantum_accelerator', 'advanced_ae:quantum_unit', 'advanced_ae:quantum_storage_256')
    .inputFluids('gtceu:soldering_alloy 576')
    .itemOutputs('advanced_ae:quantum_core')
    .duration(600)
    .EUt(IV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/quantum_multi_threader')
    .itemInputs('3x advanced_ae:quantum_processor', '3x advanced_ae:quantum_accelerator', 'advanced_ae:quantum_unit', 'advanced_ae:quantum_core')
    .inputFluids('gtceu:soldering_alloy 576')
    .itemOutputs('advanced_ae:quantum_multi_threader')
    .duration(600)
    .EUt(IV)

  gtr.assembler('gtl_compat:advanced_ae/assembler/data_entangler')
    .itemInputs('3x advanced_ae:quantum_storage_256', '4x advanced_ae:shattered_singularity', 'advanced_ae:quantum_unit', 'advanced_ae:quantum_core')
    .inputFluids('gtceu:soldering_alloy 576')
    .itemOutputs('advanced_ae:data_entangler')
    .duration(600)
    .EUt(IV)
})

// Optional GTCEu routes for LT2's ordinary inscriber/circuit-cutter processing.
// Keep native recipes, workbench crafting and lightning-machine recipes intact.
// Quantities follow LT2 compat.5; EU/t, duration and cutting water are pack balance.
ServerEvents.recipes(event => {
  if (!Platform.isLoaded('ae2lt') || !Platform.isLoaded('gtceu')) return

  const gtr = event.recipes.gtceu
  const LV = 30
  const HV = 480

  gtr.macerator('gtl_compat:ae2lt/macerator/overload_crystal_dust')
    .itemInputs('ae2lt:overload_crystal')
    .itemOutputs('ae2lt:overload_crystal_dust')
    .duration(80)
    .EUt(LV)

  // The press is reusable; this produces only the UNCHARGED circuit board.
  gtr.forming_press('gtl_compat:ae2lt/forming_press/unoverloaded_circuit_board')
    .notConsumable('ae2lt:overload_inscriber_press')
    .itemInputs('ae2lt:overload_crystal')
    .itemOutputs('ae2lt:unoverloaded_circuit_board')
    .duration(200)
    .EUt(HV)

  // A native overload crystal block contains four crystals, not nine.
  gtr.cutter('gtl_compat:ae2lt/cutter/unoverloaded_circuit_board')
    .itemInputs('ae2lt:overload_crystal_block')
    .inputFluids('minecraft:water 100')
    .itemOutputs('4x ae2lt:unoverloaded_circuit_board')
    .duration(200)
    .EUt(HV)

  // Charging the board still requires LT2 lightning processing beforehand.
  gtr.forming_press('gtl_compat:ae2lt/forming_press/overload_processor')
    .itemInputs('ae2lt:overload_circuit_board', '#forge:dusts/redstone', 'ae2:printed_silicon')
    .itemOutputs('ae2lt:overload_processor')
    .duration(200)
    .EUt(HV)
})

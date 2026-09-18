const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')
const vm = require('node:vm')

const script = fs.readFileSync(path.join(__dirname, '../../kubejs/server_scripts/ae2lt_gtceu.js'), 'utf8')
const bothMods = ['ae2lt', 'gtceu']

// A DSL contract check, not a substitute for a real Forge /reload.
function recipeLoader(loadedMods = bothMods) {
  let callback
  let recipes
  const gtr = Object.fromEntries(['macerator', 'forming_press', 'cutter'].map(type => [type, id => {
    assert.ok(!recipes.has(id), `Duplicate recipe ID: ${id}`)
    const recipe = { type, id, calls: [] }
    recipes.set(id, recipe)
    const builder = {}
    for (const method of ['itemInputs', 'itemOutputs', 'inputFluids', 'notConsumable', 'duration', 'EUt']) {
      builder[method] = (...args) => {
        recipe.calls.push([method, ...args])
        return builder
      }
    }
    return builder
  }]))
  const context = vm.createContext({
    Platform: { isLoaded: mod => loadedMods.includes(mod) },
    ServerEvents: { recipes: fn => { callback = fn } }
  })
  return () => {
    recipes = new Map()
    vm.runInContext(script, context)
    assert.equal(typeof callback, 'function')
    callback({
      get recipes() {
        assert.ok(bothMods.every(mod => loadedMods.includes(mod)), 'GT DSL accessed with a missing mod')
        return { gtceu: gtr }
      }
    })
    return Array.from(recipes.values())
  }
}

for (const mods of [[], ['ae2lt'], ['gtceu']]) {
  test(`missing required mod skips all recipes: ${mods.join(',') || 'none'}`, () => {
    assert.deepEqual(recipeLoader(mods)(), [])
  })
}

const expected = [
  { type: 'macerator', id: 'gtl_compat:ae2lt/macerator/overload_crystal_dust', calls: [
    ['itemInputs', 'ae2lt:overload_crystal'], ['itemOutputs', 'ae2lt:overload_crystal_dust'],
    ['duration', 80], ['EUt', 30]
  ] },
  { type: 'forming_press', id: 'gtl_compat:ae2lt/forming_press/unoverloaded_circuit_board', calls: [
    ['notConsumable', 'ae2lt:overload_inscriber_press'], ['itemInputs', 'ae2lt:overload_crystal'],
    ['itemOutputs', 'ae2lt:unoverloaded_circuit_board'], ['duration', 200], ['EUt', 480]
  ] },
  { type: 'cutter', id: 'gtl_compat:ae2lt/cutter/unoverloaded_circuit_board', calls: [
    ['itemInputs', 'ae2lt:overload_crystal_block'], ['inputFluids', 'minecraft:water 100'],
    ['itemOutputs', '4x ae2lt:unoverloaded_circuit_board'], ['duration', 200], ['EUt', 480]
  ] },
  { type: 'forming_press', id: 'gtl_compat:ae2lt/forming_press/overload_processor', calls: [
    ['itemInputs', 'ae2lt:overload_circuit_board', '#forge:dusts/redstone', 'ae2:printed_silicon'],
    ['itemOutputs', 'ae2lt:overload_processor'], ['duration', 200], ['EUt', 480]
  ] }
]

test('registers exactly the four approved processing routes, without native recipe removal', () => {
  assert.deepEqual(recipeLoader()(), expected)
})

for (const recipe of expected) {
  test(`preserves quantities, catalysts, power and duration: ${recipe.id}`, () => {
    assert.deepEqual(recipeLoader()().find(actual => actual.id === recipe.id), recipe)
  })
}

test('consecutive script evaluations use the same IDs without leaking global declarations', () => {
  const reload = recipeLoader()
  assert.deepEqual(reload(), expected)
  assert.deepEqual(reload(), expected)
})

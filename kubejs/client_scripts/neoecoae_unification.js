JEIEvents.hideItems(event => {
    // GTCEu obtains tungsten from minerals such as scheelite and wolframite;
    // it has no equivalent pure tungsten ore or raw-tungsten item to unify to.
    const unavailableTungstenForms = [
        "neoecoae:tungsten_ore",
        "neoecoae:raw_tungsten_ore",
        "neoecoae:raw_tungsten_block"
    ]
    unavailableTungstenForms.forEach(item => event.hide(item))
})

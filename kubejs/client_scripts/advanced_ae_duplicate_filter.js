// Hide the intentionally disabled AdvancedAE duplicates from JEI. The items
// remain registered so existing worlds are not modified.
if (Platform.isLoaded('advanced_ae') && Platform.isLoaded('gtlcore')) {
  JEIEvents.hideItems(function(event) {
    event.hide('advanced_ae:throughput_monitor')
    event.hide('advanced_ae:throughput_monitor_configurator')
  })
}

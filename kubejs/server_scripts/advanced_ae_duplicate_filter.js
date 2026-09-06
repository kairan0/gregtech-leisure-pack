// GTLCore's throughput monitor has the same base recipe as AdvancedAE's
// version, and additionally supports the GTLCore local/wireless terminals
// and I/O source tracking. Keep GTLCore as the canonical implementation.
ServerEvents.recipes(function(event) {
  if (!Platform.isLoaded('advanced_ae') || !Platform.isLoaded('gtlcore')) return

  event.remove({ id: 'advanced_ae:throughput_monitor' })
  event.remove({ id: 'advanced_ae:throughput_monitor_configurator' })
})

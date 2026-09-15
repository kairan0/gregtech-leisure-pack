# Changelog

## [1.4.5.1-kairan.6] - 2026-09-16

### Fixed

- Removed Wildcard Pattern's six-condition limit in both filter and I/O configurators, with a bounded scrollable list and visible scrollbar.
- Stabilized AE2LT Network Tool sidebars during the initial inventory synchronization without accepting later tool removal or a different-NBT replacement.
- Let the AE2LT Lightning Simulation Chamber consume its local FE buffer first and fall back to correctly converted native ME-network power; lightning-key requirements remain unchanged.
- Aligned the public pack manifest with the validated ExtendedAE Plus NeoECO C4 compat.3 build already used by the client and server.

## [1.4.5.1-kairan.5] - 2026-09-09

### Added

- Added 27 balanced GTCEu machine routes for AdvancedAE materials, network devices, and quantum crafting CPU components.

### Fixed

- Added NeoECO C4 CPU support for ExtendedAE Plus virtual crafting cards without suppressing outstanding real recipe outputs.

## [1.4.5.1-kairan.3] - 2026-09-07

### Fixed

- Reserved UDP port 24455 for the GTL Simple Voice Chat server so pack synchronization no longer restores the conflicting 24454 client value.

## [1.4.5.1-kairan.2] - 2026-09-07

### Fixed

- Fixed the dedicated-server crash when opening a GTLCore ME Dual Input Hatch with LDLib 1.0.33.b.
- Restored LDLib 1.0.33.b, which is required by Neo ECO 20.4.2, while retaining the repaired GTLCore client action behavior.

## [1.4.5.1-kairan.1] - 2026-09-07

### Added

- Added packwiz metadata for the current MC 1.20.1 / Forge 47.4.16 client.
- Added Neo ECO, AdvancedAE, AE2 Lightning Tech, Thunderbolt and Wildcard Pattern compatibility builds used by the server.
- Added `.mrpack` export and `office` server update scripts.

### Changed

- Updated current FTB, Sophisticated Storage, Jade, ModernFix, MAE2 and ToolBelt metadata from the older launcher manifest.
- Marked eleven client-only mods so they are excluded from dedicated-server installation.
- Prefer exact SHA-512 Modrinth sources, then verified CurseForge CDN URLs; custom builds remain SHA-256 pinned on GitHub Releases.
- Distribute resource packs and shaders as client-only downloads instead of embedding them in the pack.

### Fixed

- Excluded obsolete duplicate JAR versions and runtime caches from distributed packs.
- Kept the existing GTL compatibility fixes and KubeJS recipe/unification changes in the published configuration.
- Removed client-side YSM model payloads and auto-downloaded TLM packs from the public archive, reducing the `.mrpack` to about 7.6 MB with zero embedded JAR/ZIP payloads.
- Added a SHA-256-pinned server updater shared by manual synchronization and both `office` server launch entry points.

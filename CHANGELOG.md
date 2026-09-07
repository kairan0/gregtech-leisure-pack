# Changelog

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

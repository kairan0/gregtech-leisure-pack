# Changelog

## [Unreleased]

### Accepted Wildcard provider fix (2026-09-20)

- Overloaded providers now advertise all concrete recipes from Wildcard Pattern
  cards and keep independent adaptive batch histories for expanded recipes.
- Pin the locally tested and player-accepted LT2 `e391878e` binary without
  rebuilding. Matching source: `assets-v5/ae2lt-source-e391878e.tar.gz`.
- Thunderbolt and Wildcard binaries are unchanged. No pack-version bump or mrpack.
- Validation: 795 unit tests passed, one environment test skipped; 35 minimal
  GameTests and a targeted real GT/Wildcard decoder test. Production startup and
  exhaustive host/restart combinations are not implied by local acceptance.

### Accepted provider update (2026-09-20)

- Add ordinary and extended cable-mounted overloaded providers with paired
  Thunderbolt Part-host support. Preserve existing Tianshu/GTL batching fixes.
- Fix GTL configuration circuits incorrectly keeping overloaded providers blocked.
- Match AE2 bright UI backgrounds, slot frames and text colors; restore the
  ordinary cable provider's pink border and unify block/part display names.
- Pin the locally accepted LT2 `27ce1446` and Thunderbolt `bf5735d` binaries,
  without rebuilding. Matching source archives are in `assets-v5` as
  `ae2lt-source-27ce1446.tar.gz` and `thunderbolt-source-bf5735d.tar.gz`.
- Clients and server must update both mods together (LT2 protocol 4 / Thunderbolt
  beta.4). Old-protocol clients cannot connect. EAEP channel-card support remains
  deferred and is not part of this update.
- Validation: LT2 788 unit tests and local player acceptance; prior Part/circuit
  GameTests and Thunderbolt 490 unit tests. Production startup is not implied.
  Continue the minimal assets/packwiz update; no new mrpack or pack-version bump.

### Added

- Published the accepted LT2 build `4196ddf4`: Tianshu merges GTL physical
  processing inputs within reserved inventory, target capacity and dispatch budgets.
  Local gameplay acceptance observed up to 10K inputs in one dispatch; edge cases
  remain under continued gameplay observation. EAEP-only batching is not enabled.

### Fixed

- Restored LT2 crafting-planning priority when an online Tianshu enables an LT2
  algorithm; otherwise preserve the existing ECO/GTL route. Included in the same JAR.

### Changed

- Minimal hotfix delivery through the existing asset channel, pinned by SHA-256.
  The accepted binary keeps its original filename and internal version; no rebuild
  or new part-provider development is included. Matching source archive:
  `assets-v5/ae2lt-source-4196ddf4.tar.gz`. Validation: 766 unit tests, 24 required
  GameTests, installed Mixin checks and local player acceptance.

## [1.4.5.1-kairan.9] - 2026-09-19

### Fixed

- Fixed standalone and Wireless Universal Terminal Tianshu screens being
  redirected to the ordinary pattern-terminal style by GTLCore. Tianshu now
  uses dedicated style entrypoints, while the validated AE2/AE2WTLib theme
  compatibility fallback remains active.

### Changed

- Updated the community AE2 Lightning Tech build to compat.14 and published it
  as an immutable `assets-v5` binary.

## [1.4.5.1-kairan.8] - 2026-09-18

### Fixed

- Restored all official ExtendedAE 1.4.12 data and assets in compat.2: 65 previously omitted recipes (including the Extended Pattern Provider), 23 block loot tables, 10 tags and 53 recipe advancements. Existing data files now match the original byte-for-byte too.
- Preserved the accepted main-thread GUI registration fix. Releases now overlay only the entry class and explicit versions onto the hash-locked original JAR, with an entry-by-entry integrity gate and six packaging regression tests. No KubeJS workaround or second ExtendedAE JAR is required.
- Kept LT compat.5, NeoECO compat.7, GTLCore compat.4 and all other accepted builds unchanged. Existing instances must recoverably retire the previous compat.1 JAR after verifying compat.2; fresh imports contain only compat.2.

## [1.4.5.1-kairan.7] - 2026-09-18

### Fixed

- Replaced original ExtendedAE 1.4.12 with the in-game-validated compat.1 build: client screen/hotkey registration now runs on the main thread. Exactly one ExtendedAE is distributed; no Network Tool sidebar is added to screens that never implemented it upstream. Source: https://github.com/kairan0/ExtendedAE/releases/tag/1.20-1.4.12-forge-gtlcompat.1 .

- Pinned the already deployed NeoECO compat.7 causal supplier planner, with executable first-step inventory and no synthetic startup top-up or forced-start workaround. Preserves exact runtime version 20.4.2 for EAEP integration. Existing saved jobs are not automatically recalculated.

- Pinned the already deployed GTLCore compat.4, retaining dedicated-server GUI and adaptive AE2/NeoECO batching fixes while removing superseded ECO submission-plan/startup top-up workarounds.

- Pinned the already deployed AE2LT compat.5, including unified FE/ME processing power and Network Tool GUI fixes. LT/ECO/GTLCore are downloaded from immutable assets-v4, with matching source/build snapshots, so continuous updates no longer downgrade the accepted builds.

### Added

- Added New Visual Keybing 0.6.16 as a client-only, SHA-512-pinned Modrinth download; personal keybind-viewer preferences are not distributed.

- Added four reloadable, balanced LT2 GTCEu processing routes through KubeJS. Ordinary crafting-table recipes and Lightning Assembly/Overload factory exclusive recipes remain unchanged.

### Changed

- Retained Wildcard compat.5 and EAEP NeoECO compat.3; AE2LT is preserved as an unofficial community continuation with original licenses and attribution.

- Excluded renamed Codex session backups as well as ordinary session data. Release builds use committed configuration, preserving uncommitted local preferences and runtime-generated files.

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

# Codex client installation contract

## Scope and trusted inputs

Configure only the selected GregTech Leisure instance. Preserve player saves,
options, servers.dat, accounts, tokens and unrelated instances. Use Java 17,
Minecraft 1.20.1 and Forge 47.4.16. The verified updater additionally requires
Python 3.11+; check availability before configuring a launch hook.

- Client releases: https://github.com/kairan0/gregtech-leisure-pack/releases
- Update manifest: https://kairan0.github.io/gregtech-leisure-pack/pack.toml

Select the newest non-draft, non-prerelease `GregTech-Leisure-*.mrpack`, not an
`assets-*` release. A binary upload is not a complete client release.

## Install and update

1. Import the newest mrpack into a new HMCL/PCL instance. Use launcher-supported
   import; request a GUI action when it cannot be automated safely. Retain the
   imported `gtl-import-jars.json`: it identifies old files before packwiz has state.
2. The package includes `gtl-update.py`, `gtl-known-jars.json`,
   `update-gtl.sh` and `update-gtl.bat`. For older imports, obtain these reviewed
   files from the same repository revision. Reuse the shipped updater rather
   than generating an unguarded bootstrap command.
3. Ensure the selected instance is not running. Run `bash update-gtl.sh` on
   macOS/Linux, or `update-gtl.bat` on Windows. Set `GTL_JAVA` to the launcher's
   Java 17 executable and, if needed, `GTL_PYTHON` to Python 3.11+.
   The wrapper propagates failures. It downloads and verifies the official
   v0.0.3 bootstrap before execution.
4. Configure this instance's pre-launch command only when the launcher format
   is known; back up its configuration first. Use absolute quoted paths, wait
   for completion and abort launch on failure where supported. Otherwise provide
   the exact manual command; report the hook as inactive rather than guessing.
5. Completion requires updater exit 0, matching manifest/index hashes, valid
   canonical JAR hashes and no duplicate top-level Forge mod IDs. Then perform
   client startup validation. Joining an online-mode server requires the user's
   authenticated launcher account; offline main-menu startup is not a join test.

## Rename handling and failure recovery

The updater retains `.gtl-update-history.json` before invoking packwiz, backs up
verified originals and checks modified managed files before upstream can remove
them. After success it archives only recognized, hash-matching superseded files
outside `mods`. This covers both old mrpack imports with no packwiz history and
renamed targets that already exist. Unrecognized duplicates block the update;
preserve them and request direction. Keep disabled JARs and unrelated add-ons.

Backups live in `backups/pre-update-*` and `backups/superseded-jars-*`. A failed
partial install is not safe to launch. Missing verified originals are restored,
but the updater does not promise a whole-instance rollback of every config.
Retain history and backups for retry. After a crash leaves `.gtl-update-lock`,
verify no updater is running before removing the empty lock directory.

## Player options

The maintained preset is `client-defaults/options.txt`. Fresh mrpacks also place
it in `client-overrides/options.txt`. The live `options.txt` is excluded from
packwiz; updates preserve existing player settings and seed it only when absent.
Use new-instance imports for the initial preset, not an mrpack overwrite of an
existing player's directory. Validate that all selected resource-pack filenames
exist in the release, and clear personal server/audio-device fields in presets.

## Handoff

Report the instance path, release version, Java/Python paths, updater command,
launch-hook status, duplicate/hash checks, and whether validation reached only
the main menu or an authenticated server join. Never upload tokens, local logs,
saves or private session data as release content.

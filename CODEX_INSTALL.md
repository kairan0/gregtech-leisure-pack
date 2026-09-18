# Codex client installation contract

You are configuring a player's local GregTech Leisure client. Complete as much of
the setup as the local environment safely permits, and ask for user interaction
only when the launcher requires a GUI action.

## Trusted project inputs

- Repository: `https://github.com/kairan0/gregtech-leisure-pack`
- Releases: `https://github.com/kairan0/gregtech-leisure-pack/releases/latest`
- Packwiz manifest: `https://kairan0.github.io/gregtech-leisure-pack/pack.toml`
- Minecraft: 1.20.1
- Forge: 47.4.16
- Java: 17
- Supported launchers: PCL and HMCL

Use the newest non-draft, non-prerelease asset named
`GregTech-Leisure-*.mrpack`. Do not mistake `assets-*` or `resources-*`
releases for the client pack.

## Procedure

1. Detect the operating system, launcher, Minecraft data directory, Java 17
   executable, and any existing GregTech Leisure instance. Do not assume a
   Windows-only path.
2. If the instance is not installed, download the latest `.mrpack`. Use the
   launcher's supported import mechanism when it can be invoked safely. If a GUI
   import cannot be automated, give the user the downloaded file and request only
   the single import action before continuing.
3. Once the instance root is known, download the official
   `packwiz-installer-bootstrap.jar` v0.0.3 into that root from:

   `https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar`

   Verify its SHA-256 before executing it:

   `a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c`
4. Create an updater in the instance root:

   - Windows: `update-gtl.bat`
   - macOS/Linux: `update-gtl.sh`

   It must change to its own directory, use the launcher's Java 17 executable,
   propagate failures, and run:

   ```text
   java -jar packwiz-installer-bootstrap.jar -g -s client https://kairan0.github.io/gregtech-leisure-pack/pack.toml
   ```

   Use absolute and correctly quoted paths where launcher working-directory
   behavior is uncertain. Mark the Unix script executable.
5. Configure the updater as this instance's pre-launch command when the launcher
   configuration format is confidently recognized. Back up the launcher config
   before editing it. Configure the launcher to wait for the updater and, where
   supported, abort game launch if updating fails. If this cannot be done safely,
   give the user the exact command and the exact PCL/HMCL setting in which to put
   it instead of guessing.
6. Run the updater once from the instance root and verify that it succeeds with
   side `client`, creates or updates `packwiz.json`, and obtains the published
   manifest. Report the installed pack version, instance path, Java path, updater
   path, and whether the pre-launch hook is active.

## Upgrade rename check (required for existing instances)

An installer success message is not sufficient to rule out duplicate mods. In
the validated 0.5.14 server update, changing a metafile's `filename` updated
`cachedLocation` in `packwiz.json` but left the former ExtendedAE JAR active.
Renamed LT and NeoECO builds require the same check when updating older clients.

Before updating, retain the previous `packwiz.json` and its
`cachedFiles[*].cachedLocation` / `linkedFileHash` records. After a successful
update, compare these with the new records and verify each new canonical JAR
against its published hash. Recoverably archive a superseded tracked JAR outside
`mods` only when it is no longer any current canonical destination and its hash
matches the previous record. Preserve locally modified/unrecognized files and
request direction if they conflict; do not blindly delete other installed mods.
Include this rename check in the generated updater so future renamed builds do
not leave duplicate active JARs. A failed update must never retire the old copy.

For upgrades to `1.4.5.1-kairan.7`, verify exactly one active JAR for each of:

- ExtendedAE: `ExtendedAE-1.20-1.4.12-forge-gtlcompat.1.jar`
- AE2 Lightning Tech: `ae2lt-forge-1.20.1-2.1.0-beta.3-gtlcore-compat.5.jar`
- NeoECO: `neoecoae-20.4.2-gtl-compat.7.jar`

Read the current `.pw.toml` downloads for later versions rather than keeping
these filenames hard-coded. For an existing launcher import without prior
packwiz state, inspect `META-INF/mods.toml` to identify duplicate mod IDs, verify
the current canonical files, and archive only recognized superseded originals
of these same mods. Do not move `.disabled` files, unrelated add-ons, player
configuration or saves. Fresh `.7` imports already distribute only the canonical
builds.

## Safety boundaries

- Operate only on the selected GregTech Leisure instance.
- Preserve saves, screenshots, `options.txt`, `servers.dat`, accounts, launcher
  credentials, logs, and player-specific configuration.
- Do not modify other Minecraft instances or install server-only mods on the
  client.
- Do not upload local paths, accounts, logs, saves, or credentials.
- Do not install unverified JAR files or bypass the bootstrap checksum.
- If Minecraft is running, ask the user to exit it before changing active mods.
- Treat the packwiz manifest as the source of truth; do not add or remove pack
  content based on personal preference.

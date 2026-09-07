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

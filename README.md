# GregTech Leisure - kairan0 custom pack

这是当前私人 GTL 1.20.1 客户端与 `office` 服务器使用的非官方维护版本。

## 玩家安装

1. 在 GitHub Releases 下载最新的 `GregTech-Leisure-*.mrpack`。
2. 使用支持 Modrinth 整合包格式的 PCL 或 HMCL 导入。
3. 使用 Java 17 启动。

包内固定 Minecraft 1.20.1 与 Forge 47.4.16。每次更新都会发布新的 `.mrpack`；服务器从同一份 packwiz 清单同步 `server`/`both` 文件。

使用 Codex 的玩家可以把下面这一句话直接发给 Agent，让它按仓库内的版本化规程完成安装和启动前自动同步：

```text
请读取并执行 https://raw.githubusercontent.com/kairan0/gregtech-leisure-pack/main/CODEX_INSTALL.md
```

## 本地维护

当前游戏目录就是唯一编辑源。修改模组、配置或 KubeJS 后：

```bash
scripts/export-mrpack.sh
git add pack.toml index.toml mods config defaultconfigs kubejs ldlib packmenu patchouli_books resourcepacks shaderpacks skyblockbuilder scripts
git commit -m "chore: update modpack"
git push
scripts/publish.sh
```

`.tools/packwiz` 是本地构建工具，不提交到 Git。`mods/*.jar`、存档、日志、缓存和本地兼容构建档案也不会进入仓库。

首次发布前先执行 `scripts/publish-assets-v1.sh` 和 `scripts/publish-resources-v1.sh` 上传锁定的自托管文件；之后执行 `scripts/export-mrpack.sh`、提交更新，再运行 `scripts/publish.sh`。

模组来源按 SHA-512 精确匹配优先使用 Modrinth，其次使用已验证的 CurseForge CDN；只有修改版/定制 JAR 使用 GitHub Release。资源包和光影同样通过下载元数据分发，不直接嵌入 `.mrpack`。

YSM 的 `built`、`custom` 和 `cache` 不进入公开客户端包。发布脚本会把本地 `built/custom` 同步到 `office` 服务端，由服务端向客户端提供模型。`tlm_custom_pack` 由 Touhou Little Maid 自动下载默认内容，也不进入发行包。

`office` 服务端的 `run.sh` 与 `start.sh` 在启动 Forge 前都会执行 `update-pack.sh`，从同一个 Pages 清单安装服务端所需文件。也可以在本地随时手动同步配置、YSM 模型并刷新服务端：

```bash
scripts/update-office-server.sh
```

更新失败会阻止服务器继续启动，避免以不完整版本运行。`packwiz-installer-bootstrap` 固定为官方 v0.0.3，并在执行前校验 SHA-256。

## 自托管模组

无法从 Modrinth/CurseForge 精确取得的定制 JAR 使用 GitHub Release `assets-v1` 和 SHA-256 固定；本地定制资源包使用 `resources-v1`。更新这些文件时应发布新的 assets tag，并同步修改相应 `.pw.toml`，不要覆盖旧资产。

本仓库只用于维护该私人服务器所需的组合；第三方模组的著作权和许可证归各自作者所有。

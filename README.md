# GregTech Leisure - kairan0 custom pack

这是当前私人 GTL 1.20.1 客户端与 `office` 服务器使用的非官方维护版本。

## 玩家安装

1. 在 GitHub Releases 下载最新的 `GregTech-Leisure-*.mrpack`。
2. 使用支持 Modrinth 整合包格式的 PCL 或 HMCL 导入。
3. 使用 Java 17 启动。

包内固定 Minecraft 1.20.1 与 Forge 47.4.16。每次更新都会发布新的 `.mrpack`；服务器从同一份 packwiz 清单同步 `server`/`both` 文件。

## 本地维护

当前游戏目录就是唯一编辑源。修改模组、配置或 KubeJS 后：

```bash
scripts/export-mrpack.sh
git add pack.toml index.toml mods config defaultconfigs kubejs ldlib packmenu patchouli_books resourcepacks shaderpacks skyblockbuilder tlm_custom_pack
git commit -m "chore: update modpack"
git push
scripts/publish.sh
```

`.tools/packwiz` 是本地构建工具，不提交到 Git。`mods/*.jar`、存档、日志、缓存和本地兼容构建档案也不会进入仓库。

首次发布前先执行 `scripts/publish-assets-v1.sh` 上传锁定的自托管文件；之后执行 `scripts/export-mrpack.sh`、提交更新，再运行 `scripts/publish.sh`。

## 自托管模组

无法从 CurseForge 精确取得的定制 JAR 使用 GitHub Release `assets-v1` 和 SHA-256 固定。更新这些文件时应发布新的 assets tag，并同步修改相应 `.pw.toml`，不要覆盖旧资产。

本仓库只用于维护该私人服务器所需的组合；第三方模组的著作权和许可证归各自作者所有。

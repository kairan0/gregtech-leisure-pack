# GregTech Leisure - kairan0 custom pack

这是当前私人 GTL 1.20.1 客户端与 `office` 服务器使用的非官方维护版本。

## 玩家安装

1. 在 GitHub Releases 下载最新的 `GregTech-Leisure-*.mrpack`。
2. 使用支持 Modrinth 整合包格式的 PCL 或 HMCL 导入。
3. 新实例会使用维护者的材质包顺序、按键和其他 options 预设。使用 Java 17 启动。
4. 在线更新使用包内 `update-gtl.sh`（Windows 为 `update-gtl.bat`），需 Python 3.11+；
   可通过 `GTL_JAVA`、`GTL_PYTHON` 指定解释器。首次导入新包本身不需要 Python。

包内固定 Minecraft 1.20.1 与 Forge 47.4.16。每次更新都会发布新的 `.mrpack`；服务器从同一份 packwiz 清单同步 `server`/`both` 文件。

使用 Codex 的玩家可以把下面这一句话直接发给 Agent，让它按仓库内的版本化规程完成安装和启动前自动同步：

```text
请读取并执行 https://raw.githubusercontent.com/kairan0/gregtech-leisure-pack/main/CODEX_INSTALL.md
```

更新器会验证当前 JAR，并将哈希可确认的旧版本移到 `backups/`；未知或被改动的重复包会阻止更新，交由用户处理。`options.txt` 不受在线更新覆盖。自动更新需在启动器中明确配置为等待执行并在失败时停止启动，单纯导入包不会自动启用此钩子。

已有 `config/ae2lt-common.toml` 和 `config/skyblockbuilder/structures.json5` 使用 packwiz
`preserve` 保留，防止实例页数及空岛结构设置被更新还原；新实例仍取得包内默认值。
若以后需要迁移这些配置，必须单独设计和验收迁移，不能假设清单会覆盖已有文件。

## 本地维护

发布应在独立干净 checkout 中构建，避免将游戏运行中产生的配置改动意外打包。修改模组、配置或 KubeJS 后：

```bash
scripts/export-mrpack.sh --preview
# 只提交已审查的改动；检查 refresh 更新的清单。
git add <reviewed-files>
git commit -m "chore: update modpack"
git push
# 先保留已完成游戏内验收的候选附件，再交给发布入口比较载荷。
scripts/publish.sh --accepted-artifact /absolute/path/to/accepted.mrpack
```

`.tools/packwiz` 是本地构建工具，不提交到 Git。`mods/*.jar`、存档、日志、缓存和本地兼容构建档案也不会进入仓库。

首次发布前先执行 `scripts/publish-assets-v1.sh` 和 `scripts/publish-resources-v1.sh` 上传锁定的自托管文件；之后执行 `scripts/export-mrpack.sh`、提交更新，再运行 `scripts/publish.sh`。

模组来源按 SHA-512 精确匹配优先使用 Modrinth，其次使用已验证的 CurseForge CDN；只有修改版/定制 JAR 使用 GitHub Release。资源包和光影同样通过下载元数据分发，不直接嵌入 `.mrpack`。

YSM 的 `built`、`custom` 和 `cache` 不进入公开客户端包。单独运行服务器部署脚本时，会把本地 `built/custom` 同步到 `office` 服务端，由服务端向客户端提供模型。`tlm_custom_pack` 由 Touhou Little Maid 自动下载默认内容，也不进入发行包。发布客户端不再自动部署服务器。

`office` 服务端的 `run.sh` 与 `start.sh` 在启动 Forge 前都会执行 `update-pack.sh`，从同一个 Pages 清单安装服务端所需文件。也可以在本地随时手动同步配置、YSM 模型并刷新服务端：

```bash
scripts/update-office-server.sh
```

更新失败会阻止服务器继续启动，避免以不完整版本运行。`packwiz-installer-bootstrap` 固定为官方 v0.0.3，并在执行前校验 SHA-256。

发布门禁包括：导出包逐项匹配当前元数据、下载内容哈希、唯一模组 ID、options 引用的资源包完整、Pages 与当前提交逐文件一致、GitHub 草稿附件重新下载后逐字节一致。Pages 尚未更新时会明确失败，稍后重试；上传成功不等于整条链验收完成。

回归测试：`python3.11 -m unittest discover -s scripts/tests -p 'test_*.py'`。
本次问题和避免复发的规则见 [发布安装故障记录](docs/release-install-20260922.md)。

## 自托管模组

无法从 Modrinth/CurseForge 精确取得的定制 JAR 使用 GitHub Release `assets-v1` 和 SHA-256 固定；本地定制资源包使用 `resources-v1`。更新这些文件时应发布新的 assets tag，并同步修改相应 `.pw.toml`，不要覆盖旧资产。

本仓库只用于维护该私人服务器所需的组合；第三方模组的著作权和许可证归各自作者所有。

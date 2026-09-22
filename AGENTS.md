# 发布与部署

涉及整合包发布、部署、核对最新版本或验证玩家安装时，先完整读取并执行
`.agents/skills/gtl-release/SKILL.md`；完成条件以其中的验收门禁和实际证据为准。

技能和本文件属于仓库开发资料，排除在 packwiz 和客户端包之外。

# 提交内容

- 提交前读取 `.agents/skills/gtl-release/SKILL.md` 的“公开内容边界”，按明确文件列表暂存并审查完整 staged diff。
- 对全部 Git 跟踪路径运行 `python3.11 scripts/content_policy.py`；打包忽略规则不能代替 Git 内容审查。
- 玩家运行数据和本次排障／验收记录留在本地忽略目录；新增长期文档须说明维护用途。

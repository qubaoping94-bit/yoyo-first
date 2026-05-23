# 安全与核验原则

## 安装第三方 skill 前

必须核验：

- 仓库 owner 是否可信
- 是否来自官方组织或产品方
- 是否有 `SKILL.md`
- `SKILL.md` frontmatter 是否清晰
- 是否包含脚本
- 是否访问浏览器 cookie、本地凭据、SSH key、云账号 token
- 是否有 destructive 命令，如删除目录、销毁云资源、修改权限
- 是否有不必要的网络下载、base64 执行、`eval`、`exec`

## 云部署类 skill 的特殊风险

Azure、Foundry、部署类 skill 经常会出现：

- `az login`
- access token
- credential
- managed identity
- role assignment
- `azd up`
- `terraform apply`

这些词本身不代表恶意，但必须判断是否只是文档说明，还是安装时会自动执行。

本技能包的原则：

- 安装阶段不运行部署命令。
- 部署前必须经过准备和验证。
- 破坏性操作必须让用户确认。
- 不读取或上传用户私密凭据。
- 不把视频里提到的名字直接当成真实包安装。

## 抖音内容提取安全

提取视频时只用于识别公开页面文本、标题、章节、字幕或可见内容。

如果 Douyin 要求登录或 cookies：

- 不主动窃取浏览器 cookie。
- 不要求用户暴露账号密码。
- 可让用户提供视频截图、文字稿或复制出来的内容作为替代。

## GitHub 上传注意

不要把这些内容提交到公开仓库：

- `.env`
- API Key
- Azure subscription secret
- access token
- 浏览器 cookie
- 本地账号信息
- 私有项目源码

本仓库 `.gitignore` 已默认忽略常见敏感文件。


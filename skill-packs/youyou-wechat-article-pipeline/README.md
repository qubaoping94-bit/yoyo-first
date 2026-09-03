# 优优无机板公众号文章一条龙

这是一个面向 WorkBuddy 的单技能包，覆盖优优无机板公众号文章从选题、写作、排版、配图、校验到微信草稿箱的完整流程。

## 安装

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

安装后重启 WorkBuddy 或新开会话。外部依赖与本机路径配置见 [安装说明](docs/INSTALLATION.md)。

## 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

## 调用示例

```text
使用 $youyou-wechat-article-pipeline 写优优无机板材料体系系列下一篇公众号文章。
```

原始中文使用说明随技能安装，路径为 `skills/youyou-wechat-article-pipeline/使用说明书.md`。


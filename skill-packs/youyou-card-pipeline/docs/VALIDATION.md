# 2.0.0 实测记录

日期：2026-10-09。环境：Windows、Python 3.12.10、Node 24.15.0、已有 Playwright 1.62.1、Google Chrome channel。

- 内置 deck.example.json 构建成功，8张PNG均为1080×1440；布局校验 ok=true，无 issues/warnings。
- 八张图片分别打开目检：标题、正文、箭头、对齐与收尾蓝块可见，无截字。示例图片位于 examples/demo。
- 正文1000字符通过，1001字符返回超限；缺少规定标题返回输入错误。
- 故意将三列卡正文扩大80倍，布局检查返回失败；未放行该输入。
- quick_validate.py 以UTF-8模式验证技能入口通过；包清单13个文件的SHA-256检查通过。
- Codex与WorkBuddy安装目录均核对同一清单；旧WorkBuddy版本移入发现目录之外的skill-backups。

未验证：宿主UI自动发现与附件展示完整流程、macOS/Linux、其他字体、独立下载的Playwright最低版本。源码可跨宿主使用不等于所有环境完成实测。图片示例是流程说明，不是任何产品检测或摄影证明。

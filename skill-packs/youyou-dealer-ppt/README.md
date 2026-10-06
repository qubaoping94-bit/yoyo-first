# youyou-dealer-ppt

独立技能包，用于制作优优无机板经销商、产品知识和商业演讲。当前优先标准是用户指定的 2026-09-27 正式交付 **21 页八零功能与经营演讲系统**：浅米色网格、近黑大字、红色强调、低无意义留白、清晰证据边界、演讲者备注和可靠翻页。

本包记录样例标准，不发布用户的 EXE、快捷方式、运行配置或完整 21 页样例截图。`assets/approved-21-fixture.html` 是不含业务内容的 21 页样例风格参考页型；`approved-black-red-template.html` 是历史 27 页视觉种子，不得误认作当前样例或事实真源。

2.1.0 增加了画布比例、左侧红色识别条、网格、字号、内容版本冲突和证据台账的静态预检。新稿先对照参考页型做代表页，再逐页目检；静态检查通过并不等于视觉或业务主张已经获批。

安装：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

验证：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
python .\skills\youyou-dealer-ppt\scripts\audit-fidelity.py <deck-html> --pptx <deck.pptx> --pdf <deck.pdf> --report <audit.json>
```

使用时请说明项目所需输出格式；默认先核对样例与新稿资料、主张证据，再制作和逐页验收。技能说明见 [SKILL.md](skills/youyou-dealer-ppt/SKILL.md)。

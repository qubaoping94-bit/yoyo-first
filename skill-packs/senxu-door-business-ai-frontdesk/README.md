# senxu-door-business-ai-frontdesk 使用说明

> **最简单调用方式——安装并配合森旭木门样例库使用，直接复制下面这句话：**

```text
用 $senxu-door-business-ai-frontdesk 查询演示数据 ORDER-A-DEMO-001，从订单、回款、生产、质检、发货、安装、验收到售后逐项汇总当前状态和下一步；只读，不写入。
```

官方仓库：[qubaoping94-bit/yoyo-first](https://github.com/qubaoping94-bit/yoyo-first/tree/main/skill-packs/senxu-door-business-ai-frontdesk)

---

## 一、它是什么

这是森旭木门企业内部经营管理知识库样例的专用 AI 前台。它用于展示一家木门制造企业如何把客户销售、现场测量、设计图纸、报价合同、订单、回款、拆单 BOM、采购、生产、质检、入库、发货物流、安装验收和售后串成现实业务链。

它是“企业实际样例 Skill”，不是给任意制造企业直接套用的通用模板。给其他制造企业建库时，应使用 [`manufacturing-enterprise-operations-ai-frontdesk`](../manufacturing-enterprise-operations-ai-frontdesk)。

本技能包内包含 54 个唯一工作流，核验日期为 2026-08-11。

## 二、核心能力

- 员工用“描述或上传 → 查看预览 → 有权限人员确认”三步办理业务。
- 稳定资料从主档带出，后续事件继承订单、合同、图纸和 BOM 历史快照。
- 严格区分付款凭证与到账、签收与验收、售后受理与责任认定及结案。
- 查询按当前账号权限过滤，保持只读，默认排除 DEMO。
- 外部接口未连接时明确提示，改用上传凭证或人工提供已核实事实。
- 内置 DEMO 实体 ID 真值矩阵，支持正常履约和异常售后两条样例链的精确查询。

## 三、适合与不适合做什么

### 适合

- 给木门生产企业老板、管理人员和员工展示完整成品效果。
- 演示如何按订单号查询订单、回款、生产、发货、安装、验收和售后。
- 培训员工理解哪些字段由 AI 带出、哪些事实必须人工确认。
- 验证森旭木门样例库的 54 条业务意图路由。

### 不适合或尚未验证

- 不适合直接改名后给另一家企业正式使用；新企业应使用 A 通用模板 Skill。
- 本技能包不包含完整森旭木门知识库笔记，只包含 Skill 与业务合同。
- 不连接真实 ERP、物流、财务或生产设备。
- 尚未在真实 ima 在线环境完成安装和 E2E。

## 四、需要提供什么，会得到什么

### 输入

- 配套的森旭木门企业内部经营管理样例知识库。
- 自然语言问题、订单号、客户、日期、状态或上传的业务资料。
- 办理写业务时，需要当前账号及其岗位权限。

### 输出

- 查询时返回符合权限的数据、来源、状态、负责人和下一步，写入增量为 0。
- 办理业务时返回预览；未经确认、修改中、取消或权限不足时不写正式记录。
- 后续事件沿用当时订单、地址、价格、产品、图纸和 BOM 快照。

## 五、两条主要使用路线

### 路线 A：对外展示

在森旭样例库中明确说“查询演示数据”，按 `ORDER-A-DEMO-001` 查看正常履约链，按 `ORDER-A-DEMO-002` 查看变更、延期、质量问题和售后链。

### 路线 B：内部培训

让员工模拟新增客户、订单、生产、发货或售后。每次先查看预览，再由具备相应权限的人员确认；不要把演示结果当作真实业务记录。

## 六、可直接复制的调用指令

### 1. 最简查询

```text
用 $senxu-door-business-ai-frontdesk 查询演示数据 ORDER-A-DEMO-001 的完整状态和下一步；只读，不写入。
```

### 2. 异常订单复盘

```text
用 $senxu-door-business-ai-frontdesk 查询演示数据 ORDER-A-DEMO-002，按时间顺序列出订单变更、延期、生产问题、分批发货、安装验收、售后受理、责任复核、结案和回访；注明每一步的来源和负责人。
```

### 3. 模拟新增订单

```text
用 $senxu-door-business-ai-frontdesk 模拟新增一张木门订单；从样例主档带出客户、项目、产品和单位，让我填写数量、价格、交期和特殊要求，计算后只生成预览，不写正式记录。
```

### 4. 权限约束查询

```text
用 $senxu-door-business-ai-frontdesk 按当前登录账号权限查询演示客户的回款和订单状态；越权字段不要返回，目录10和未明确要求的 DEMO 数据默认排除。
```

### 5. 迁移为其他企业

```text
不要修改森旭样例 Skill。请改用 $manufacturing-enterprise-operations-ai-frontdesk，根据新企业资料生成独立 SETUP 预览，并保留森旭样例作为只读参考。
```

## 七、标准工作流程

1. 先建立或导入森旭木门企业内部经营管理样例库。
2. 安装本 Skill。
3. 对外展示时明确查询演示数据，不混入正式企业数据。
4. 写业务时先描述或上传，再查看预览，最后由有权限人员确认。
5. 查询时按客户、订单号、日期或状态组合条件，只读返回。
6. 需要给新企业建库时，停止修改本样例，切换到 A 通用模板 Skill。

## 八、安装、发现与验证

### 从 GitHub 安装到 Codex

```powershell
git clone https://github.com/qubaoping94-bit/yoyo-first.git
cd .\yoyo-first\skill-packs\senxu-door-business-ai-frontdesk
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

### 验证技能包

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

### 验证已安装副本

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -InstalledOnly
```

验证脚本检查源文件树、Skill 名称、54 个唯一工作流，并在本机可用时运行 Codex quick validator。

### 在 ima 中使用

应先建立森旭木门样例知识库，再通过 ima 当前版本的 Skill 导入入口选择 `skills/senxu-door-business-ai-frontdesk`。真实 ima 导入尚未完成 E2E，具体界面和文件格式以客户端为准。

## 九、依赖与运行条件

- Codex 或兼容 `SKILL.md` 的 Agent。
- 配套森旭木门 A 样例知识库；本仓库未包含完整样例笔记。
- 本 Skill 自身不要求 Python，也不要求网络。

## 十、限制、安全与隐私

- 仓库中的 ID 矩阵是虚构 DEMO；不要替换为真实客户数据后公开提交。
- 查询必须遵守当前账号和员工岗位权限。
- 历史快照优先于后来更新的主档，不能用新地址、新价格或新图纸覆盖旧订单事实。
- 本 Skill 用于展示和培训，不应被宣传为已接通真实企业系统。

## 十一、常见问题

### 为什么直接安装后查询不到订单？

因为本技能包不包含完整森旭样例知识库。需要先导入配套样例笔记。

### 为什么默认查不到 DEMO？

这是防止演示数据混入正式结果的保护规则。演示时明确说“查询演示数据”。

### 如何给另一家木门企业使用？

不要修改森旭样例；使用 A 通用模板 Skill 和该企业自己的资料建立新库。

## 十二、版本与核验信息

- 技能包版本：`1.0.0`
- 适配对象：森旭木门 A 样例知识库 V6.1
- 工作流数量：54
- 源文件数量：5
- 源树 SHA-256：`2FE0F1476C6F6FBD146F0ED8EA8A64FB6843FCB676CB92CA9EB6C8015AC87B7B`
- 最后核验日期：2026-08-11
- 依据：原始 `SKILL.md`、54 项工作流合同、DEMO 实体 ID 真值矩阵、业务快照规则、搜索权限规则、Codex quick validation
- 许可证：本技能包随仓库根目录 MIT License 发布

## 十三、未验证项

- `REAL_AI_IMA_E2E_NOT_RUN`：没有在真实 ima 环境验证安装、权限和查询。
- 没有验证任何真实 ERP、生产、物流或财务接口。

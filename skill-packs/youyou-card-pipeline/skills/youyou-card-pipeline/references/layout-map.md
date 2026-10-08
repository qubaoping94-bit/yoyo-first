# 八卡版式与内容字段

默认顺序：cover → two → tri → two → two → quad → ledger → closing。中间五张可调整顺序，但必须包含 tri、quad；总数固定8张。

JSON 顶层为 title 与 cards。每卡共用 type、eyebrow、title（1至2个明确行字符串）、lead。cover 的 nodes 为2项；tri 为3项；quad 为4项，每项包含 label、title、body。two 的 modules 为2项，每项 label、title、bullets（1至4条）。ledger/closing 的 rows 为3项，每项 title、body；closing 另有 closing（1至2行）。完整可运行样例见 assets/deck.example.json。

普通主标题112px；节点标题48、正文30；编号100、标签52、补充28；模块标题46、列表32；收束38；小标签25、页眉20；第8卡蓝块标题52。所有同类角色统一。模板使用白、黑、浅灰与 IKB #002fa7。

三列卡片的标题和正文尤其需要简短；长原文先提炼，不能把段落原样塞入面板。标题每行建议4至7个中文字符，但是否能放下以实测为准。构建脚本验证结构并转义文字；渲染脚本检查实际几何、字号与图片尺寸。脚本无法判定观点准确性或整体美感，必须逐张目检。

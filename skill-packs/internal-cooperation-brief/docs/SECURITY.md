# 数据与发布范围

生成器读取指定JSON，只写指定输出目录；导出器读取本地HTML，导出时阻断HTTP/HTTPS请求。没有模型API、账号读取、Cookie读取、消息发送或业务材料上传功能。

浏览器依赖安装可能联网；首次下载应使用官方Playwright。Skill不捆绑第三方库、缓存或浏览器。Playwright上游：https://github.com/microsoft/playwright 。

公开包只包含通用规则、模板、代码和明确标为虚构的示例。已确认真实报告及回归用业务JSON保留本地，不纳入仓库。真实业务报告是否发送给谁由用户决定。

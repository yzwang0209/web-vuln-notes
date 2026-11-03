# 02 · 文件上传绕过

| 项 | 内容 |
|---|---|
| 靶场 | PortSwigger Web Security Academy |
| 题目 | ① 直接上传 Web Shell ② Content-Type 绕过 ③ 扩展名黑名单绕过 ④ 混淆扩展名 |
| 用时 | 60 分钟 |
| 状态 | 待开始 |

## 1. 原理

- [ ] 上传功能的风险点在哪一步？（文件落盘 → 路径可访问 → 被当作脚本执行，三个条件缺一不可）
- [ ] 前端校验为什么等于没有校验？
- [ ] 黑名单为什么永远列不全？（`.php3` `.phtml` `.php.` `.php%00` `.pHp`、`::$DATA`、双写 `.pphphp`）

## 2. 复现

### Lab ①：直接上传 shell
- 上传的文件名 / 内容：
- 访问路径：
- 执行的命令与返回：
- 截图：`screenshots/02-upload-01.png`

### Lab ②：Content-Type 绕过
- 被拦时的响应（状态码、提示文字）：
- Burp 里改了哪个字段、改成什么：
- 绕过成功后的响应：
- 截图：`screenshots/02-upload-02.png`

## 3. PoC

```
POST /my-account/avatar HTTP/1.1
Content-Type: multipart/form-data; boundary=...

<请求原文，保留关键头>
```

## 4. 修复建议

- [ ] 白名单扩展名 + 服务端 MIME 与实际内容检测（magic bytes）
- [ ] 上传目录**禁止解析**（`php_flag engine off` / Nginx `location ~ \.php$ { deny all; }`）
- [ ] 文件名随机化 + 不在 web 根目录
- [ ] 为什么"只改前端 JS 校验"完全没用？

## 5. 卡住记录

| 时间 | 卡在哪 | 怎么解决的 |
|---|---|---|
|  |  |  |

## 6. 三层追问自检

1. 为什么能被上传？（校验只在客户端 / 只在扩展名 / 只在 Content-Type，三者都不等于内容安全）
2. 我怎么绕的？（改哪个字段、为什么服务端信了它）
3. 修复为什么有效？（把"能不能执行"从文件名判断改成"目录不具备执行能力"）

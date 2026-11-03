# 01 · SQL 注入（普通注入 + 布尔盲注 + 时间盲注）

| 项 | 内容 |
|---|---|
| 靶场 | PortSwigger Web Security Academy（官方托管，无需本地环境） |
| 题目 | ① WHERE 子句注入（隐藏数据） ② 登录绕过 ③ 布尔盲注 ④ 时间盲注 |
| 用时 | 60 分钟 |
| 状态 | 进行中 |

## 1. 原理（自己写，不要抄）

要回答清楚这四件事，缺一件就是"背过但没懂"：

- [ ] 注入点是怎么形成的？把 `'` 塞进去之后，数据库最终执行的那条 SQL 长什么样？（把拼接前后的完整语句写出来）
- [ ] 为什么 `--` 或 `#` 能"切断"后半句？注释符生效的条件是什么（注意：URL 里的 `--` 后面通常要跟空格或 `+`）？
- [ ] **盲注**：页面不返回数据、也不报错，只剩"有/没有回显"这种二元信号时，凭什么还能把数据一个字一个字挖出来？
- [ ] 时间盲注和布尔盲注的区别在哪、什么场景只能用时间盲注？

## 2. 复现（Lab ①：WHERE 子句）

- 目标 URL（记下来）：
- 正常请求：`GET /filter?category=Gifts` → 返回 N 件商品
- 注入请求：
```
GET /filter?category=Gifts'-- HTTP/1.1
```
- 观察到的差异：
- 截图：`screenshots/01-sqli-01-normal.png`、`screenshots/01-sqli-02-injected.png`

> 注意：`Gifts'--` 能把查询后半句切掉；`Gifts'+OR+1=1--` 是把 `WHERE` 条件变成恒真。两种写法都试一遍，写下区别。

## 3. 复现（Lab ③：布尔盲注）

- 信号是什么（页面出现/消失的是哪段文字）：
- 判定式：
```
Cookie: TrackingId=xxxxxxxx' AND '1'='1     → 有 "Welcome back"
Cookie: TrackingId=xxxxxxxx' AND '1'='2     → 没有
```
- 猜第一个字符：
```
Cookie: TrackingId=xxxxxxxx' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
```
- 用二分把 20 位密码挖出来（脚本：`scripts/blind_sqli_boolean.py`），贴出脚本运行输出：
```
<在这里贴终端输出>
```
- 用时 / 请求数：
- 截图：`screenshots/01-sqli-03-bool.png`、`screenshots/01-sqli-04-script.png`

## 4. PoC

最小可复现的东西：一条 curl 或一段 20 行以内的脚本。要求：**换一台机器、改掉 URL 和 Cookie，能直接跑通**。

```bash
# 在这里放 curl
```

## 5. 修复建议（要说"为什么这样就够"）

- [ ] 参数化查询（Prepared Statement）：为什么它能让 `'` 变回普通字符？
- [ ] 输入白名单（比如 category 只允许枚举值）+ 最小权限数据库账号
- [ ] 为什么"转义引号"不如参数化可靠？

## 6. 卡住记录

| 时间 | 卡在哪 | 怎么解决的 |
|---|---|---|
|  |  |  |

## 7. 三层追问自检

1. 为什么能注入？（数据流：用户输入 → SQL 字符串拼接 → 数据库执行）
2. 我怎么判断有注入？（回显差异 / 布尔差异 / 时间差异，三种信号分别对应什么场景）
3. 修复为什么有效？（语法结构与数据分离，参数永远不参与 SQL 解析）

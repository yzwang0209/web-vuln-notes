#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二分边界演示：把 extract_char() 的每一步打印出来，看清楚 lo/hi 怎么收缩。
不用连靶场，纯本地跑。对比"正确写法"和"lo = mid 的错法"。

python scripts/bisect_trace.py
"""

CHARSET_LO, CHARSET_HI = 32, 126


def trace_correct(target: str):
    """正确写法：lo = mid + 1 / hi = mid"""
    lo, hi = CHARSET_LO, CHARSET_HI
    steps = 0
    print(f"目标字符 = {target!r} (ord={ord(target)})")
    print(f"{'步':<4}{'lo':<6}{'hi':<6}{'mid':<6}{'mid字符':<8}{'mid < 目标?':<12}动作")
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        guess = chr(mid)
        is_less = mid < ord(target)      # 等价于靶场的 "SUBSTRING(...) > mid"
        action = "lo = mid + 1" if is_less else "hi = mid"
        print(f"{steps:<4}{lo:<6}{hi:<6}{mid:<6}{guess:<8}{str(is_less):<12}{action}")
        if is_less:
            lo = mid + 1
        else:
            hi = mid
        if steps > 30:
            print("!! 超过 30 步，异常")
            return None
    print(f"→ {steps} 步收敛，结果 = {chr(lo)!r}\n")
    return chr(lo)


def trace_wrong(target: str):
    """错误写法：lo = mid（当 mid 一直等于 lo 时会死循环）"""
    lo, hi = CHARSET_LO, CHARSET_HI
    steps = 0
    print(f"[错法] 目标字符 = {target!r}")
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        is_less = mid < ord(target)
        if is_less:
            lo = mid          # ← 错在这里
        else:
            hi = mid
        if steps > 200:
            print(f"[错法] 200 步还没收敛：卡在 lo={lo}, hi={hi}, mid={mid} → 死循环\n")
            return None
    print(f"[错法] 收敛，{steps} 步\n")


if __name__ == "__main__":
    for t in ("a", "m", "z", "A", "_", "~"):
        trace_correct(t)
    trace_wrong("a")
    trace_wrong("m")

"""LeetCode 217. 存在重复元素 (Easy)

https://leetcode.cn/problems/contains-duplicate/

题目：给定整数数组，只要存在任一元素出现至少两次就返回 True。

思路：用 set 记录已见元素，命中重复立即返回 True。
也可以直接比较 len(set(nums)) 和 len(nums)，但那样无法提前退出。

复杂度：
- 时间 O(n)
- 空间 O(n)

易错点：
- 空数组返回 False
- 提前返回的写法比全量构造 set 更省时间
"""

from typing import List


def contains_duplicate(nums: List[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


# ========== 闭卷复写区 ==========

def contains_duplicate_practice(nums: List[int]) -> bool:
    # TODO: 闭卷复写
    raise NotImplementedError("先自己写，写不出来再对照上面的实现")


def _run_tests():
    cases = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
        ([], False),
        ([1], False),
    ]
    for nums, expected in cases:
        result = contains_duplicate(nums)
        assert result == expected, f"失败: {nums} 期望{expected} 实际{result}"
        print(f"通过: {nums} -> {result}")
    print("\n参考实现全部测试通过")


if __name__ == "__main__":
    _run_tests()

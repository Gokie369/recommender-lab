"""LeetCode 1. 两数之和 (Easy)

https://leetcode.cn/problems/two-sum/

题目：给定整数数组 nums 和目标值 target，返回和为 target 的两个数的下标。

思路：一次遍历 + 哈希表。遍历时用字典记录「已经见过的值 -> 下标」，
对当前数 num 检查 target - num 是否出现过。用空间换时间，把 O(n^2) 降到 O(n)。

复杂度：
- 时间 O(n)，只遍历一次数组
- 空间 O(n)，最坏情况哈希表存 n 个元素

易错点：
- [3, 3], target=6：必须先查 complement，再存当前值，否则会返回同一个下标
- 无解情况要返回空列表
- 题目要求返回下标，不是返回数值
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}  # {数值: 下标}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ========== 闭卷复写区 ==========
# 复习时遮住上面的实现，在这里重新写一遍，再运行文件末尾的测试验证。

def two_sum_practice(nums: List[int], target: int) -> List[int]:
    # TODO: 闭卷复写两数之和的哈希表解法
    # raise NotImplementedError("先自己写，写不出来再对照上面的实现")
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if  complement in seen:
            return [seen(complement), i]
        seen[num] = i
    return []

def _run_tests():
    cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([1, 2, 3], 100, []),
    ]
    for nums, target, expected in cases:
        result = two_sum(nums, target)
        assert result == expected, f"失败: nums={nums} target={target} 期望{expected} 实际{result}"
        print(f"通过: nums={nums}, target={target} -> {result}")
    print("\n参考实现全部测试通过")


if __name__ == "__main__":
    _run_tests()

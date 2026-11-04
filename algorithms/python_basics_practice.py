"""Python 基础 10 个小练习（第 1 周周二产出）。

每题先自己写，再看参考实现。运行本文件会校验参考实现正确性。
"""

from collections import Counter, defaultdict
import heapq


# 1. 列表去重并保持原顺序
def dedupe(items):
    return list(dict.fromkeys(items))


# 2. 统计元素频次，返回出现最多的元素
def most_common(items):
    return Counter(items).most_common(1)[0][0]


# 3. 按长度分组字符串
def group_by_length(words):
    groups = defaultdict(list)
    for w in words:
        groups[len(w)].append(w)
    return dict(groups)


# 4. 找第 k 大的元素
def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]


# 5. 判断是否为回文串（忽略非字母数字和大小写）
def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


# 6. 反转字典的键值
def invert_dict(d):
    return {v: k for k, v in d.items()}


# 7. 求两个列表的交集
def intersection(a, b):
    return list(set(a) & set(b))


# 8. 把列表按奇偶拆成两个列表
def split_odd_even(nums):
    return [x for x in nums if x % 2 == 0], [x for x in nums if x % 2 != 0]


# 9. 计算阶乘（递归）
def factorial(n):
    if n < 0:
        raise ValueError("阶乘不支持负数")
    return 1 if n <= 1 else n * factorial(n - 1)


# 10. 找两个列表的差集（在 a 中不在 b 中）
def difference(a, b):
    b_set = set(b)
    return [x for x in a if x not in b_set]


def _run_tests():
    assert dedupe([1, 2, 2, 3, 1]) == [1, 2, 3]
    assert most_common([1, 1, 2, 2, 2, 3]) == 2
    assert group_by_length(["a", "bb", "cc"]) == {1: ["a"], 2: ["bb", "cc"]}
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert sorted(intersection([1, 2, 3], [2, 3, 4])) == [2, 3]
    assert split_odd_even([1, 2, 3, 4]) == ([2, 4], [1, 3])
    assert factorial(5) == 120
    assert difference([1, 2, 3], [2]) == [1, 3]
    print("10 个基础练习全部通过")


if __name__ == "__main__":
    _run_tests()

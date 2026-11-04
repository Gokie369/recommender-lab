"""LeetCode 49. 字母异位词分组 (Medium)

https://leetcode.cn/problems/group-anagrams/

题目：给定字符串数组，把互为字母异位词的字符串分到同一组。

思路：异位词排序后结果相同，所以用「排序后的字符串」当哈希键。
也可以用 26 个字母的计数元组当键，避免排序，复杂度更优。

复杂度（排序键法）：
- 时间 O(n * k log k)，n 是字符串个数，k 是最长字符串长度
- 空间 O(n * k)，存所有分组结果

易错点：
- 返回顺序不影响判题，但分组内顺序也不影响
- 键必须是可哈希类型（list 不能当键，tuple 可以）
"""

from collections import defaultdict
from typing import List


def group_anagrams(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())


def group_anagrams_count(strs: List[str]) -> List[List[str]]:
    """计数法：用长度为 26 的字符计数元组当键，不做排序。"""
    groups = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(s)
    return list(groups.values())


# ========== 闭卷复写区 ==========

def group_anagrams_practice(strs: List[str]) -> List[List[str]]:
    # TODO: 闭卷复写
    raise NotImplementedError("先自己写，写不出来再对照上面的实现")


def _normalize(groups):
    return sorted(sorted(g) for g in groups)


def _run_tests():
    cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]
    for strs, expected in cases:
        for fn in (group_anagrams, group_anagrams_count):
            result = fn(strs)
            assert _normalize(result) == _normalize(expected), \
                f"{fn.__name__} 失败: {strs} -> {result}"
        print(f"通过: {strs}")
    print("\n参考实现全部测试通过")


if __name__ == "__main__":
    _run_tests()

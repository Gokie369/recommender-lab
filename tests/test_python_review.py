"""练习自测：检查 python_review.py 里练习区的实现。

运行：
    python tests/test_python_review.py

它会读取 src/python_review.py，逐个调用你的练习实现，并用断言比对结果。
没实现的练习会显示 SKIP；实现了但答错的会显示 FAIL 并给出具体差异。
"""

import sys
import traceback
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import python_review as pr  # noqa: E402


# (练习描述, 调用函数, 测试用例列表)
# 每个用例是 (参数元组, 期望返回值)
CASES = [
    (
        "练习1 去重并保持顺序",
        pr.exercise_1_dedupe,
        [
            (([1, 2, 2, 3, 1],), [1, 2, 3]),
            (([3, 1, 2, 1, 3],), [3, 1, 2]),
            (([],), []),
            (([5],), [5]),
            (([1, 1, 1],), [1]),
            ((["a", "b", "a"],), ["a", "b"]),
        ],
    ),
    (
        "练习2 安全相除",
        pr.exercise_2_safe_divide,
        [
            ((10, 2), 5.0),
            ((10, 0), None),
            ((0, 5), 0.0),
            ((-6, 3), -2.0),
        ],
    ),
    (
        "练习3 统计词频",
        pr.exercise_3_word_count,
        [
            (("a b a",), {"a": 2, "b": 1}),
            (("",), {}),
            (("the the the",), {"the": 3}),
        ],
    ),
]


def check_simple():
    passed = skipped = failed = 0

    for title, fn, cases in CASES:
        print("=" * 58)
        print(title)
        print("=" * 58)

        try:
            args, _ = cases[0]
            fn(*args)
        except NotImplementedError:
            print("  状态: SKIP（还没实现）")
            skipped += 1
            print()
            continue
        except Exception:  # noqa: BLE001
            print("  状态: FAIL（运行时报错）")
            traceback.print_exc()
            failed += 1
            print()
            continue

        ok = True
        for args, expected in cases:
            try:
                actual = fn(*args)
            except Exception as exc:  # noqa: BLE001
                print(f"  FAIL {args} -> 报错 {type(exc).__name__}: {exc}")
                ok = False
                continue
            if actual != expected:
                print(f"  FAIL {args} -> 期望 {expected!r}，实际 {actual!r}")
                ok = False
            else:
                print(f"  ok   {args} -> {actual!r}")

        if ok:
            print("  状态: PASS")
            passed += 1
        else:
            print("  状态: FAIL")
            failed += 1
        print()

    return passed, skipped, failed


def check_movie_class():
    print("=" * 58)
    print("练习4 Movie 类")
    print("=" * 58)
    try:
        Movie = pr.exercise_4_movie()
    except NotImplementedError:
        print("  状态: SKIP（还没实现）")
        return 0, 1, 0
    except Exception:  # noqa: BLE001
        print("  状态: FAIL（运行时报错）")
        traceback.print_exc()
        return 0, 0, 1

    try:
        good = Movie("Toy Story", 5)
        bad = Movie("Jumanji", 2)
        assert good.title == "Toy Story"
        assert good.rating == 5
        assert good.is_good() is True, "rating=5 应为 True"
        assert bad.is_good() is False, "rating=2 应为 False"
        edge = Movie("X", 4)
        assert edge.is_good() is True, "rating=4 应为 True（边界）"
        print("  ok   title/rating/is_good 全部正确")
        print("  状态: PASS")
        return 1, 0, 0
    except AssertionError as exc:
        print(f"  FAIL {exc}")
        print("  状态: FAIL")
        return 0, 0, 1


def main():
    print()
    passed, skipped, failed = check_simple()
    p4, s4, f4 = check_movie_class()
    passed, skipped, failed = passed + p4, skipped + s4, failed + f4

    print("=" * 58)
    print(f"汇总: PASS {passed} | SKIP {skipped} | FAIL {failed}")
    print("=" * 58)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

"""Day 1 步骤 2：Python 核心语法速览。

覆盖每日计划要求的五块内容：
  1. 基本数据类型（int / float / str / bool）
  2. 容器类型（list / tuple / dict / set）
  3. 函数（默认参数、*args、**kwargs）
  4. 类与对象（__init__、实例方法、类属性 vs 实例属性）
  5. 异常处理（try-except-finally、常见异常）

运行：
    python src/python_review.py

文件末尾有 4 个练习，先自己写，再对照 _answers。
"""


def part_1_basic_types() -> None:
    print("=" * 58)
    print("Part 1  基本数据类型")
    print("=" * 58)

    num_int = 42
    num_float = 3.14
    text = "Hello, Python"
    is_true = True

    for value in (num_int, num_float, text, is_true):
        print(f"{value!r:>20}  ->  {type(value).__name__}")

    # 类型转换
    print("\n类型转换:")
    print(f'int("123")   = {int("123")}')
    print(f'float("3.5") = {float("3.5")}')
    print(f'str(42)      = {str(42)!r}')
    print(f'bool(0)      = {bool(0)}  (0/空容器为 False)')


def part_2_containers() -> None:
    print("\n" + "=" * 58)
    print("Part 2  容器类型")
    print("=" * 58)

    my_list = [1, 2, 3, 4, 5]
    my_tuple = (1, 2, 3)
    my_dict = {"name": "Alice", "age": 25, "city": "Beijing"}
    my_set = {1, 2, 3, 3, 3}

    print(f"list  有序可重复: {my_list}")
    print(f"tuple 不可变:     {my_tuple}")
    print(f"dict  键值对:     {my_dict}")
    print(f"set   自动去重:   {my_set}")

    # 关键区别演示
    print("\n关键区别:")
    my_list.append(6)
    print(f"list 可以 append: {my_list}")
    try:
        my_tuple[0] = 99
    except TypeError as exc:
        print(f"tuple 不可修改:   TypeError -> {exc}")

    # 查表：先判存在再取，避免 KeyError
    print(f'\ndict 取值: my_dict["name"] = {my_dict["name"]}')
    print(f'dict 安全取值: my_dict.get("gender", "不存在") = {my_dict.get("gender", "不存在")}')

    # set 常用于去重与存在性判断
    raw = [1, 2, 2, 3, 3, 3]
    print(f"\nlist 去重: {list(set(raw))}（注意：set 不保证顺序）")
    print(f"保持顺序去重: {list(dict.fromkeys(raw))}")
    print(f"存在性判断: 3 in my_set -> {3 in my_set}，O(1)")


def part_3_functions() -> None:
    print("\n" + "=" * 58)
    print("Part 3  函数")
    print("=" * 58)

    def greet(name, greeting="Hello"):
        """带默认参数的函数。"""
        return f"{greeting}, {name}!"

    print(greet("Bob"))
    print(greet("Charlie", "Hi"))
    print(greet("Dave", greeting="Hey"))

    def sum_all(*args):
        """*args 收集位置参数为元组。"""
        return sum(args)

    print(f"\n*args: sum_all(1, 2, 3, 4) = {sum_all(1, 2, 3, 4)}")

    def describe(**kwargs):
        """**kwargs 收集关键字参数为字典。"""
        return ", ".join(f"{k}={v}" for k, v in kwargs.items())

    print(f"**kwargs: describe(name='Ann', age=20) -> {describe(name='Ann', age=20)}")

    print("\n默认参数陷阱（可变对象不要在默认值里写）:")

    def bad_append(item, target=[]):
        target.append(item)
        return target

    print(f"  第一次: {bad_append(1)}")
    print(f"  第二次: {bad_append(2)}  <- 期望 [2] 却累积了！")

    def good_append(item, target=None):
        if target is None:
            target = []
        target.append(item)
        return target

    print(f"  正确写法: {good_append(1)} -> {good_append(2)}")


def part_4_classes() -> None:
    print("\n" + "=" * 58)
    print("Part 4  类与对象")
    print("=" * 58)

    class Movie:
        """类属性：所有实例共享。"""
        source = "MovieLens"

        def __init__(self, title, rating):
            self.title = title      # 实例属性：每个实例独有
            self.rating = rating

        def describe(self):
            return f"《{self.title}》评分 {self.rating}（来源 {Movie.source}）"

        def __repr__(self):
            return f"Movie(title={self.title!r}, rating={self.rating})"

    m1 = Movie("Toy Story", 5)
    m2 = Movie("Jumanji", 3.5)

    print(m1.describe())
    print(m2.describe())
    print(f"\n实例属性: m1.title = {m1.title!r}")
    print(f"类属性:   Movie.source = {Movie.source!r}")

    # 类属性被实例覆盖后，不影响其他实例
    m1.source = "IMDB"
    print(f"覆盖后: m1.source = {m1.source!r}，Movie.source 仍是 {Movie.source!r}")
    print(f"m2.source 不受影响: {m2.source!r}")


def part_5_exceptions() -> None:
    print("\n" + "=" * 58)
    print("Part 5  异常处理")
    print("=" * 58)

    try:
        result = 10 / 0
    except ZeroDivisionError as exc:
        print(f"捕获 ZeroDivisionError: {exc}")
    finally:
        print("finally 无论是否出错都会执行")

    my_dict = {"name": "Alice"}
    print()
    for key in ("name", "gender"):
        try:
            print(f"取 {key}: {my_dict[key]}")
        except KeyError:
            print(f"取 {key}: KeyError -> 键不存在，用 .get() 或先判断")

    print("\n常见异常速查:")
    cases = [
        ("IndexError", lambda: [1, 2][5], "索引越界"),
        ("KeyError", lambda: {"a": 1}["b"], "字典键不存在"),
        ("ValueError", lambda: int("abc"), "值类型对但内容不对"),
        ("TypeError", lambda: 1 + "a", "类型不匹配"),
    ]
    for name, fn, desc in cases:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            print(f"  {name:<12} {desc:<18} -> {exc}")


# ============================================================
# 练习区（先自己写，再看 _answers）
# ============================================================

def exercise_1_dedupe(items):
    """练习 1：对列表去重并保持原顺序。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_1")


def exercise_2_safe_divide(a, b):
    """练习 2：安全相除，除数为 0 时返回 None。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_2")


def exercise_3_word_count(text):
    """练习 3：统计字符串中每个单词出现次数，返回 dict。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_3")


def exercise_4_movie():
    """练习 4：定义一个 Movie 类，含 title/rating 属性和 is_good() 方法（rating>=4 返回 True）。"""
    raise NotImplementedError("自己实现，再对照 _answers.exercise_4")


class _answers:
    """参考资料：写完之后再打开对照。"""

    @staticmethod
    def exercise_1(items):
        return list(dict.fromkeys(items))

    @staticmethod
    def exercise_2(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return None

    @staticmethod
    def exercise_3(text):
        counts = {}
        for word in text.split():
            counts[word] = counts.get(word, 0) + 1
        return counts

    @staticmethod
    def exercise_4():
        class Movie:
            def __init__(self, title, rating):
                self.title = title
                self.rating = rating

            def is_good(self):
                return self.rating >= 4

        return Movie


def main() -> None:
    part_1_basic_types()
    part_2_containers()
    part_3_functions()
    part_4_classes()
    part_5_exceptions()

    print("\n" + "=" * 58)
    print("练习区：实现 exercise_1 ~ exercise_4，再对照 _answers")
    print("=" * 58)


if __name__ == "__main__":
    main()

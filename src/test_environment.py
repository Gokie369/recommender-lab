"""Day 1 步骤 1：开发环境自检。

一次性检查 Python、常用库、pip、Git 版本和 Git 身份配置。
运行：
    python src/test_environment.py

每一项都会打印 OK / FAIL，最后给出总结。FAIL 的处理办法写在每一项后面。
"""

import platform
import subprocess
import sys
from importlib.util import find_spec


RESULTS = []


def record(name: str, passed: bool, detail: str = "", fix: str = "") -> None:
    RESULTS.append((name, passed, fix))
    mark = "OK  " if passed else "FAIL"
    line = f"[{mark}] {name}"
    if detail:
        line += f"  ->  {detail}"
    print(line)
    if not passed and fix:
        print(f"        处理办法: {fix}")


def run_command(args):
    """执行外部命令，返回标准输出；失败返回 None。"""
    try:
        out = subprocess.run(
            args, capture_output=True, text=True, timeout=15, shell=False
        )
        if out.returncode == 0:
            return out.stdout.strip()
        return None
    except (OSError, subprocess.SubprocessError):
        return None


def check_python() -> None:
    version = platform.python_version()
    ok = sys.version_info >= (3, 8)
    record(
        "Python 版本 >= 3.8", ok, f"Python {version}",
        "从 python.org 下载 3.8+ 并勾选 Add to PATH",
    )
    record("Python 解释器路径", True, sys.executable)
    record("操作系统", True, f"{platform.system()} {platform.release()}")


def check_libraries() -> None:
    # (import 名称, 展示名, 是否必需)
    packages = [
        ("numpy", "NumPy", True),
        ("pandas", "Pandas", True),
        ("jupyter", "Jupyter", True),
        ("sklearn", "scikit-learn", False),
        ("matplotlib", "Matplotlib", False),
    ]
    for module_name, display_name, required in packages:
        found = find_spec(module_name) is not None
        if found:
            try:
                mod = __import__(module_name)
                version = getattr(mod, "__version__", "已安装")
                record(f"{display_name} 可用", True, str(version))
            except Exception as exc:  # noqa: BLE001
                record(f"{display_name} 可导入", False, str(exc),
                       f"pip install --upgrade {display_name.lower()}")
        else:
            level = "" if required else "（可选）"
            record(
                f"{display_name} 可用{level}", False, "未安装",
                f"pip install {module_name if module_name != 'sklearn' else 'scikit-learn'}",
            )


def check_git() -> None:
    version = run_command(["git", "--version"])
    record("Git 可用", version is not None, version or "未找到 git",
           "从 git-scm.com 下载安装")

    name = run_command(["git", "config", "--global", "user.name"])
    record(
        "Git user.name 已配置", bool(name), name or "未配置",
        'git config --global user.name "你的名字"',
    )

    email = run_command(["git", "config", "--global", "user.email"])
    record(
        "Git user.email 已配置", bool(email), email or "未配置",
        'git config --global user.email "你的邮箱"',
    )


def main() -> None:
    print("=" * 60)
    print("Day 1 · 开发环境自检")
    print("=" * 60)

    check_python()
    print()
    check_libraries()
    print()
    check_git()

    print("\n" + "=" * 60)
    total = len(RESULTS)
    failed = [name for name, passed, _ in RESULTS if not passed]
    required_failed = [name for name, passed, fix in RESULTS if not passed and fix]

    if not required_failed:
        print(f"全部通过（{total} 项检查，{total - len(failed)} 项 OK）")
        print("可以进入步骤 2：Python 核心语法速览。")
    else:
        print(f"共 {total} 项检查，{len(failed)} 项需要处理：")
        for name in failed:
            print(f"  - {name}")
        print("\n按上面每项给出的『处理办法』修好后，重新运行本脚本。")

    print("=" * 60)
    return 0 if not required_failed else 1


if __name__ == "__main__":
    sys.exit(main())

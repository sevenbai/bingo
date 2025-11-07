#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试猜数字宾果游戏的核心功能
"""

from number_guessing_bingo import NumberGuessingBingo


def test_validate_code():
    """测试密码验证功能"""
    game = NumberGuessingBingo()

    print("测试密码验证功能...")

    # 有效的密码
    assert game.validate_code("0123") == True
    assert game.validate_code("9876") == True
    assert game.validate_code("2674") == True

    # 无效的密码
    assert game.validate_code("1123") == False  # 有重复数字
    assert game.validate_code("123") == False   # 长度不够
    assert game.validate_code("12345") == False # 长度太长
    assert game.validate_code("12ab") == False  # 包含非数字
    assert game.validate_code("") == False      # 空字符串

    print("✓ 密码验证功能测试通过！")


def test_compare_codes():
    """测试密码比对功能"""
    game = NumberGuessingBingo()

    print("\n测试密码比对功能...")

    # 测试案例1: 密码 2674, 猜测 1276
    secret = [2, 6, 7, 4]
    guess = [1, 2, 7, 6]
    a, b = game.compare_codes(secret, guess)
    assert a == 1, f"期望 A=1, 实际 A={a}"  # 7在正确位置
    assert b == 2, f"期望 B=2, 实际 B={b}"  # 2和6存在但位置不对
    print(f"  案例1: 密码=2674, 猜测=1276 → {a}A{b}B ✓")

    # 测试案例2: 完全正确
    secret = [1, 2, 3, 4]
    guess = [1, 2, 3, 4]
    a, b = game.compare_codes(secret, guess)
    assert a == 4 and b == 0
    print(f"  案例2: 密码=1234, 猜测=1234 → {a}A{b}B ✓")

    # 测试案例3: 完全错误
    secret = [0, 1, 2, 3]
    guess = [4, 5, 6, 7]
    a, b = game.compare_codes(secret, guess)
    assert a == 0 and b == 0
    print(f"  案例3: 密码=0123, 猜测=4567 → {a}A{b}B ✓")

    # 测试案例4: 数字都对但位置全错
    secret = [1, 2, 3, 4]
    guess = [4, 3, 2, 1]
    a, b = game.compare_codes(secret, guess)
    assert a == 0 and b == 4
    print(f"  案例4: 密码=1234, 猜测=4321 → {a}A{b}B ✓")

    # 测试案例5: 混合情况
    secret = [5, 6, 7, 8]
    guess = [5, 7, 9, 8]
    a, b = game.compare_codes(secret, guess)
    assert a == 2 and b == 1  # 5和8位置对，7存在但位置错
    print(f"  案例5: 密码=5678, 猜测=5798 → {a}A{b}B ✓")

    print("✓ 密码比对功能测试通过！")


def test_format_result():
    """测试结果格式化功能"""
    game = NumberGuessingBingo()

    print("\n测试结果格式化功能...")

    assert game.format_result(0, 0) == "0A0B"
    assert game.format_result(1, 2) == "1A2B"
    assert game.format_result(4, 0) == "4A0B"
    assert game.format_result(2, 2) == "2A2B"

    print("✓ 结果格式化功能测试通过！")


def test_generate_all_possible_codes():
    """测试生成所有可能密码的功能"""
    game = NumberGuessingBingo()

    print("\n测试生成所有可能密码...")

    codes = game.generate_all_possible_codes()

    # 应该有 10P4 = 10*9*8*7 = 5040 种组合
    assert len(codes) == 5040, f"期望5040种组合，实际{len(codes)}种"

    # 检查每个密码都是4位不重复数字
    for code in codes:
        assert len(code) == 4
        assert len(set(code)) == 4
        assert all(0 <= d <= 9 for d in code)

    print(f"✓ 生成了 {len(codes)} 种可能的密码组合！")


def test_ai_strategy():
    """测试AI策略的基本功能"""
    game = NumberGuessingBingo()

    print("\n测试AI策略...")

    # 初始化可能的密码空间
    game.possible_codes = game.generate_all_possible_codes()
    game.human_secret = [1, 2, 3, 4]

    # 第一次猜测
    guess1 = game.ai_make_guess()
    assert len(guess1) == 4
    assert len(set(guess1)) == 4
    print(f"  AI第1次猜测: {''.join(map(str, guess1))}")

    # 记录第一次猜测的结果
    a, b = game.compare_codes(game.human_secret, guess1)
    game.ai_guesses.append((guess1, (a, b)))
    print(f"  结果: {a}A{b}B")

    # 第二次猜测
    guess2 = game.ai_make_guess()
    assert len(guess2) == 4
    assert len(set(guess2)) == 4
    print(f"  AI第2次猜测: {''.join(map(str, guess2))}")

    a, b = game.compare_codes(game.human_secret, guess2)
    game.ai_guesses.append((guess2, (a, b)))
    print(f"  结果: {a}A{b}B")

    print("✓ AI策略基本功能测试通过！")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("开始测试猜数字宾果游戏")
    print("=" * 60)

    try:
        test_validate_code()
        test_compare_codes()
        test_format_result()
        test_generate_all_possible_codes()
        test_ai_strategy()

        print("\n" + "=" * 60)
        print("✓ 所有测试通过！游戏核心功能正常。")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

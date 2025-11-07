#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI策略演示程序
展示AI如何逐步缩小搜索空间
"""

from number_guessing_bingo import NumberGuessingBingo


def demo_ai_thinking():
    """演示AI的思考过程"""
    game = NumberGuessingBingo()

    # 设定一个示例密码
    secret = [2, 6, 7, 4]
    print("=" * 70)
    print("AI策略演示：看AI如何猜中密码 [2, 6, 7, 4]")
    print("=" * 70)
    print()

    # 初始化
    game.possible_codes = game.generate_all_possible_codes()
    print(f"初始状态：")
    print(f"  搜索空间大小: {len(game.possible_codes)} 种可能")
    print(f"  密码范围: 所有4位不重复数字组合")
    print()

    round_num = 1

    while True:
        print("-" * 70)
        print(f"第 {round_num} 轮")
        print("-" * 70)

        # AI猜测
        guess = game.ai_make_guess()
        guess_str = ''.join(map(str, guess))
        print(f"AI猜测: {guess_str}")

        # 比对结果
        a, b = game.compare_codes(secret, guess)
        result = game.format_result(a, b)
        print(f"结果: {result}")

        # 记录猜测
        game.ai_guesses.append((guess, (a, b)))

        # 过滤搜索空间
        game.possible_codes = [
            code for code in game.possible_codes
            if all(
                game.compare_codes(code, g) == r
                for g, r in game.ai_guesses
            )
        ]

        print(f"剩余可能: {len(game.possible_codes)} 种")

        # 显示一些剩余的可能密码（最多5个）
        if len(game.possible_codes) <= 20:
            print(f"剩余候选密码:")
            for i, code in enumerate(game.possible_codes[:10], 1):
                code_str = ''.join(map(str, code))
                if code == secret:
                    print(f"  {i}. {code_str} ← 真实密码")
                else:
                    print(f"  {i}. {code_str}")
            if len(game.possible_codes) > 10:
                print(f"  ... 还有 {len(game.possible_codes) - 10} 个")

        # 解释本轮获得的信息
        print(f"\n本轮约束分析:")
        if a > 0:
            print(f"  ✓ 有 {a} 个数字位置完全正确")
        if b > 0:
            print(f"  ✓ 有 {b} 个数字存在但位置错误")
        if a == 0 and b == 0:
            print(f"  ✓ 猜测的4个数字都不在密码中")

        # 检查是否猜中
        if a == 4:
            print()
            print("=" * 70)
            print(f"🎉 AI在第 {round_num} 轮猜中了密码！")
            print(f"总猜测次数: {round_num}")
            print(f"搜索空间缩减: 5040 → 1 (缩减了 {(1 - 1/5040) * 100:.2f}%)")
            print("=" * 70)
            break

        print()
        round_num += 1

        # 防止无限循环
        if round_num > 15:
            print("演示结束（超过15轮）")
            break


def demo_constraint_filtering():
    """演示约束过滤的工作原理"""
    game = NumberGuessingBingo()

    print("\n" + "=" * 70)
    print("约束过滤演示")
    print("=" * 70)
    print()

    print("假设我们猜测 [0, 1, 2, 3]，得到结果 1A0B")
    print("这意味着：有1个数字位置正确，0个数字存在但位置错误")
    print()

    # 生成所有可能的密码
    all_codes = game.generate_all_possible_codes()
    print(f"原始搜索空间: {len(all_codes)} 种可能")
    print()

    # 应用约束
    guess = [0, 1, 2, 3]
    target_result = (1, 0)  # 1A0B

    filtered_codes = [
        code for code in all_codes
        if game.compare_codes(code, guess) == target_result
    ]

    print(f"约束条件: compare_codes(密码, [0,1,2,3]) == (1, 0)")
    print(f"过滤后搜索空间: {len(filtered_codes)} 种可能")
    print(f"缩减比例: {(1 - len(filtered_codes) / len(all_codes)) * 100:.1f}%")
    print()

    print("满足约束的前10个密码示例:")
    for i, code in enumerate(filtered_codes[:10], 1):
        code_str = ''.join(map(str, code))
        # 分析为什么满足约束
        a, b = game.compare_codes(code, guess)
        print(f"  {i}. {code_str} → 比对 [0,1,2,3] = {a}A{b}B ✓")

    print()
    print("分析：这些密码都有且仅有1个数字与 [0,1,2,3] 位置匹配，")
    print("      并且没有其他数字存在于密码中。")


def demo_search_space_reduction():
    """演示搜索空间如何快速缩减"""
    game = NumberGuessingBingo()

    print("\n" + "=" * 70)
    print("搜索空间缩减速度演示")
    print("=" * 70)
    print()

    secret = [5, 6, 7, 8]
    game.possible_codes = game.generate_all_possible_codes()

    guesses = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [9, 7, 5, 6],
        [5, 6, 7, 8],
    ]

    print(f"真实密码: {''.join(map(str, secret))}")
    print(f"初始搜索空间: {len(game.possible_codes)}")
    print()

    for i, guess in enumerate(guesses, 1):
        a, b = game.compare_codes(secret, guess)
        result = game.format_result(a, b)
        game.ai_guesses.append((guess, (a, b)))

        # 过滤
        game.possible_codes = [
            code for code in game.possible_codes
            if all(
                game.compare_codes(code, g) == r
                for g, r in game.ai_guesses
            )
        ]

        guess_str = ''.join(map(str, guess))
        reduction = (1 - len(game.possible_codes) / 5040) * 100

        print(f"第{i}轮: 猜测 {guess_str} → {result}")
        print(f"  剩余: {len(game.possible_codes):4d} 种 (已缩减 {reduction:.1f}%)")

        if a == 4:
            print(f"\n🎉 在第 {i} 轮猜中！")
            break

        print()


def main():
    """主函数"""
    print("\n" + "🤖 " * 35)
    print("AI策略演示程序")
    print("🤖 " * 35)

    # 演示1：完整的AI思考过程
    demo_ai_thinking()

    # 演示2：约束过滤原理
    demo_constraint_filtering()

    # 演示3：搜索空间缩减速度
    demo_search_space_reduction()

    print("\n" + "=" * 70)
    print("演示结束！")
    print("=" * 70)
    print("\n关键要点：")
    print("1. AI维护一个包含所有可能密码的搜索空间")
    print("2. 每次猜测后，使用约束条件过滤掉不符合的密码")
    print("3. 搜索空间快速缩减（每轮通常缩减60-80%）")
    print("4. 平均5-7次猜测即可找到答案")
    print()


if __name__ == "__main__":
    main()

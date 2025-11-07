#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猜数字宾果游戏 (Number Guessing Bingo Game)
人类 vs AI 比赛，看谁先猜中对方的4位不重复数字密码
"""

import random
from typing import List, Tuple, Set
import sys


class NumberGuessingBingo:
    """猜数字宾果游戏类"""

    def __init__(self):
        self.human_secret = []  # 人类的密码
        self.ai_secret = []     # AI的密码
        self.human_guesses = []  # 人类的猜测历史 [(guess, result)]
        self.ai_guesses = []     # AI的猜测历史 [(guess, result)]
        self.possible_codes = []  # AI可能的答案空间

    def validate_code(self, code: str) -> bool:
        """验证密码是否合法（4位数字，不重复）"""
        if len(code) != 4:
            return False
        if not code.isdigit():
            return False
        if len(set(code)) != 4:  # 检查是否有重复数字
            return False
        return True

    def compare_codes(self, secret: List[int], guess: List[int]) -> Tuple[int, int]:
        """
        比对密码和猜测，返回 (A, B)
        A: 数字和位置都正确的个数
        B: 数字正确但位置不对的个数
        """
        a_count = 0
        b_count = 0

        for i in range(4):
            if guess[i] == secret[i]:
                a_count += 1
            elif guess[i] in secret:
                b_count += 1

        return a_count, b_count

    def format_result(self, a: int, b: int) -> str:
        """格式化结果为 ?A?B 格式"""
        return f"{a}A{b}B"

    def generate_all_possible_codes(self) -> List[List[int]]:
        """生成所有可能的4位不重复数字组合"""
        codes = []
        for a in range(10):
            for b in range(10):
                if b == a:
                    continue
                for c in range(10):
                    if c == a or c == b:
                        continue
                    for d in range(10):
                        if d == a or d == b or d == c:
                            continue
                        codes.append([a, b, c, d])
        return codes

    def ai_generate_secret(self) -> List[int]:
        """AI生成密码"""
        digits = list(range(10))
        random.shuffle(digits)
        return digits[:4]

    def ai_make_guess(self) -> List[int]:
        """
        AI智能猜测策略
        使用约束满足和信息熵最大化策略
        """
        # 第一次猜测，使用启发式策略
        if not self.ai_guesses:
            # 第一次猜测使用 0123，这样可以快速获得信息
            return [0, 1, 2, 3]

        # 根据历史猜测结果过滤可能的密码
        self.possible_codes = [
            code for code in self.possible_codes
            if all(
                self.compare_codes(code, guess) == result
                for guess, result in self.ai_guesses
            )
        ]

        if not self.possible_codes:
            print("错误：没有符合条件的密码！")
            return [0, 0, 0, 0]

        # 如果只剩下一个可能的密码，直接猜它
        if len(self.possible_codes) == 1:
            return self.possible_codes[0]

        # 使用信息熵策略：选择能最好区分剩余可能性的猜测
        # 简化版本：随机选择一个尚未猜过的可能密码
        for code in self.possible_codes:
            if code not in [g[0] for g in self.ai_guesses]:
                return code

        # 如果所有可能的都猜过了，随机选一个
        return random.choice(self.possible_codes)

    def setup_game(self):
        """设置游戏"""
        print("=" * 60)
        print("欢迎来到猜数字宾果游戏！")
        print("=" * 60)
        print()
        print("游戏规则：")
        print("1. 你和AI都要设定4个0到9不重复的数字作为密码")
        print("2. 双方轮流猜测对方的密码")
        print("3. 每次猜测后会得到 ?A?B 的反馈")
        print("   - A: 数字和位置都正确的个数")
        print("   - B: 数字正确但位置错误的个数")
        print("4. 先得到 4A0B 的一方获胜！")
        print()
        print("=" * 60)
        print()

        # 人类设置密码
        while True:
            human_input = input("请输入你的4位密码（0-9不重复的数字）: ").strip()
            if self.validate_code(human_input):
                self.human_secret = [int(d) for d in human_input]
                print("✓ 密码设置成功！")
                break
            else:
                print("✗ 无效的密码！请确保是4位不重复的数字。")

        print()

        # AI设置密码
        self.ai_secret = self.ai_generate_secret()
        print("AI已设置好密码。")
        print()

        # 初始化AI的可能答案空间
        self.possible_codes = self.generate_all_possible_codes()
        print(f"游戏开始！共有 {len(self.possible_codes)} 种可能的密码组合。")
        print("=" * 60)
        print()

    def human_turn(self) -> bool:
        """
        人类回合
        返回 True 表示人类获胜，False 表示继续游戏
        """
        print("\n" + "=" * 60)
        print(f"第 {len(self.human_guesses) + 1} 轮 - 你的回合")
        print("=" * 60)

        # 显示历史猜测
        if self.human_guesses:
            print("\n你的猜测历史：")
            for i, (guess, result) in enumerate(self.human_guesses, 1):
                guess_str = ''.join(map(str, guess))
                print(f"  第{i}次: {guess_str} -> {result}")
            print()

        # 人类猜测
        while True:
            guess_input = input("请输入你的猜测（4位不重复数字）: ").strip()
            if self.validate_code(guess_input):
                guess = [int(d) for d in guess_input]
                break
            else:
                print("✗ 无效的猜测！请确保是4位不重复的数字。")

        # 比对结果
        a, b = self.compare_codes(self.ai_secret, guess)
        result = self.format_result(a, b)
        self.human_guesses.append((guess, result))

        print(f"\n结果: {result}")

        # 检查是否获胜
        if a == 4:
            print("\n" + "=" * 60)
            print("🎉 恭喜！你猜中了AI的密码！")
            print(f"AI的密码是: {''.join(map(str, self.ai_secret))}")
            print(f"你用了 {len(self.human_guesses)} 次猜测")
            print("=" * 60)
            return True

        return False

    def ai_turn(self) -> bool:
        """
        AI回合
        返回 True 表示AI获胜，False 表示继续游戏
        """
        print("\n" + "=" * 60)
        print(f"第 {len(self.ai_guesses) + 1} 轮 - AI的回合")
        print("=" * 60)

        # 显示AI的历史猜测
        if self.ai_guesses:
            print("\nAI的猜测历史：")
            for i, (guess, result) in enumerate(self.ai_guesses, 1):
                guess_str = ''.join(map(str, guess))
                print(f"  第{i}次: {guess_str} -> {result}")
            print()

        # AI猜测
        guess = self.ai_make_guess()
        guess_str = ''.join(map(str, guess))
        print(f"AI猜测: {guess_str}")

        # 比对结果
        a, b = self.compare_codes(self.human_secret, guess)
        result = self.format_result(a, b)
        self.ai_guesses.append((guess, (a, b)))

        print(f"结果: {result}")

        # 显示AI剩余可能的密码数量
        remaining = len([
            code for code in self.possible_codes
            if all(
                self.compare_codes(code, g) == r
                for g, r in self.ai_guesses
            )
        ])
        print(f"(AI剩余可能的密码数: {remaining})")

        # 检查是否获胜
        if a == 4:
            print("\n" + "=" * 60)
            print("💻 AI猜中了你的密码！")
            print(f"你的密码是: {''.join(map(str, self.human_secret))}")
            print(f"AI用了 {len(self.ai_guesses)} 次猜测")
            print("=" * 60)
            return True

        return False

    def play(self):
        """主游戏循环"""
        self.setup_game()

        round_num = 1
        while True:
            print(f"\n{'#' * 60}")
            print(f"第 {round_num} 轮开始")
            print(f"{'#' * 60}")

            # 人类回合
            if self.human_turn():
                break

            # AI回合
            if self.ai_turn():
                break

            round_num += 1

            # 询问是否继续
            print("\n按 Enter 继续下一轮，或输入 'quit' 退出...")
            user_input = input().strip().lower()
            if user_input == 'quit':
                print("\n游戏已退出。")
                break

        print("\n游戏结束！感谢游玩！")


def main():
    """主函数"""
    game = NumberGuessingBingo()
    game.play()


if __name__ == "__main__":
    main()

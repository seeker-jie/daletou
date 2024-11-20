import os
import asyncio
import aiohttp
from telegram import Bot
from typing import Dict, Optional, List


class LotteryNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = "https://api.huiniao.top/interface/home/lotteryHistory"
        self.bot = Bot(self.bot_token)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """支持异步上下文管理器"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """关闭会话"""
        if self.session:
            await self.session.close()

    async def get_lottery_result(self, lottery_type: str = "dlt") -> Optional[Dict]:
        """异步获取彩票开奖结果"""
        params = {
            "type": lottery_type,
            "page": 1,
            "limit": 1
        }

        try:
            async with self.session.get(self.base_url, params=params) as response:
                data = await response.json()

                if data["code"] == 1:
                    return {
                        "latest": data["data"]["last"],
                        "history": data["data"]["data"]["list"][0] if data["data"]["data"]["list"] else None
                    }
                else:
                    print(f"API返回错误: {data['info']}")
                    return None

        except Exception as e:
            print(f"获取开奖结果失败: {str(e)}")
            return None

    @staticmethod
    def format_numbers(latest: Dict) -> tuple[List[str], List[str]]:
        """格式化号码"""
        numbers = [
            latest.get("one", ""),
            latest.get("two", ""),
            latest.get("three", ""),
            latest.get("four", ""),
            latest.get("five", ""),
            latest.get("six", ""),  # 后区
            latest.get("seven", "")  # 后区
        ]

        # 过滤掉空值并转为字符串
        numbers = [str(n) for n in numbers if n != ""]
        # 补足位数为两位
        numbers = [n.zfill(2) for n in numbers]
        return numbers[:5], numbers[5:7]

    def format_dlt_message(self, result: Dict) -> str:
        """格式化大乐透开奖消息"""
        if not result or not result["latest"]:
            return "获取开奖信息失败"

        latest = result["latest"]
        front_nums, back_nums = self.format_numbers(latest)

        message = (
            f"🎯 *大乐透第{latest['code']}期开奖结果*\n\n"
            f"📅 开奖日期：{latest['day']}\n"
            f"⏰ 开奖时间：{latest['open_time']}\n\n"
            f"🔵 前区号码：*{' '.join(front_nums)}*\n"
            f"🔴 后区号码：*{' '.join(back_nums)}*\n\n"
            f"📆 下期开奖：{latest['next_open_time']}\n"
            f"📋 下期期号：{latest['next_code']}"
        )
        return message

    async def send_notification(self, message: str):
        """发送 Telegram 通知"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            print("通知发送成功")
        except Exception as e:
            print(f"发送通知失败: {str(e)}")

    async def run(self):
        """运行通知程序"""
        try:
            # 获取大乐透开奖结果
            dlt_result = await self.get_lottery_result("dlt")
            if dlt_result:
                message = self.format_dlt_message(dlt_result)
                await self.send_notification(message)
        except Exception as e:
            print(f"运行出错: {str(e)}")


async def main():
    async with LotteryNotifier() as notifier:
        await notifier.run()


if __name__ == "__main__":
    asyncio.run(main())

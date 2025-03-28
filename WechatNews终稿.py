import asyncio
import websockets
from wxauto import WeChat
import logging
from datetime import datetime  # 导入 datetime 模块
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 初始化 WeChat
wx = WeChat()

WEBSOCKET_SERVER_URL = "ws://localhost:1234"

async def websocket_client():
    """
    WebSocket 客户端
    """
    while True:
        try:
            async with websockets.connect(WEBSOCKET_SERVER_URL) as websocket:
                logging.info("✅ 客户端已连接到服务器")

                while True:
                    # 监听微信消息
                    msgs = wx.GetNextNewMessage()
                    if msgs:
                        logging.info("🟢 wxauto 检测到新消息！")
                        for chat, one_msgs in msgs.items():
                            for msg in one_msgs:
                                if hasattr(msg, 'content'):
                                    # 获取发送者和时间
                                    sender = chat  # 发送者是聊天名称
                                    content = msg.content  # 消息内容
                                    time = datetime.now().strftime("%H:%M")  # 当前时间

                                    # 构造消息对象
                                    message_data = {
                                        "sender": sender,
                                        "content": content,
                                        "time": time
                                    }

                                    # 发送消息到 WebSocket 服务端
                                    await websocket.send(json.dumps(message_data,ensure_ascii=False))
                                    logging.info(f"📤 发送到 WebSocket: {message_data}")

                    else:
                        logging.info("⚠️ 未检测到新消息")

                    # 每 2 秒检测一次
                    await asyncio.sleep(2)

        except Exception as e:
            logging.error(f"❌ WebSocket 连接失败: {e}")
            await asyncio.sleep(5)  # 重试间隔

async def main():
    """
    主函数
    """
    await websocket_client()

if __name__ == "__main__":
    asyncio.run(main())

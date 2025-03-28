import asyncio
import websockets
import logging
import json  # 导入 json 模块

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 用于存储所有连接的客户端 WebSocket
connected_clients = set()

async def handle_connection(websocket, *args):
    """
    处理 WebSocket 连接
    :param websocket: WebSocket 连接对象
    :param args: 可变参数，包含 path 和其他传递的内容
    """
    # 打印所有传递的参数
    logging.info(f"New connection established, arguments: {args}")

    # 将客户端 WebSocket 加入到连接池
    connected_clients.add(websocket)
    logging.info("✅ 新的 WebSocket 连接已建立")

    try:
        async for message in websocket:
            # 当收到消息时，打印到终端
            logging.info(f"📥 收到消息: {message}")

            # 将收到的消息广播给所有连接的客户端（直接广播原始消息）
            await broadcast_message(message)  # 直接传递原始消息

    except websockets.ConnectionClosed as e:
        logging.info(f"❌ WebSocket 连接已关闭: {e}")
    finally:
        # 移除断开连接的客户端
        connected_clients.remove(websocket)

async def broadcast_message(message):
    """将消息广播给所有已连接的客户端"""
    # 直接发送原始消息，无需重新包装
    for client in connected_clients:
        try:
            await client.send(message)  # 直接发送原始消息
            logging.info(f"📤 广播消息: {message}")
        except websockets.ConnectionClosed:
            connected_clients.remove(client)

async def start_websocket_server():
    """
    启动 WebSocket 服务器
    """
    server = await websockets.serve(
        handle_connection,  # 直接传递函数
        "localhost", 1234
    )
    logging.info("🚀 WebSocket 服务器已启动，正在监听 ws://localhost:1234")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())

import asyncio
import aiohttp
import time
from urllib.parse import urlencode  # 用来构造 URL 查询参数


async def fetch_data(url, a, b):
    data = {'a': a, 'b': b}
    headers = {"Content-Type": "application/json"}  # 关键点！！！
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.text()


def async_fun():
    while True:
        print("hello")
        time.sleep(1)


async def main():
    url = "http://127.0.0.1:5000/remote"  # 替换为实际的 URL
    a = 10
    b = 20
    # task1 = fetch_data(url, a, b)
    # fetch_task = asyncio.create_task(fetch_data(
    #     url, a, b))  # 创建一个异步任务，并放到后台运行，等到需要结果时再等待
    fetch_task = fetch_data(url, a, b)
    # background_task = asyncio.create_task(async_fun())
    print("Doing other task...")
    # 执行其他任务
    # 模拟其他异步操作
    for i in range(3):
        print(f"Other task step {i}")
        await asyncio.sleep(0.5)

    # 可选：等待 fetch_data 完成（如果不需结果，可删除此部分）
    response_text = await fetch_task
    print("Fetch completed:", response_text)

# 执行异步任务
asyncio.run(main())

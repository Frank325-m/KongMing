#!/usr/bin/env python3
"""
测试SSE连接是否正常工作的脚本
"""

import asyncio
import aiohttp
import sys

async def test_sse_connection():
    """测试SSE连接"""
    url = "http://localhost:8000/chat-stream?question=测试SSE连接"
    
    print(f"测试SSE连接: {url}")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Accept": "text/event-stream"}) as response:
                print(f"状态码: {response.status}")
                print(f"Content-Type: {response.headers.get('Content-Type')}")
                
                if response.status == 200:
                    print("\n开始接收流式数据...")
                    print("-" * 30)
                    
                    # 读取前几行数据
                    count = 0
                    async for line in response.content:
                        if count >= 5:  # 只读取前5行
                            break
                        if line:
                            decoded_line = line.decode('utf-8').strip()
                            if decoded_line:
                                print(f"收到: {decoded_line[:100]}...")
                                count += 1
                    
                    print("\n[PASS] SSE连接测试成功！")
                    return 0
                else:
                    print(f"\n[FAIL] 请求失败，状态码: {response.status}")
                    return 1
                    
    except Exception as e:
        print(f"\n[ERROR] 连接错误: {e}")
        return 1

async def test_get_endpoint():
    """测试GET端点"""
    url = "http://localhost:8000/"
    
    print(f"\n测试GET端点: {url}")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"状态码: {response.status}")
                data = await response.json()
                print(f"响应: {data}")
                
                if response.status == 200:
                    print("[PASS] GET端点测试成功！")
                    return 0
                else:
                    print("[FAIL] GET端点测试失败")
                    return 1
                    
    except Exception as e:
        print(f"[ERROR] 连接错误: {e}")
        return 1

async def main():
    """主测试函数"""
    print("=== 后端API测试 ===\n")
    
    # 测试1: 基础GET端点
    result1 = await test_get_endpoint()
    
    # 测试2: SSE连接
    result2 = await test_sse_connection()
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"GET端点: {'[PASS] 通过' if result1 == 0 else '[FAIL] 失败'}")
    print(f"SSE连接: {'[PASS] 通过' if result2 == 0 else '[FAIL] 失败'}")
    
    if result1 == 0 and result2 == 0:
        print("\n[SUCCESS] 所有测试通过！")
        return 0
    else:
        print("\n[WARNING] 部分测试失败")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
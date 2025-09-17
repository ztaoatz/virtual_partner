#!/usr/bin/env python3
import requests
import json

def test_emotion_trend_api():
    print("=== 测试情绪趋势图API修复 ===")
    
    # 使用已知存在的用户ID进行测试
    test_users = [
        {
            "name": "li",
            "user_id": "44852831-3cad-4ed6-9857-8e796c5c334c",
            "has_diary": True
        },
        {
            "name": "zhnagtao", 
            "user_id": "26368a8b-03cd-4f64-b73e-c37dcb0d5f0e",
            "has_diary": True
        },
        {
            "name": "不存在的用户",
            "user_id": "12345678-1234-1234-1234-123456789abc",
            "has_diary": False
        }
    ]
    
    base_url = "http://127.0.0.1:8000"
    
    for user in test_users:
        print(f"\n--- 测试用户: {user['name']} ---")
        print(f"用户ID: {user['user_id']}")
        
        try:
            # 测试情绪趋势API
            url = f"{base_url}/emotion-trend/"
            params = {
                "user_id": user['user_id'],
                "days": 10
            }
            
            print(f"请求URL: {url}")
            print(f"请求参数: {params}")
            
            response = requests.get(url, params=params, timeout=10)
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ API调用成功")
                print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if data.get('success'):
                    trend_data = data.get('trend_data', [])
                    print(f"✓ 获取到 {len(trend_data)} 条趋势数据")
                    if trend_data:
                        print(f"最新日记日期: {trend_data[-1]['date']}")
                        print(f"情绪分值范围: {min(item['emotion_score'] for item in trend_data)} - {max(item['emotion_score'] for item in trend_data)}")
                else:
                    print(f"❌ API返回失败: {data}")
                    
            elif response.status_code == 404:
                print(f"❌ API端点不存在 (404)")
                print(f"响应内容: {response.text}")
                
            elif response.status_code == 500:
                print(f"❌ 服务器内部错误 (500)")
                try:
                    error_data = response.json()
                    print(f"错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"原始错误响应: {response.text}")
                    
            else:
                print(f"❌ 未预期的状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败 - Django服务器可能未启动")
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时")
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    test_emotion_trend_api()

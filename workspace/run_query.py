import requests

def query(user_query):
    url = "http://localhost:8000/query_stockprice"
    payload = {
        "user_query": user_query
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()['data']['response']
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    result = query("平安银行最近20天股价")
    print(result)

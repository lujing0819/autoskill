import requests
import sys

 
service_names=["stockinfo_agent","stockprice_agent","stocknews_agent","stockposition_agent","stocksimilar_agent","stockfinancial_agent"]
for name in service_names:
    url = f"http://localhost:8000/{name}"
    response = requests.post(url, json={"user_query":"平安银行"})
    result=response.json()
    print (result)
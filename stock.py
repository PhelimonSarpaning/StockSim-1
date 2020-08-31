import requests 

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"

querystring = {"interval":"5m","region":"US","symbol":"IBM","lang":"en","range":"1d"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "48cd5a1b82msh073f810ab2c4614p18e96djsn5ef997c07bbf"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response = response.json()

print(response['chart']['result'][0]['meta']['regularMarketPrice'])

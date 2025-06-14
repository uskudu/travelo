import requests

from app.utils import countries

all_cities = []

url = "https://countriesnow.space/api/v0.1/countries/cities"


for cnt in countries.countries:
    if len(all_cities) > 122:
        break
    payload = {"country": cnt}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get("error") is False:
            all_cities.extend(data["data"])
        else:
            print(f"❌ Ошибка от API для страны: {cnt} — {data.get('msg')}")
    else:
        print(f"❌ HTTP ошибка для страны: {cnt} — статус {response.status_code}")

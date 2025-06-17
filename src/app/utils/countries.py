import requests


def iso2_to_emoji_flag(iso2: str) -> str:
    iso2 = iso2.upper()
    OFFSET = 0x1F1E6

    first_char = chr(OFFSET + ord(iso2[0]) - ord("A"))
    second_char = chr(OFFSET + ord(iso2[1]) - ord("A"))
    return first_char + second_char


def fetch_countries():
    url = "https://countriesnow.space/api/v0.1/countries/iso"
    response = requests.get(url)

    data = response.json()
    raw_countries = data["data"]

    result = []
    for country in raw_countries:
        iso2 = country["Iso2"]
        title = country["name"]
        flag = iso2_to_emoji_flag(iso2)
        result.extend([{"iso2": iso2, "title": title, "flag": flag}])

    return result


countries = fetch_countries()

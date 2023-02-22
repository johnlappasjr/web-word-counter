import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

base_url = "https://mozilla.org"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
urls = set()

try:
    html = urlopen(base_url)
except HTTPError as e:
    print(f"Error opening {base_url}: {e}")
else:
    bsObj = BeautifulSoup(html.read(), features="html.parser")
    for link in bsObj.find_all('a'):
        urls.add(link.get('href'))

    words = 0
    for url in urls:
        if url in ["NULL", "_blank", "None", None, "NoneType", base_url]:
            continue

        if url[0] == "/":
            specific_url = base_url + url
        else:
            specific_url = url

        try:
            response = requests.get(specific_url, headers=headers)
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error opening {specific_url}: {e}")
        except Exception as e:
            print(f"Error opening {specific_url}: {e}")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
            for script in soup(["script", "style"]):
                script.clear()

            text = soup.get_text()
            print(f"{specific_url}: {len(text)} words")
            words += len(text)

    print(f"Total: {words} words")

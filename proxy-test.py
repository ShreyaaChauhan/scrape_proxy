import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures


def getProxies():
    r = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("tbody")
    proxies = []
    for row in table:
        if row.find_all("td")[4].text == "elite proxy":
            proxy = ":".join([row.find_all("td")[0].text, row.find_all("td")[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies


def proxy_from_txt(filename):
    with open(filename, "r") as f:
        txt_proxies = [line.strip() for line in f]
    return txt_proxies


def extract(proxy):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
    }
    try:
        r = requests.get(
            "https://shopify.com/",
            headers=headers,
            proxies={"http": proxy, "https": proxy},
            timeout=15,
        )
        if r.status_code == 200:
            working = {
                "proxy": proxy,
                "status_code": r.status_code,
                "data": r.text[:200],
            }
            print(proxy)
    except requests.ConnectionError:
        pass
    return proxy


def main():
    txt_prox = proxy_from_txt("proxy-list.txt")
    proxylist = getProxies()

    for p in txt_prox:
        proxylist.append(p)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, proxylist)

    return


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re, json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows; Windows NT 10.1; WOW64) AppleWebKit/603.23 (KHTML, like Gecko) Chrome/53.0.1727.275 Safari/601.4 Edge/13.39746",
    "Accept-Language": "da, en-gb, en",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}


def get_title(soup: BeautifulSoup):
    element = soup.find(id="productTitle")
    if element:
        return element.text.strip()


def get_details(soup: BeautifulSoup):
    element = soup.find(id="feature-bullets") or soup.find(
        id="productFactsDesktopExpander"
    )
    if not element:
        return []

    items = element.find_all("li")

    return [item.text.strip() for item in items]


def get_image(soup: BeautifulSoup):
    possible = (
        soup.find(id="main-image-container").find("ul").find_all("li", class_="image")
    )
    for p in possible:
        img = p.find("img")
        if img:
            return img.attrs["src"]

    return None


def get_price_and_savings(soup: BeautifulSoup):
    container = soup.find(id="corePriceDisplay_desktop_feature_div")

    savings_element = container.find(class_="savingsPercentage")
    savings = (
        savings_element.text.strip().replace("-", "").replace("%", "")
        if savings_element
        else "0"
    )
    price = (
        soup.find(id="corePriceDisplay_desktop_feature_div")
        .find(class_="priceToPay")
        .find(class_="a-price-whole")
        .text.strip()
        .replace(",", "")
    )
    return price, savings


def get_category(soup: BeautifulSoup):
    return soup.find(id="wayfinding-breadcrumbs_feature_div").find("li").text.strip()


def main():
    with open("input.txt", "r") as f:
        _input = f.read().splitlines()

    products = []

    for url in _input:
        res = requests.get(
            url,
            headers=headers,
        )
        soup = BeautifulSoup(res.content, features="html.parser")

        title = get_title(soup)
        category = get_category(soup)
        details = get_details(soup)
        image = get_image(soup)
        price, savings = get_price_and_savings(soup)

        products.append(
            {
                "title": title,
                "category": category,
                "details": details,
                "image": image,
                "price": {"payable": price, "savings": savings},
            }
        )

    with open("products.json", "w") as f:
        json.dump(products, f, indent=2)


if __name__ == "__main__":
    main()

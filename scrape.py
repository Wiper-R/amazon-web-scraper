import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows; Windows NT 10.1; WOW64) AppleWebKit/603.23 (KHTML, like Gecko) Chrome/53.0.1727.275 Safari/601.4 Edge/13.39746",
    "Accept-Language": "da, en-gb, en",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

def get_title(soup: BeautifulSoup):
    title_element = soup.find(id="productTitle")
    return title_element.text.strip() if title_element else None

def get_details(soup: BeautifulSoup):
    feature_element = soup.find(id="feature-bullets") or soup.find(id="productFactsDesktopExpander")
    if feature_element:
        return [item.text.strip() for item in feature_element.find_all("li")]
    return []

def get_image(soup: BeautifulSoup):
    main_image_container = soup.find(id="main-image-container")
    if main_image_container:
        possible_images = main_image_container.find("ul").find_all("li", class_="image")
        for img in possible_images:
            img_src = img.find("img")
            if img_src:
                return img_src.attrs["src"]
    return None

def get_price_and_savings(soup: BeautifulSoup):
    price_element = soup.find(id="corePriceDisplay_desktop_feature_div")
    if price_element:
        price = price_element.find(class_="a-price-whole").text.strip().replace(",", "")
        savings_element = price_element.find(class_="savingsPercentage")
        savings = savings_element.text.strip().replace("-", "").replace("%", "") if savings_element else "0"
        return price, savings
    return None, None

def get_category(soup: BeautifulSoup):
    breadcrumbs_element = soup.find(id="wayfinding-breadcrumbs_feature_div")
    if breadcrumbs_element:
        return breadcrumbs_element.find("li").text.strip()
    return None

def main():
    with open("processable.txt", "r") as f:
        urls = f.read().splitlines()

    products = []

    for url in urls:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="html.parser")

        title = get_title(soup)
        category = get_category(soup)
        details = get_details(soup)
        image = get_image(soup)
        price, savings = get_price_and_savings(soup)

        products.append({
            "title": title,
            "category": category,
            "details": details,
            "image": image,
            "price": {"payable": price, "savings": savings}
        })

    with open("products.json", "w") as f:
        json.dump(products, f, indent=2)

def clean_link(link):
    parsed_url = urlparse(link)
    path_components = parsed_url.path.split("/")
    for i, component in enumerate(path_components):
        if component.lower() == "dp" and i < len(path_components) - 1:
            return parsed_url.scheme + "://" + parsed_url.netloc + "/dp/" + path_components[i + 1]
    return parsed_url.geturl()


def write_clean_links():
    with open("input.txt", "r") as f:
        raw_links = f.read().splitlines()

    clean_links = [clean_link(link) for link in raw_links]

    with open("processable.txt", "w") as f:
        f.write("\n".join(clean_links))

if __name__ == "__main__":
    write_clean_links()
    main()

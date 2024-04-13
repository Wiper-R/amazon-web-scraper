
# Amazon Web Scraper

A small utility to fetch products data from Amazon


Example Data: (fetched from amazon.in)
```json
{
    "title": "Red Tape Casual Sneaker Shoes for Men | Stylish and Comfortable",
    "category": "Shoes & Handbags",
    "details": [
      "MATERIAL: Upper - PU | Outsole - TPR (Thermoplastic Rubber)",
      "FEATURES: Closure - Lace-Up | TOE SHAPE- Round Toe",
      "Benefits: Experience ultimate comfort through the TPU + TPR Sole of these shoes. Enjoy dynamic feet and arch support, coupled with slip-resistant features that effectively eliminate the possibility of accidental falls.",
      "These shoes offer continuous comfort throughout the day, ensuring your feet stay relaxed, all while maintaining a casually stylish appearance.",
      "Lifestyle: Sneaker Shoes",
      "Care Instruction : Wipe with a clean, dry cloth to remove the dust."
    ],
    "image": "https://m.media-amazon.com/images/I/41o75CZtK-L._SY395_SX395_.jpg",
    "price": {
      "payable": "1119", // In rupees
      "savings": "80" // In Percent
    }
  }
```

### How to use:

I would advise you to use user agent generators.
Ex. [IP Logger](https://iplogger.org/useragents/)

Open `input.txt` and add your all product urls in it


Then run these following commands


```
python -m pip install poetry
```


```
poetry shell
```

```
poetry install
```


```
python scrape.py
```


All scraped data will get saved in `products.json` in root directory





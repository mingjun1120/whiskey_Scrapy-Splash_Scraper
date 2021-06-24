# whiskey_Scrapy-Splash_Scraper
This is a web crawler that can help to crawl all the details of Scotch Whisky and also World Whisky from this website [THE WHISKY SHOP](https://www.whiskyshop.com/scotch-whisky)





## Authors
- Lim Ming Jun

  
## Documentation
- [Documentation for Scrapy](https://docs.scrapy.org/en/latest/)
- [Documentation for Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash)


  
## Important Notes!
This project requires you to install [Docker](https://www.docker.com/products/docker-desktop) in your PC or laptop in order to use Scrapy-Splash. So, I highly recommend you to follow the below tutorials to setup your project.
Either one of these videos will teach you how to install Docker and setup Scrapy-Splash project. The details explanation of Scapy-Splash will also be delivered in the link below.
- https://youtu.be/mTOXVRao3eA
- https://youtu.be/RgdaP54RvUM

## How to run?
Open up your terminal and **navigate** to the **inner whiskey folder**
```
cd whiskey
```
Example output:
`> C:\Users\JuroyLim\Desktop\whiskey\whiskey>`

Then, type any of these commands to **`run`**

**Crawled data will stored in JSON file:**
```
scrapy crawl whiskey_crawl -O whiskey.json
```


> OR
**Crawled data will stored in CSV file:**
```
scrapy crawl whiskey_crawl -O whiskey.csv
```

> OR

**Just crawled data and view the output in terminal:**
```
scrapy crawl whiskey_crawl
```
**Note:** **`whiskey_crawl`** is the crawler name

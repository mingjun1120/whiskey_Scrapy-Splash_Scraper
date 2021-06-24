import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from whiskey.items import WhiskeyItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest, SplashJsonResponse, SplashTextResponse
from scrapy.http import HtmlResponse

class WhiskeyCrawlSpider(CrawlSpider):
    name = 'whiskey_crawl'
    allowed_domains = ['whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    # response.css("div.product-item-info > a")
    le_whiskey_details = LinkExtractor(restrict_xpaths = "//div[@class='product-item-info' and @data-container='product-grid']/a")
    le_next = LinkExtractor(restrict_xpaths= "(//a[@title = 'Next'])[2]") # Next Button
    le_world_whiskey_details = LinkExtractor(restrict_xpaths= "//nav[@id='cwsMenu-5']/ul/li[6]/a") # World Whiskey

    rule_whiskey_details = Rule(le_whiskey_details, callback = 'parse_item', follow = False, process_request="use_splash")
    rule_next = Rule(le_next, follow = True, process_request="use_splash")
    rule_world_whiskey_details = Rule(le_world_whiskey_details, follow = True, process_links='processLink', process_request="use_splash")

    rules = (rule_whiskey_details, rule_next, rule_world_whiskey_details)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'wait': 15}, meta={'real_url': url})

    def use_splash(self, request):
        request.meta['splash'] = {'endpoint':'render.html', 'args':{'wait': 15,}}
        return request
    
    def _requests_to_follow(self, response):
        if not isinstance(response, (HtmlResponse, SplashJsonResponse, SplashTextResponse)):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response) if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def processLink(self, links):
        if type(links) in [tuple, list]: 
            for link in links:
                if type(link.url) is str:
                    link.url = link.url + '?item_availability=In+Stock'
                    yield link
        elif type(links.url) == str:
            links.url = links.url + '?item_availability=In+Stock'
            yield links

    def parse_item(self, response):
        l = ItemLoader(item = WhiskeyItem(), selector = response.css('div.product-info-wrap'))

        l.add_xpath('Name', '//h1[@class="page-title"]')
        l.add_css('Volume', 'p.product-info-size-abv > span:contains("cl")')
        l.add_css('Alcohol_Percent', 'p.product-info-size-abv > span:contains("abv")')
        l.add_xpath('Region', "//p[@class='product-info-size-abv']/span[not(contains(., 'abv')) and not(contains(., 'cl'))]")
        l.add_xpath('Price_Pound', "(//span[contains(@class, 'price-wrapper')])[1]/span[@class='price']")
        l.add_value('Link', response.url)

        yield l.load_item()

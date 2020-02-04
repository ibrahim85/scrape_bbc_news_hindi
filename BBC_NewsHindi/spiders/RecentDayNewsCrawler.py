# -*- coding: utf-8 -*-
import scrapy
import datetime
from BBC_NewsHindi.items import BbcNewshindiItem

g_dict_months = {'يناير': '01', 'فبراير': '02', 'مارس': '03', 'ابريل': '04', 'مايو': '05', 'يونية': '06', 'يوليو': '07', 'اغسطس': '08', 'سبتمبر': '09', 'اكتوبر': '10', 'نوفمبر': '11', 'ديسمبر': '12'}

# create a new file in every crawl
file_obj = open('third_file.txt', 'w+')
file_obj.close()
file_obj = open('third_file_date_log.txt', 'w+')
file_obj.close()


class RecentdaynewscrawlerSpider(scrapy.Spider):
    name = "RecentDayNewsCrawler"
    allowed_domains = ["bbc.com"]

    def urlFunc():
        groups_list = ['arabic', 'international', 'entertainment', 'sport', 'science', 'social', 'media/video', 'media/audio', 'media/photogalleries', 'in_depth']
        url_list = ["https://www.bbc.com/arabic"]
        for group in groups_list:
            url = "https://www.bbc.com/arabic/" + group
            url_list.append(url)
        # print(url_list)
        return url_list

    start_urls = urlFunc()

    def parse(self, response):

        # for news title and main url
        for sel in response.xpath("//*[@class='faux-block-link__overlay-link']"):
            item = BbcNewshindiItem()

            news_url = sel.xpath("@href").extract_first()

            if news_url is not None:
                if news_url.startswith("http"):
                    item['news_page_url'] = news_url               
                    request = scrapy.Request(item['news_page_url'], callback=self.parseSpecialNewsDetails)
                else:
                    item['news_page_url'] = "https://www.bbc.com" + news_url                    
                    request = scrapy.Request(item['news_page_url'], callback=self.parseNewsDetails)

                request.meta['item'] = item
                yield request


    def parseNewsDetails(self, response):
        item = response.meta['item']
        item = self.getNewsDetails(item, response)
        return item

    # Data source written to file from main news page
    def getNewsDetails(self, item, response):
        check_recent = str(response.xpath("//*[@class='date date--v2']/text()").extract_first().encode('utf-8')).strip()

        news_recent_day = check_recent[:2] + g_dict_months[check_recent.split()[1]] + check_recent[-4:]

        today_date = datetime.date.today().strftime("%d%m%Y")

        if news_recent_day == today_date:

        	with open('third_file_date_log.txt', 'a+') as fp:
	            fp.write('{0} - - {1}\n\n\n'.format(news_recent_day, today_date))

	        news_title = response.xpath("//*[@class='story-body__h1']/text()").extract_first().encode('utf-8')
	        if news_title is not None:
	            item['title_headlines'] = news_title
	        else:
	            item['title_headlines'] = "Not Found"

	        lNewsContent = response.xpath("//*[@class='story-body__inner']/p/text()").extract()
	        news_content = ('\n'.join(lNewsContent)).encode('utf-8')
	        if news_content is not None:
	            item['content_news'] = news_content
	        else:
	            item['content_news'] = "Not Found"

	        with open('third_file.txt', 'a+') as fp:
	            fp.write('{0}\n\n{1}\n\n\n\n'.format(item['title_headlines'], item['content_news']))

        return item


    def parseSpecialNewsDetails(self, response):
        for sel in response.xpath("//*[@class='faux-block-link__overlay-link']"):
            item = BbcNewshindiItem()

            news_url = sel.xpath("@href").extract_first()
            
            if news_url is not None:
                item['news_page_url'] = "https://www.bbc.com" + news_url                
                request = scrapy.Request(item['news_page_url'], callback=self.parseNewsDetails)
                request.meta['item'] = item
                yield request


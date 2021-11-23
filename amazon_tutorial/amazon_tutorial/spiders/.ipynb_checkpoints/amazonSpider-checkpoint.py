import scrapy
from ..items import AmazonTutorialItem
import pandas as pd

class AmazonspiderSpider(scrapy.Spider):
    name = 'amazon'
    page_no = 2
    max_page_no = 70
    urls =[
        'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011%2Cn%3A565108&dc&qid=1637621859&rnid=13896617011&ref=sr_nr_n_2',
    ]
    for i in range(page_no, max_page_no+1):
        urls.append('https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011%2Cn%3A565108&dc&page='+str(i)+'&qid=1637629607&rnid=13896617011&ref=sr_pg_'+str(i))
        
    start_urls = urls
    type_header_name = True
    
    def parse(self, response):
        items = AmazonTutorialItem()
        items_dict = {}
        
        #hint: when use googlebot user agent, things go different. It's better to use scrapy-user-agent

        products_data_asin = response.css('::attr(data-asin)').extract()
        while '' in products_data_asin:
            products_data_asin.remove('')
        
        product_title = []
        product_price = []
        product_imageLink = []
        product_hyperLink = []
        for product in products_data_asin:
            product_data_asin_css = response.css('[data-asin='+product+']')
            product_title.append(product_data_asin_css.css('.a-color-base.a-text-normal').css('::text').extract_first())
            try:
                product_price.append(product_data_asin_css.css('.a-price-whole').css('::text').extract_first())
            except:
                product_price.append('no price found')
            product_imageLink.append(product_data_asin_css.css('.rush-component:nth-child(2) .s-image').css('::attr(src)').extract_first())
            product_hyperLink.append(product_data_asin_css.css('.a-link-normal.a-text-normal').css('::attr(href)').extract_first())
        
        items_dict['product_title'] = product_title
        items_dict['product_price'] = product_price
        items_dict['product_imageLink'] = product_imageLink
        items_dict['product_hyperLink'] = product_hyperLink
        
#         print(items_dict)

        print(f'product_title: {len(product_title)}')
        print(f'product_price: {len(product_price)}')
        print(f'product_imageLink: {len(product_imageLink)}')
        print(f'product_hyperLink: {len(product_hyperLink)}')
        
        items['product_title'] = product_title
        items['product_price'] = product_price
        items['product_imageLink'] = product_imageLink
        items['product_hyperLink'] = product_hyperLink
        
        # csv coded from scratch is tap seperated for better control as titles can have ',' commas
#         fields = ['product_title','product_price','product_imageLink', 'product_hyperLink']
#         with open('output.csv',"a", encoding="utf-8") as f: # handle the source file
#             if AmazonspiderSpider.type_header_name == True:
#                 f.write("{}\n".format('\t'.join(str(field)for field in fields))) # write header 
#                 AmazonspiderSpider.type_header_name = False
                
#             for i in range(len(items_dict['product_title'])):
#                 for item in items_dict:
#                     f.write("{}\t".format(str((items_dict[item])[i]))) # write items
#                 f.write("\n")
        
        # csv using pandas and dict
        
        df = pd.DataFrame.from_dict(items_dict)
        if AmazonspiderSpider.type_header_name == True:
            df.to_csv('output.csv', mode='a', index=False)
            AmazonspiderSpider.type_header_name = False
        else:
            df.to_csv('output.csv', mode='a', index=False, header=False)
                
        yield items
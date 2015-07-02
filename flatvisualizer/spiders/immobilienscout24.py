import scrapy
import re
from flatvisualizer.items import FlatvisualizerItem

def clean_encode(string):
	string = string.replace('\r\n', ' ')
	string = string.replace('\t', '').strip()
	string = ' '.join(string.split())
	string = string.encode('utf-8')
	return string

def make_numeric(string, func=float):
	string = re.sub("[^0-9,\.]", "", string).strip()
	string = string.replace(".", "")
	return func(string.replace(',', '.'))

class ImmobilienScout24Spider(scrapy.Spider):
	name = "immobilienscout24"
	allowed_domains = ["immobilienscout24.de"]
	start_urls = ["http://www.immobilienscout24.de/Suche/S-2/P-1/Wohnung-Miete/Berlin/Berlin/Friedenau-Schoeneberg_Lichterfelde-Steglitz_Steglitz-Steglitz_Schoeneberg-Schoeneberg_Tempelhof-Tempelhof_Wilmersdorf-Wilmersdorf/3,00-/70,00-/EURO--900,00/-/-/false"]

	result_xpath = '//div[@id="listContainer"]/ul/li[@data-item="result"]'
	link_xpath = "div[2]/div/div[2]/div[1]/span/a/@href"
	address_xpath = "div[2]/div/div[2]/div[1]/p/span/text()"
	rent_xpath = "div[2]/div/div[2]/div[2]/dl[1]/dd/text()"
	size_xpath = "div[2]/div/div[2]/div[2]/dl[2]/dd/text()"
	rooms_xpath = "div[2]/div/div[2]/div[2]/dl[3]/dd/text()"

	def parse(self, response):
		for sel in response.xpath(self.result_xpath):
			item = FlatvisualizerItem()
			item['link'] = sel.xpath(self.link_xpath).extract()[0];
			item['source_id'] = item['link'].split('/')[-1]
			item['address'] = clean_encode(sel.xpath(self.address_xpath).extract()[0]);
			item['rent'] = make_numeric(sel.xpath(self.rent_xpath).extract()[0]);
			item['size'] = make_numeric(sel.xpath(self.size_xpath).extract()[0]);
			item['rooms'] = make_numeric(sel.xpath(self.rooms_xpath).extract()[0]);
			yield item
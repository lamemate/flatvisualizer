# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import simplejson
import urllib
import googlemaps
import keys

class FlatvisualizerPipeline(object):
    def process_item(self, item, spider):
        return item

class AddDistanceToWorkPipeLine(object):

	latitude_longitude_work = str((52.45402, 13.29320))

	def __init__(self):
		self.key = keys.GOOGLE_MAPS_API_KEY
		self.gm_client = googlemaps.Client(self.key)

	def process_item(self, item, spider):
		origin = item["address"]

		geo_location = self.gm_client.geocode(origin)

		if len(geo_location) > 0:
			for k in ('lat', 'lng'):
				item[k] = geo_location[0]['geometry']["location"][k]

		directions_result = self.gm_client.directions(str((item['lat'], item['lng'])),
			self.latitude_longitude_work,
			mode = "transit",
			departure_time = 1421307820)

		chosen_leg = None
		if len(directions_result) > 0:
			for dr in directions_result:
				for l in dr['legs']:
					if chosen_leg is None:
						chosen_leg = l
					if chosen_leg is not None and chosen_leg["duration"]["value"] > l["duration"]["value"]:
						chosen_leg = l

		if chosen_leg is None:
			return
		item["time_to_work"] = chosen_leg["duration"]["value"]/60.0
		return item
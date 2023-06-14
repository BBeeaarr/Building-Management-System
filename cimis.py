import requests
import json
from datetime import date
today = date.today()
response_API = requests.get('http://et.water.ca.gov/api/data?appKey=72428d8a-f41a-4b37-85c2-7c72816b37ba&targets=92620&startDate=2022-06-14&endDate=2022-06-14&unitOfMeasure=E&dataItems=hly-rel-hum')
data = response_API.text
parse_json = json.loads(data)

class CIMIS:
	def __init__(self):
		self.int = 1
		self.cimis = parse_json['Data']['Providers'][0]['Records'][0]['HlyRelHum']['Value']

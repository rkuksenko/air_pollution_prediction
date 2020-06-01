from air_pollution_django.air_pollution_app.bl.dataset_collector.weather_collector import WeatherCollector
from air_pollution_django.air_pollution_app.bl.dataset_collector.aqi_collect import AqiCollector
from air_pollution_django.air_pollution_app.bl.dataset_collector.data_collector import DataCollector

city = 'Kiev'


aqi = AqiCollector()
aqi.collect_aqi_to_csv(city)

# all = DataCollector()
# all.collect_all_data(city)
#
# all.make_unique_dataframe()
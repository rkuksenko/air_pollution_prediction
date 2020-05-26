import logging

import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

import air_pollution_project.air_pollution_app.bl.log
from air_pollution_project.air_pollution_app.bl.dataset_collector.data_collector import DataCollector


logger = logging.getLogger('Predictor')


class AqiPredictor:
    def __init__(self):
        logger.info('AqiPredictor created')

        self.data_collector = DataCollector()

    def predict(self, city):
        self.data_collector.collect_all_data(city)

        aqi_col_names = ['id', 'aqi', 'pm10',	'pm25',	'o3', 'timestamp_local', 'so2',
                         'no2', 'timestamp_utc',	'datetime', 'co', 'ts']

        weather_col_names = ['id', 'time', 'summary', 'icon',	'precipIntensity', 'precipProbability', 'precipType',
                             'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'pressure', 'windSpeed',
                             'windGust', 'windBearing', 'cloudCover', 'uvIndex', 'visibility', 'ozone']

        # get actual columns names
        actual_aqi_col_names = ''
        with open(DataCollector.AQI_DATA_CSV_FILE, 'r') as f:
            actual_aqi_col_names = f.readline()
        actual_aqi_col_names = actual_aqi_col_names.split(',')
        actual_aqi_col_names[-1] = actual_aqi_col_names[-1][:-1]
        actual_aqi_col_names[0] = 'id'

        aqi_data = pd.read_csv(DataCollector.AQI_DATA_CSV_FILE, header=None, names=actual_aqi_col_names)
        # weather_data = pd.read_csv(DataCollector.WEATHER_DATA_CSV_FILE, header=None)

        print(aqi_data.head())
        # print(weather_data.head())

        # split dataset in features and target variable
        # aqi_feature_cols = ['id', 'pm10', 'pm25', 'o3', 'timestamp_local', 'so2', 'no2', 'timestamp_utc', 'datetime', 'co', 'ts']
        # aqi_col_names_X = aqi_data[aqi_feature_cols]  # Features
        # aqi_col_names_y = aqi_data.aqi  # Target variable
        #
        # # Split dataset into training set and test set
        # aqi_X_train, aqi_X_test, aqi_y_train, aqi_y_test = train_test_split(aqi_col_names_X,
        #                                                                     aqi_col_names_y,
        #                                                                     test_size=0.3,
        #                                                                     random_state=1)  # 70% training and 30% test
        #
        # #Create Decision Tree classifer object
        # clf = DecisionTreeClassifier()
        # clf = clf.fit(aqi_X_train, aqi_y_train)
        #
        # # Predict the response for test dataset
        # aqi_y_pred = clf.predict(aqi_X_test)


aqi_predictor = AqiPredictor()
aqi_predictor.predict('Kiev')

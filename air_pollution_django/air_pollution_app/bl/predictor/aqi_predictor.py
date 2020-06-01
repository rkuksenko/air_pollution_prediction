import logging
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from air_pollution_django.air_pollution_app.bl.logger import log
from air_pollution_django.air_pollution_app.bl.dataset_collector.data_collector import DataCollector
from sklearn.tree import export_graphviz
from io import StringIO


logger = logging.getLogger('Predictor')


class AqiPredictor:
    def __init__(self):
        logger.info('AqiPredictor created')

        self.data_collector = DataCollector()

    @staticmethod
    def _get_actual_columns_names(csv_filename: str):
        with open(csv_filename, 'r') as f:
            actual_aqi_col_names = f.readline()

        actual_aqi_col_names = actual_aqi_col_names.split(',')
        actual_aqi_col_names[-1] = actual_aqi_col_names[-1][:-1]

        logger.info(f'From {csv_filename} extracted actual columns names: {actual_aqi_col_names}')
        return actual_aqi_col_names

    def predict(self, city):
        logger.info('Start prediction')
        self.data_collector.collect_all_data(city)

        # get actual columns names from a csv files
        actual_aqi_col_names = AqiPredictor._get_actual_columns_names(csv_filename=DataCollector.AQI_DATA_CSV_FILE)
        actual_weather_col_names = AqiPredictor._get_actual_columns_names(csv_filename=DataCollector.WEATHER_DATA_CSV_FILE)

        # make a datasets
        aqi_dataset = pd.read_csv(DataCollector.AQI_DATA_CSV_FILE, header=None, names=actual_aqi_col_names)
        weather_dataset = pd.read_csv(DataCollector.WEATHER_DATA_CSV_FILE, header=None, names=actual_weather_col_names)

        # remove column names because it is no already needed
        aqi_dataset = aqi_dataset.drop([0])
        weather_dataset = weather_dataset.drop([0])

        print(aqi_dataset.head())
        print(weather_dataset.head())

        # split dataset in features and target variable
        aqi_feature_cols = ['pm10', 'pm25', 'o3', 'so2', 'no2', 'co', 'ts']     # 'datetime' left
        aqi_col_names_x = aqi_dataset[aqi_feature_cols]  # Features
        aqi_col_names_y = aqi_dataset.aqi  # Target variable

        # Split dataset into training set and test set
        aqi_x_train, aqi_x_test, aqi_y_train, aqi_y_test = train_test_split(aqi_col_names_x,
                                                                            aqi_col_names_y,
                                                                            test_size=0.3,
                                                                            random_state=1)  # 70% training and 30% test

        # Create a Decision Tree classifer object
        clf = DecisionTreeClassifier()
        clf = clf.fit(aqi_x_train, aqi_y_train)

        # Predict the response for test dataset
        aqi_y_pred = clf.predict(aqi_x_test)

        # aqi_y_pred = clf.predict()

        logger.info(f'Prediction done! Accuracy: {metrics.accuracy_score(aqi_y_test, aqi_y_pred)}')

        dot_data = StringIO()
        export_graphviz(clf,
                        out_file=dot_data,
                        filled=True,
                        rounded=True,
                        special_characters=True,
                        feature_names=aqi_feature_cols)

        decision_tree_file_path = '../data/graph.dot'
        logger.info(f'Dot file with decision tree saved in {decision_tree_file_path}')

        with open(decision_tree_file_path, 'w') as f:
            f.write(dot_data.getvalue())


aqi_predictor = AqiPredictor()
aqi_predictor.predict('Kiev')

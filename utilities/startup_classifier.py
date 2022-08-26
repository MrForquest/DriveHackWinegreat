from fuzzywuzzy import fuzz
import dill as pickle
from func_for_classifier import tokenize_sentence


# df = pd.read_csv("/content/data_startup.csv")


class Key_words:
    def __init__(self):
        self.slov = ['Transport', 'Public transport', 'Car', 'Bus', 'Train', 'Trolley', 'Trolleybus',
                     'Tram', 'Metro', 'Subway', 'Underground', 'Monorail', 'Plane', 'Boat', 'Ship',
                     'Machine', 'Autopilot', 'Taxi', 'Robotaxi', 'Robobus', 'Robotrain', 'Robocar',
                     'Transportation',
                     'Mobility', 'Future transportation', 'Scooter', 'Electric scooter',
                     'Bike', 'Bycicle', 'Electric bycicle', 'Micromobility', 'Company', 'Electric',
                     'Public',
                     'Investors', 'Technology', 'Autonomous', 'Business', 'Investment']

    def predict(self, txt):

        def compare(word):
            for i in self.slov:
                percent = fuzz.ratio(word, i)
                if percent >= 80:
                    return True
            return False

        def get_percent():
            counter = 0
            text = txt
            for i in text.split():
                if compare(i):
                    counter += 1
            percent = counter / len(self.slov)
            return percent

        return get_percent()


class StartupClassifier:
    def __init__(self):
        with open('../static/regresion7_plk', 'rb') as f:
            self.classifier_regres = pickle.load(f)
        self.keywords_classifier = Key_words()

    def predict(self, txt):
        if 0.15 * self.keywords_classifier.predict(txt) + 0.85 * \
            self.classifier_regres.predict_proba([txt])[0][
                1] >= 0.5:
            # print(0.15 * get_percent(txt) + 0.85 * grid_pipeline.predict_proba([txt])[0, 1])
            return 1  # является стартапом, связанным с транспортом
        else:
            # print(0.15 * get_percent(txt) + 0.85 * grid_pipeline.predict_proba([txt])[0, 1])
            return 0  # не является стартапом, связанным с транспортом

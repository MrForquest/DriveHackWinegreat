from fuzzywuzzy import fuzz


def compare(word):
    for i in slov:
        percent = fuzz.ratio(word, i)
        if percent >= 80:
            return True
    return False


slov = ['Transport', 'Public transport', 'Car', 'Bus', 'Train', 'Trolley', 'Trolleybus',
        'Tram', 'Metro', 'Subway', 'Underground', 'Monorail', 'Plane', 'Boat', 'Ship',
        'Maschine', 'Autopilot', 'Taxi', 'Robotaxi', 'Robobus', 'Robotrain', 'Robocar', 'Transportation',
        'Mobility', 'Future transportation', 'Scooter', 'Electric scooter',
        'Bike', 'Bycicle', 'Electric bycicle', 'Micromobility']


def get_percent(txt):
    counter = 0
    text = txt
    for i in text:
        if compare(i):
            counter += 1
    percent = counter / len(slov) * 100
    return percent

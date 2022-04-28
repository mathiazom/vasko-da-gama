import requests


def get_random_fun_fact():
    return requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()['text']


def get_random_dad_joke():
    return requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json()['joke']

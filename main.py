import argparse
from operator import contains
from os import listdir
from os.path import isfile, join
from pprint import pprint
import requests
import json
import uuid

BASE_URL = 'https://protondb.max-p.me'

def parse_args():
    parser = argparse.ArgumentParser(description='Supply full paths to your game libraries. ')
    parser.add_argument('path')
    args = parser.parse_args()
    return args.path

def check_path_for_gamedirs(path):
    games = [d for d in listdir(path)]
    filtered_games = [game for game in games if not "." in game]
    return filtered_games

def query_protondb_api(url):
    response = requests.get(url)
    return response.json()

def filter_api_results(games, api_data):
    api_data_key_val_tuples = [entry.items() for entry in api_data]
    game_metadata = {}
    result = []
    for appId, title in api_data_key_val_tuples:
        random_id = str(uuid.uuid4())[:8]
        game_metadata[random_id] = {'appId': appId[1], 'title': title[1]}
    for game in games:
        for id, data in game_metadata.items():
            if game == data['title']:
                result.append(game_metadata[id])
    return result

def get_reports_from_found_games(found_games):
    for found_game in found_games:
        response = requests.get(f"{BASE_URL}/games/{found_game['appId']}/reports/")
        return response.json()

def main():
    path = parse_args()
    games = check_path_for_gamedirs(path)
    
    api_data =  query_protondb_api(BASE_URL + '/games')
    found_games = filter_api_results(games, api_data)
    reports = get_reports_from_found_games(found_games)
    pprint(reports)




if __name__ == "__main__":
    main()
import os
import json


def get_all_entities_path(path_filter:str):
    file_paths = []
    script_path = os.path.abspath(__file__)
    root_folder = os.path.dirname(os.path.dirname(script_path))
    path = root_folder + "/metadata/"
    file_names = os.listdir(path)

    # Filter the file names that ends with "_entity"
    filtered_file_names = [file_name for file_name in file_names if file_name.endswith(path_filter)]

    # Print the filtered file names
    for file_name in filtered_file_names:
        file_paths.append(path + "/" + file_name)

    return file_paths


def load_json(file_path: str):
    # Open the file and load the JSON data
    with open(file_path, "r") as file:
        json_data = json.load(file)

    return json_data

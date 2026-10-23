import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def read_csv_data(filename):
    filepath = os.path.join(BASE_DIR, "data", filename)
    with open(filepath, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def read_json_data(filename):
    filepath = os.path.join(BASE_DIR, "data", filename)
    with open(filepath, mode="r", encoding="utf-8-sig") as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"The JSON file '{filepath}' is empty! Please paste the JSON data and press Ctrl+S.")
        return json.loads(content)
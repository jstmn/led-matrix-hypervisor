import argparse
import os
import json

from utils import send_json_post

_APP_URL = f"http://127.0.0.1:5000/LED"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, type=str)
    args = parser.parse_args()

    filepath = os.path.join("data/", args.filename + ".json")
    assert os.path.isfile(filepath), f"filepath '{filepath}' does not exist"

    with open(filepath, "r") as f:
        data = json.load(f)
        send_json_post(_APP_URL, data, verbose=True)
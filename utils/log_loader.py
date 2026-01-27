# utils/log_loader.py

import os

def load_logs(logs_path):
    logs_data = {}

    for file in os.listdir(logs_path):
        if file.endswith(".log"):
            with open(os.path.join(logs_path, file), "r") as f:
                logs_data[file] = f.readlines()

    return logs_data
import pandas as pd
import gdown
from datetime import datetime


def process_google_sheet():
    log = "=====================================================\n"
    log += f"Downloading and Processing Google Sheets at {datetime.now()}\n"
    url = "https://docs.google.com/spreadsheets/d/1C1gcxQGkV0OP2Y-okwJb-J4gjv_1dLiAJOoceSoKwhQ/edit?usp=sharing"

    output_path = "./data/raw_data.xlsx"
    gdown.download(url, output_path, quiet=False, fuzzy=True)

    df = pd.read_excel(output_path, engine="openpyxl")

    rename_columns = {
        "Timestamp": "timestamp",
        "Name (optional)": "name",
        "Age": "age",
        "Gender": "gender",
        "Weight (in Kgs)": "weight",
        "Height (in cms)": "height",
        "Number of sessions per week": "sessions",
        "Number of minutes per session": "duration",
        "Availability of equipments": "gym",
        "Additional Comments for your workout": "comments",
        "Enter a username (at least 7 characters)": "random_chars",
    }

    df = df.rename(rename_columns, axis=1)

    def strip_replace(text):
        return str(text).replace(" ", "-").replace("/", "-").replace(":", "-").strip()

    df["id"] = df["timestamp"].apply(strip_replace)

    df.to_csv("./data/processed_1.csv", index=False)

    log += f"Completed processing at {datetime.now()}\n"

    return log

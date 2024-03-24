import uuid
import pandas as pd


filename = "./data/Workout Planner (Responses) - Form Responses 1.csv"
df = pd.read_csv(filename)


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
    "Enter a random 7 characters (numerics and alphabets) without spaces": "random_chars",
}

df = df.rename(rename_columns, axis=1)


def strip_replace(text):
    return text.replace(" ", "-").replace("/", "-").replace(":", "-").strip()


df["id"] = df["timestamp"].apply(strip_replace)

df.to_csv("./data/processed_1.csv", index=False)

import pandas as pd
import requests
import time
from datetime import datetime, timedelta

while True:
    sheet_id = "18SlNAWCnZJWzj7e4CdKA425qq9FbdfEJSOIEAZ5ORo8"
    
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    try:
        df = pd.read_csv(url)
    except pd.errors.EmptyDataError:
        # Handle the case when the sheet is empty
        df = pd.DataFrame()

    df["Schedule Datetime"] = pd.to_datetime(df["Schedule Datetime"])

    previous_minute = datetime.now() - timedelta(minutes=1)
    current_time = datetime.now()

    df = df[(df["Schedule Datetime"] > previous_minute) & (df["Schedule Datetime"] < current_time)]

    def send_message(row):
        bot_id = "6977434953:AAG4M4AlHMChevD5rmOliddrcISKl8I3bXk"
        chat_id = "@pcr_chat"
        message = row[0]
        url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"

        return requests.get(url).json()

    if not df.empty:
        df['status'] = df.apply(send_message, axis=1)

    time.sleep(60)

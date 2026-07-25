import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

URL = "https://teamweb.sporetrofit.com/Location/"
CSV_FILENAME = "gym_capacity_log.csv"

def fetch_and_record():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找人數的標籤 (若後續網頁改版，這裡可能需要微調)
        people_element = soup.select_one('.people-count') 

        # 取得目前的台灣時間
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if people_element:
            current_people = people_element.text.strip()

            # 檢查並寫入 CSV 檔案
            file_exists = os.path.isfile(CSV_FILENAME)
            with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Current_People"])
                writer.writerow([current_time, current_people])

            print(f"[{current_time}] 成功記錄：現在人數 {current_people} 人")
        else:
            print(f"[{current_time}] 警告：找不到對應的人數元素，請檢查網頁結構。")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    fetch_and_record()

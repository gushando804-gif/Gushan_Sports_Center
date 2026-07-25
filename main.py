import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# 嘗試在網址後方直接加上場館代號，強迫伺服器回傳鼓山的資料
URL = "https://teamweb.sporetrofit.com/Location/?LID=TMEGS"
CSV_FILENAME = "gym_capacity_log.csv"

def fetch_and_record():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 使用 Session 來連線
        session = requests.Session()
        response = session.get(URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # === 【新增】偵錯訊息區塊 ===
        print("【網頁載入測試】")
        print(f"機器人實際抓到的網頁標題: {soup.title.text.strip() if soup.title else '找不到標題'}")
        print("---------------------")
        
        current_people = None
        
        # 尋找人數
        gym_divs = soup.find_all('div', class_='col-6')
        for div in gym_divs:
            if '健身房' in div.text:
                people_div = div.find_next_sibling('div', class_='col-3')
                if people_div:
                    current_people = people_div.text.strip()
                break
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if current_people:
            file_exists = os.path.isfile(CSV_FILENAME)
            with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Current_People"])
                writer.writerow([current_time, current_people])
                
            print(f"[{current_time}] 成功記錄：現在人數 {current_people} 人")
        else:
            print(f"[{current_time}] 警告：找不到人數！")
            # 如果找不到，印出網頁最前面的程式碼，讓我們看看機器人到底抓到了什麼鬼東西
            print(f"網頁前 300 字元預覽：\n{response.text[:300]}")
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    fetch_and_record()

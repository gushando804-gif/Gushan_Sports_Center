import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

URL = "https://teamweb.sporetrofit.com/Location/"
CSV_FILENAME = "gym_capacity_log.csv"

def fetch_and_record():
    try:
        # 加上 headers 偽裝成瀏覽器，避免被網站阻擋
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        # 使用 BeautifulSoup 解析網頁
        soup = BeautifulSoup(response.text, 'html.parser')
        
        current_people = None
        
        # 根據截圖結構：尋找所有 class 為 'col-6' 的區塊
        gym_divs = soup.find_all('div', class_='col-6')
        for div in gym_divs:
            # 如果這個區塊裡面包含「健身房」三個字
            if '健身房' in div.text:
                # 抓取它緊鄰的下一個 class 為 'col-3' 的區塊 (裡面就是現在人數)
                people_div = div.find_next_sibling('div', class_='col-3')
                if people_div:
                    # 取出數字，並清除前後多餘的空白或換行
                    current_people = people_div.text.strip()
                break # 找到後就提早結束迴圈
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 檢查是否有成功抓到數字
        if current_people:
            # 寫入 CSV 檔案
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

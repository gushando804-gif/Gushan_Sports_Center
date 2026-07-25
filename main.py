from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime

URL = "https://teamweb.sporetrofit.com/Location/?LID=TMEGS"
CSV_FILENAME = "gym_capacity_log.csv"

def fetch_and_record():
    print("準備啟動虛擬瀏覽器...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 【新增】強制設定解析度為電腦版 1080p，避免網頁變成手機版排版
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"正在連線至 {URL} ...")
        driver.get(URL)
        
        # 【修改】GitHub 機器人可能網路較慢，給它 10 秒鐘慢慢轉
        print("等待 10 秒鐘讓動態資料載入...")
        time.sleep(10) 
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        current_people = None
        
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
                
            print(f"[{current_time}] 🎉 成功記錄：現在人數 {current_people} 人")
        else:
            print(f"[{current_time}] ❌ 警告：依然找不到人數！")
            print("-" * 30)
            print("【機器人視角大公開】以下是網頁載入後，畫面上實際出現的所有文字：")
            # 把網頁裡的所有文字抽出來印在畫面上，方便我們除錯
            clean_text = '\n'.join([line.strip() for line in soup.text.splitlines() if line.strip()])
            print(clean_text[:1500])  # 印出前 1500 個字
            print("-" * 30)
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        driver.quit()
        print("瀏覽器已關閉。")

if __name__ == "__main__":
    fetch_and_record()

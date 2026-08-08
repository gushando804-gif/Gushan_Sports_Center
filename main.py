from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # 定位畫面的元素
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime, timezone, timedelta

# 首頁網址
URL = "https://teamweb.sporetrofit.com/Location/"
CSV_FILENAME = "gym_capacity_log.csv"

def fetch_and_record():
    print("準備啟動虛擬瀏覽器...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"正在連線至首頁...")
        driver.get(URL)
        
        # 等待場地清單載入
        print("等待 5 秒鐘讓場地清單載入...")
        time.sleep(5) 
        
        # === 模擬點擊鼓山選項 ===
        try:
            print("尋找「鼓山」選項並點擊...")
            gushan_btn = driver.find_element(By.XPATH, "//*[contains(text(), '鼓山')]")
            driver.execute_script("arguments[0].click();", gushan_btn)
            print("👉 點擊成功！等待 5 秒讓專屬資料載入...")
            time.sleep(5)
        except Exception as e:
            print("找不到鼓山選項，可能網頁結構有變。")
        # ===================================
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        current_people = None
        
        # 尋找人數
        gym_divs = soup.find_all('div', class_='col-6')
        for div in gym_divs:
            if '健身房' in div.text:
                people_div = div.find_next_sibling('div', class_='col-3')
                if people_div:
                    current_people = people_div.text.strip()
                break
        
        # 設定台灣時區並取得抓取當下的真實時間
        tw_tz = timezone(timedelta(hours=8))
        current_time = datetime.now(tw_tz).strftime("%Y-%m-%d %H:%M:%S")
        
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
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        driver.quit()
        print("瀏覽器已關閉。")

if __name__ == "__main__":
    fetch_and_record()

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
    
    # 設定 Chrome 為無頭模式 (Headless)，也就是在背景不顯示實體視窗執行
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 自動下載並啟動對應版本的 Chrome Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"正在連線至 {URL} ...")
        driver.get(URL)
        
        # 【關鍵步驟】強制等待 5 秒鐘，讓網頁的 JavaScript 有時間把人數載入出來
        print("等待 5 秒鐘讓動態資料載入...")
        time.sleep(5) 
        
        # 取得經過 JavaScript 渲染後的完整網頁原始碼
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        current_people = None
        
        # 用一樣的方式尋找人數
        gym_divs = soup.find_all('div', class_='col-6')
        for div in gym_divs:
            if '健身房' in div.text:
                people_div = div.find_next_sibling('div', class_='col-3')
                if people_div:
                    current_people = people_div.text.strip()
                break
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if current_people:
            # 成功抓到資料，寫入 CSV
            file_exists = os.path.isfile(CSV_FILENAME)
            with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Current_People"])
                writer.writerow([current_time, current_people])
                
            print(f"[{current_time}] 🎉 成功記錄：現在人數 {current_people} 人")
        else:
            print(f"[{current_time}] ❌ 警告：依然找不到人數，可能網頁結構有變動。")
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 無論成功或失敗，最後一定要關閉瀏覽器釋放資源
        driver.quit()
        print("瀏覽器已關閉。")

if __name__ == "__main__":
    fetch_and_record()

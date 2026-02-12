import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


    driver = webdriver.Chrome(service=Service(), options=options)
    driver.execute_script("return navigator.webdriver")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url)

    return driver

def is_flight_schedule_available(url):
    driver = get_driver(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.scheduleList > div.tblbody > div.scrollArea'))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        scroll_area_div = soup.select_one('div.scheduleList > div.tblbody > div.scrollArea')
        if scroll_area_div:
            return True
        
    except Exception as e:
        print(e)
        return False

    finally:
        driver.quit()

def get_flight_schedules(url):
    driver = get_driver(url)

    try:
        print("페이지 로딩 중...")
        time.sleep(20)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)

        # 버튼 텍스트 기반 파싱 (CSS 클래스 해시에 의존하지 않음)
        buttons = driver.find_elements(By.TAG_NAME, 'button')

        flight_info_list = []
        seen = set()
        flight_pattern = re.compile(
            r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})\s+([\d,]+원)\s+(\S+)'
        )

        for btn in buttons:
            text = ' '.join(btn.text.split())
            match = flight_pattern.search(text)
            if match:
                departure_time = match.group(1)
                arrival_time = match.group(2)
                fee = match.group(3)
                airline_name = match.group(4)

                key = (airline_name, departure_time, arrival_time)
                if key in seen:
                    continue
                seen.add(key)

                flight_info = {
                    "airline_name": airline_name,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "fee": fee
                }
                flight_info_list.append(flight_info)
                print(f"항공편 추가: {airline_name} {departure_time}-{arrival_time} ({fee})")

        print(f"총 {len(flight_info_list)}개 항공편 발견")
        return flight_info_list

    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []

    finally:
        driver.quit()
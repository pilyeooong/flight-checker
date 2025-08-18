import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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
        # React 앱 로딩을 위해 충분한 시간 대기
        time.sleep(20)
        
        # 페이지 스크롤로 동적 콘텐츠 로딩 트리거
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 새로운 선택자로 항공편 데이터 추출
        flight_info_list = []
        
        # 항공사명 요소들 찾기
        airline_elements = soup.find_all('p', class_='text__Text-sc-365491ba-0 dgsTUN')
        # 시간 요소들 찾기  
        time_elements = soup.find_all('p', class_='text__Text-sc-365491ba-0 dkOzsE')
        
        print(f"발견된 항공사: {len(airline_elements)}개, 시간: {len(time_elements)}개")
        
        # 항공사와 시간 데이터를 매칭하여 항공편 정보 생성
        min_count = min(len(airline_elements), len(time_elements))
        
        for i in range(min_count):
            airline_name = airline_elements[i].text.strip() if airline_elements[i] else None
            time_text = time_elements[i].text.strip() if time_elements[i] else None
            
            # 시간 텍스트에서 출발시간과 도착시간 분리 (예: "07:55 - 09:10")
            departure_time = None
            arrival_time = None
            
            if time_text and ' - ' in time_text:
                times = time_text.split(' - ')
                if len(times) == 2:
                    departure_time = times[0].strip()
                    arrival_time = times[1].strip()
            
            # 가격 정보는 현재 명확한 선택자를 찾지 못했으므로 None으로 설정
            # 추후 가격 선택자가 확인되면 추가 가능
            fee = None
            
            if airline_name and departure_time and arrival_time:
                flight_info = {
                    "airline_name": airline_name,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "fee": fee
                }
                flight_info_list.append(flight_info)
                print(f"항공편 추가: {airline_name} {departure_time}-{arrival_time}")
        
        return flight_info_list
        
    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []

    finally:
        driver.quit()
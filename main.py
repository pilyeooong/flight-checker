import time
import traceback
from dotenv import load_dotenv
import os
from crawler import get_flight_schedules
from slack import send_slack_webhook
import random
import re

load_dotenv()

def main():
    while True:
        urls_str = os.getenv('FLIGHT_SCHEDULE_URL')
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        # 쉼표로 구분된 URL들을 리스트로 변환
        urls = [url.strip() for url in urls_str.split(',') if url.strip()]
        
        all_messages = []
        found_any_flights = False
        
        for url in urls:
            try:
                # URL에서 날짜 추출 (YYYYMMDD 형식)
                date_match = re.search(r'-(\d{8})', url)
                if date_match:
                    date_str = date_match.group(1)
                    formatted_date = f"{date_str[:4]}년 {date_str[4:6]}월 {date_str[6:8]}일"
                else:
                    formatted_date = "날짜 정보 없음"
                
                # URL에서 노선 정보 추출
                route_match = re.search(r'[ac]:([A-Z]+)-[ac]:([A-Z]+)', url)
                if route_match:
                    departure = route_match.group(1)
                    arrival = route_match.group(2)
                    route_info = f"{departure} → {arrival}"
                else:
                    route_info = "노선 정보 없음"
                
                print(f"크롤링 중: {route_info} ({formatted_date})")
                schedules = get_flight_schedules(url)
                
                if schedules:
                    found_any_flights = True
                    # 헤더에 날짜와 노선 정보 추가
                    header = f"✈️ *{route_info} ({formatted_date})*\n"
                    header += f"🔍 *발견된 항공편: {len(schedules)}개*\n"
                    header += f"🔗 <{url}|예약 페이지 바로가기>\n\n"
                    
                    flights_info = "\n".join([
                        f"*{schedule['airline_name']}*\n⏰ {schedule['departure_time']} → {schedule['arrival_time']}"
                        + (f"\n💰 {schedule['fee']}" if schedule['fee'] else "") + "\n"
                        for schedule in schedules
                    ])
                    
                    all_messages.append(header + flights_info)
                else:
                    # 항공편이 없는 경우도 기록
                    no_flight_msg = f"📅 {formatted_date} ({route_info})\n예약 가능 스케줄이 없습니다.\n"
                    all_messages.append(no_flight_msg)

            except Exception as e:
                error_msg = f"❌ {url} 크롤링 오류: {str(e)}\n"
                all_messages.append(error_msg)
                print(f"Error crawling {url}: {e}")
        
        # 모든 메시지 결합
        if all_messages:
            # 항공편이 하나라도 있으면 @channel 태그 추가
            if found_any_flights:
                final_message = "<!channel>\n" + "="*30 + "\n" + ("\n" + "="*30 + "\n").join(all_messages)
            else:
                final_message = "="*30 + "\n" + ("\n" + "="*30 + "\n").join(all_messages)
            
            send_slack_webhook(webhook_url, final_message)
        
        random_number = random.randint(30, 60)
        time.sleep(random_number)

if __name__ == "__main__":
    main()

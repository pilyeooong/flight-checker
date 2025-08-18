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
        url = os.getenv('FLIGHT_SCHEDULE_URL')
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')

        try:
            # URL에서 날짜 추출 (YYYYMMDD 형식)
            date_match = re.search(r'-(\d{8})', url)
            if date_match:
                date_str = date_match.group(1)
                formatted_date = f"{date_str[:4]}년 {date_str[4:6]}월 {date_str[6:8]}일"
            else:
                formatted_date = "날짜 정보 없음"
            
            # URL에서 노선 정보 추출
            route_match = re.search(r'a:([A-Z]+)-a:([A-Z]+)', url)
            if route_match:
                departure = route_match.group(1)
                arrival = route_match.group(2)
                route_info = f"{departure} → {arrival}"
            else:
                route_info = "노선 정보 없음"
            
            schedules = get_flight_schedules(url)
            if schedules:
                # 헤더에 날짜와 노선 정보 추가
                header = f"✈️ *{route_info} ({formatted_date})*\n"
                header += f"🔍 *발견된 항공편: {len(schedules)}개*\n\n"
                
                flights_info = "\n".join([
                    f"*{schedule['airline_name']}*\n⏰ {schedule['departure_time']} → {schedule['arrival_time']}"
                    + (f"\n💰 {schedule['fee']}" if schedule['fee'] else "") + "\n"
                    for schedule in schedules
                ])
                
                message = "<!channel>\n" + header + flights_info
            else:
                message = f"📅 {formatted_date} ({route_info})\n예약 가능 스케줄이 없습니다."

        except Exception as e:
            message = f"Error sending message: {e}\n{traceback.format_exc()}"

        send_slack_webhook(webhook_url, message)
        
        random_number = random.randint(30, 60)
        time.sleep(random_number)

if __name__ == "__main__":
    main()

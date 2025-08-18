## flight checker
- 비행기 좌석 확인이 번거로워서 크롤링 + 슬랙 조합으로 좌석이 생기면 노티를 보내는 스크립트
- 인터파크 투어 사이트를 기반으로 좌석을 조회한다.

### 사용 스택
- python 3.10
- selenium
- slack webhook

### 실행 방법
알림을 받아볼 Slack 채널의 Webhook URL과, 조회가 필요한 항공권 사이트 URL이 필요하며 환경변수로 등록되어야합니다.
환경 변수 값의 예시는 아래와 같습니다.
- `SLACK_WEBHOOK_URL`
  - https://xxx.slackwebhook.com
- `FLIGHT_SCHEDULE_URL`
  - https://travel.interpark.com/air/search/a:CJU-a:GMP-20250822?adult=2&child=0&infant=0&cabin=ECONOMY&byAirline=

1. git clone
2. pip install -r requirements.txt
3. python main.py

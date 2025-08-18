# Flight Checker 프로젝트 개요

## 프로젝트 목적
인터파크 투어 항공권 예약 사이트를 모니터링하여 원하는 좌석이 생기면 슬랙으로 알림을 보내는 자동화 스크립트

## 핵심 기능
- **자동 크롤링**: 인터파크 투어 사이트에서 항공 스케줄 조회
- **슬랙 알림**: 예약 가능한 좌석 발견 시 슬랙 채널로 실시간 알림
- **무한 모니터링**: 30-60초 랜덤 간격으로 지속적인 감시

## 기술 스택
- Python 3.10
- Selenium (웹 자동화)
- BeautifulSoup (HTML 파싱)
- Slack Webhook API
- Heroku 배포 지원

## 주요 파일 구조
- `main.py` - 메인 실행 파일, 무한 루프로 모니터링
- `crawler.py` - 웹 크롤링 로직, 항공 스케줄 데이터 추출
- `slack.py` - 슬랙 웹훅 메시지 전송
- `requirements.txt` - Python 패키지 의존성
- `Procfile` - Heroku 배포 설정

## 환경 변수
- `SLACK_WEBHOOK_URL`: 슬랙 웹훅 URL
- `FLIGHT_SCHEDULE_URL`: 모니터링할 인터파크 항공권 페이지 URL

## 실행 방법
1. 환경 변수 설정
2. `pip install -r requirements.txt`
3. `python main.py`
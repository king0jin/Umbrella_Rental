# Umbrella_Rental
하이브리드 클라우드를 이용한 메시지 발송 이중화
+ 퍼블릭 클라우드로 메세지 전송시 발생하는 장애를 사내에서 프라이빗 클라우드에서 처리할 수 있도록 구현
---
## 메세지 전송 플랫폼 : 우산 대여 예약 시스템
사용자와 시스템 간의 메세지 전송

### Stack
+ Server : Django
+ Clinet : React
+ Database : MariaDB
+ Public Cloud : AWS
+ Private Cloud : Open Stack
+ Message Brocker : RabbitMQ, Kafka
+ Alarm : Slack WebHook API

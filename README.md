***
안녕하세요, 인사 담당자님!
이번에 과재를 재출하는 황정연 입니다.
평소 사용하지 않았던 프래임워크와 언어를 강의를 찾아서 배우느라 시간이 조금 걸렸습니다만,
새로운 것을 접할 수 있어서 소중한 기회였습니다!
***


## 데이터베이스 선택 사유
부트캠프 시절부터 학습해온 MySQL과 MongoDB 중에 무엇을 선택할까 고민하였습니다. 코딩테스트 과제에서 요구한 필수 기능 뿐만 아니라, 보너스 기능을 추가할 경우 전체 column은 index, original_key, short_key, Date, status 이렇게 5개로 확장되는 만큼, 관리가 용이한 table 형태의 DB를 선택하는 것이 용이하다 판단하였습니다.
<br>
<br>
저장 될 데이터가 방대해져 filter 매서드로 row를 검색하는 데 지연현상을 고려하여, index의 경우 삭제 처리 대신 값을 null이나 무의미한 값으로 update하는 방식으로 처리하였습니다.
<br>
<br>
현재 본 서비스는 AWS의 EC2와 RDS에서 배포된 상태이며, http의 퍼블릭 주소로 접근이 가능합니다. 또한 insomnia와 같은 API 테스트 도구를 통해 json body로 데이터 송수신이 가능한 상태입니다. 무료 서버를 이용하는 만큼 향후 2주 간 인스턴스를 활성화 상태로 놓을 예정입니다. 
<br>
<br>
<br>
<br>
## 기능 및 구현 소개

**단축 URL 생성**
- 요청은 json body 형태로 받으며, 반드시 필요한 데이터는 original_url과 validation_date입니다.
- 각각 원래 url 주소와, 해당 주소로 생성돈 short_url의 유효기간을 validation_date로 받습니다.
- 별도의 generate_hashed_url 함수를 생성하여, 해당 함수로 해쉬화된 url을 생성하도록 하였습니다.
- 생성된 short_url은 DB내 저장이 되며, 최종적으로 반환됩니다.
<br>

**리다이렉션**
- 퍼블릭 주소/short_key 형식의 주소를 받습니다
- db내에서 filter 함수를 이용하여 short_key와 일치하는 short_url을 찾습니다.
- 없을 경우 에러를 반환하며, 찾은 컬럼의 status를 +1 을 하여 조회수를 update 합니다.
<br>

**통계 기능**
- 퍼블릭 주소/status/short_key 형식의 주소를 받습니다.
- 로직은 다소 간소한데, short_key에 해당되는 row를 찾은 다음, 해당 row의 status를 반환하는 구조입니다.
<br>

**URL 키 만료 기능**
- scheduler를 사용하여 하루를 주기로 db 전체를 순회합니다.
- 순회하여 현재 시스템 날짜보다 validation_date가 작은 row를 모두 찾습니다.
- validation_date, original_url, short_url을 null 값으로 처리하여, 추후 동일한 original_url을 입력해도 기능하도록 하였습니다.
<br>
<br>
<br>
<br>

## Swagger 및 명세서
Swagger 명세서의 

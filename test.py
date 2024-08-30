import requests
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


#임의의 url과 날짜를 보내 short_url이 생성되는 지 확인하는 테스트입니다.
#한번 실시할 때마다 original_url이 실제 db에 입력되는 것이 확인되나,
#original_url은 unique하기 때문에 1회만 유요합니다.
def test_post_url():

    payload = {
        "original_url" : "abcdefge",
        "date" : "2024-10-10" 
    }
    
    #response = client.post(f"/shorten", json=payload)
    #data = response.json()
    #assert "short_url" in data
    #assert data is not None



#status를 확인하여 조회수가 출력되는 지 확인하는 테스트입니다.
#short_url은 기간이 유효한 것을 대상으로 해야 합니다.
def test_get_status():
    short_url = "20cb1abced625f3f38f5"
    response = client.get(f"/status/{short_url}")
    data = response.json()
    assert "status" in data



#리다이렉션 메서드를 확인합니다. 
#반환하는 string이 일반 주소형태인지 확인하여 정상적으로
#https로 시작하는 주소를 반환하는지 검증합니다.

#request.get이 아닌 client.get으로 하니 계속 실패 메시지가 나오는데,
#아직 원인을 찾지 못해 고민 중에 있습니다.
def test_get_short_url():

    #리다이렉트 하기 전 status의 값을 저장합니다.
    short_url = "20cb1abced625f3f38f5"
    status_before = check_status(short_url)

    response = requests.get("http://43.201.5.12/20cb1abced625f3f38f5", allow_redirects=True)
    data = response.url

    #이후의 status의 값을 저장합니다.
    status_after = check_status(short_url)

    assert data is not None
    #https:// 로 시작되는 정상적인 리다이렉트 주소가 반환되는지 확인합니다.
    assert data.startswith("https://")
    #status가 +1 증가하였는지 확인합니다.
    assert status_before + 1 == status_after


def check_status(short_url: str):
    response = client.get(f"/status/{short_url}")
    data = response.json()
    status = data["status"]
    return status
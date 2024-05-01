def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "https://kauth.kakao.com/oauth/authorize" in response.headers["location"]

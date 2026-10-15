from fastapi.testclient import TestClient

from app_final import APP_VERSION, MAX_N, app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": APP_VERSION}


def test_factorial():
    response = client.get("/factorial/5")
    assert response.status_code == 200
    assert response.json()["result"] == 120


def test_permutations():
    response = client.get("/permutations?n=5&k=2")
    assert response.status_code == 200
    assert response.json()["result"] == 20
    assert response.json()["explanation"] == "A(5,2) = 5! / 3! = 20"


def test_permutations_with_repeat():
    response = client.get("/permutations?n=3&k=2&repeat=true")
    assert response.json()["result"] == 9


def test_combinations():
    response = client.get("/combinations?n=5&k=2")
    assert response.status_code == 200
    assert response.json()["result"] == 10
    assert response.json()["explanation"] == "C(5,2) = 5! / (2! · 3!) = 10"


def test_combinations_with_repeat():
    response = client.get("/combinations?n=3&k=2&repeat=true")
    assert response.json()["result"] == 6


def test_k_greater_than_n_returns_400():
    response = client.get("/combinations?n=2&k=5")
    assert response.status_code == 400


def test_negative_number_returns_400():
    response = client.get("/factorial/-1")
    assert response.status_code == 400


def test_too_big_number_returns_400():
    response = client.get(f"/factorial/{MAX_N + 1}")
    assert response.status_code == 400


def test_choose():
    response = client.get("/choose?order=false&repeat=false")
    assert response.status_code == 200
    assert response.json()["name"] == "Сочетания без повторений"


def test_cheatsheet():
    response = client.get("/cheatsheet")
    assert response.status_code == 200
    assert len(response.json()["formulas"]) == 4
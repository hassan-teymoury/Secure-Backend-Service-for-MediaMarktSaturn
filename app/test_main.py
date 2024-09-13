from fastapi.testclient import TestClient
from .main import app


client = TestClient(app)


def test_get_users():
    response = client.get("/users", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200
    
    
def test_get_single_user():
    response = client.get("/users/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_products():
    response = client.get("/products", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_product():
    response = client.get("/products/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200
    
    
def test_get_product_tags():
    response = client.get("/product_tags", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_product_tag():
    response = client.get("/product_tags/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200



def test_get_companies():
    response = client.get("/companies", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_company():
    response = client.get("/companies/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_companies():
    response = client.get("/companies", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_company():
    response = client.get("/companies/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200


def test_get_bank_accounts():
    response = client.get("/bank_accounts", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200
    
    
def test_get_bank_accounts():
    response = client.get("/bank_accounts", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200



def test_get_bank_account():
    response = client.get("/bank_accounts/1", headers={"Authorization": "Bearer <MyToken>"})
    assert response.status_code == 200
    


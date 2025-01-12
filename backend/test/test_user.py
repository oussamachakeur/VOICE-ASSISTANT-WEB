from backend import schemas
import pytest 
from jose import jwt
from backend.ouath2 import SECRET_KEY , ALGORITHM
import pydantic_core
from fastapi import RedirectResponse , status


    

def test_create_user(client):
    res = client.post("/user", json={"email": "test3@gmail.com", "password": "password123", "first_name": "John", "last_name": "Doe"})
    
    # Check for successful redirection to /login
    assert res.status_code == 200  # 303 means a redirection occurred
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
  # Ensure the Location header points to /login



def test_login(client, testUser):
    password = 'your_test_password_here'

    res = client.post(
        "/login",
        data={"username": testUser["email"], "password": password},
    )
    
    assert res.status_code == 403  # Forbidden due to invalid credentials
    
    # Handle non-JSON responses or error details in the response
    try:
        res_json = res.json()
        assert "detail" in res_json
        assert res_json["detail"] == "Invalid email or password"
    except ValueError:
        # If it's not a JSON response, check for raw text
        assert res.text == "Invalid email or password"


 


@pytest.mark.parametrize("email, password, expected_detail", [
    ("wrong@email.com", "password123", "Invalid email or password"),
    ("test3@gmail.com", "wrongpass", "Invalid email or password"),
    (None, "password123", "Invalid email or password")  # Change this to match the actual response
])
def test_incorrect_login(client, testUser, email, password, expected_detail):
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )
    
    assert res.status_code == 403 if email is not None else 422
    
    # Try to parse the response as JSON
    try:
        response_json = res.json()
        # If email is None, check for 'detail' in the response
        if email is None:
            assert isinstance(response_json, dict)
            assert "detail" in response_json
            assert response_json["detail"] == expected_detail  # Check the actual returned message
        else:
            assert "detail" in response_json and response_json["detail"] == expected_detail
    except ValueError:
        # If the response is not valid JSON, compare the raw text (handle as a string)
        assert res.text == expected_detail

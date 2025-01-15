import requests

url = "http://127.0.0.1:8000"  


def test_user_endpoint():
    response = requests.get(url+"/user")
    assert response.status_code == 200
    
def test_create_user():
    payload= {
        "first_name": "test",
        "last_name": "test",
        "email": "test@gamil.com",
        "password": "1234"
    }
    response = requests.post(url+"/user" , json= payload)
    assert response.status_code == 500


def test_login_endpoint():
    response = requests.get(url+"/login")
    assert response.status_code == 200


def test_successful_login():

    payload = {
        "username":"gandi@gmail.com",
        "password":"1234"
    }
    response = requests.post(url+"/login" , data= payload)
    assert response.status_code == 200


def test_wrong_login():
    payload1 = {
        "username":"wrong@gmail.com",
        "password":"1234"
    }
    payload2 = {
        "username":"gandi@gmail.com",
        "password":"wrong-email"
    }
    response1 = requests.post(url+"/login" , data= payload1)
    response2 = requests.post(url+"/login" , data= payload2)
    assert response1.status_code == 403
    assert response2.status_code == 403


def test_feedback_endpoint():
    response = requests.get(url+"/feedbacks")
    assert response.status_code == 200

def test_send_feedback():
    payload = {
        "title": "test title",
        "email": "ustster@gmail.com",
        "content": "hello ths is test"
        }
    response = requests.post(url+"/feedbacks" , data= payload)
    assert response.status_code == 401 #her is 401 because it cant do a feedback withjout a login user 
                                        # hence 401 is for unauthorized user 
    
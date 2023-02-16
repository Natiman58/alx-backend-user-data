#!/usr/bin/env python3
"""
    The main integration testing module
"""
import requests
url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
        register the user to the database
        with the given email and password
    """
    response = requests.post(url+'/users', json_data={"email": email, "password": password})
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        assert response.status_code == 400
        assert response.json() == {"message": "email already registered"}

def log_in_wrong_password(email: str, password: str) -> None:
    """
        test if login with wrong password fails
    """
    response= requests.post(url+'/sessions', json_data={"email": email, "password": password})
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """
        test if login is successful
    """
    response = requests.post(url+'/sessions', json_data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "password": password}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
        test if the user is not logged in
    """
    response = requests.delete(url+'/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
        test if the user is logged in
    """
    response = requests.get(url+'/profile', json_data={"session_id": session_id})
    assert response.status_code == 200



def log_out(session_id: str) -> None:
    """
        test if the user is logged out
    """
    response = requests.delete(url+'/sessions', jason_data={"session_id": session_id})
    assert response.status_code == 403

def reset_password_token(email: str) -> str:
    """
        test reset password functionality
    """
    response = requests.post(url+'/reset_passowrd', json_data={"email": email})
    if response.status_code == 200:
        assert response.status_code == 200
    assert response.status_code == 401


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
        test the update password functionality
    """
    response = requests.put(url+'/reset_passord', json_data={"email": email})
    assert response.status_code == 200




EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
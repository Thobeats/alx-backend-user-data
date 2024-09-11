#!/usr/bin/env python3
"""Integration test module"""
import requests


url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Test Register User
     http://127.0.0.1:5000/users POST
     args: email, password
    """
    reg_url = f"{url}/users"
    response = requests.post(reg_url,
                             data={"email": email, "password": password})
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Test Log in Wrong Password
     http://127.0.0.1:5000/sessions POST
     args: email, password
    """
    login_url = f"{url}/sessions"
    response = requests.post(login_url,
                             data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test Log in
     http://127.0.0.1:5000/sessions POST
     args: email, password
    """
    login_url = f"{url}/sessions"
    response = requests.post(login_url,
                             data={"email": email, "password": password})
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test Profile Unlogged
     http://127.0.0.1:5000/profile GET
    """
    profile_url = f"{url}/profile"
    response = requests.get(profile_url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test Profile Logged
     http://127.0.0.1:5000/profile GET
     args: session_id
    """
    profile_url = f"{url}/profile"
    response = requests.get(profile_url,
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": response.json()["email"]}


def log_out(session_id: str) -> None:
    """Test Log out
     http://127.0.0.1:5000/sessions DELETE
     args: session_id
    """
    logout_url = f"{url}/sessions"
    response = requests.delete(logout_url,
                            cookies={"session_id": session_id})
    assert response.json()['message'] == "Bienvenue"


def reset_password_token(email: str) -> str:
    """Test Reset Password Token
     http://127.0.0.1:5000/reset_password POST
     args: email
    """
    reset_url = f"{url}/reset_password"
    response = requests.post(reset_url,
                             data={"email": email})
    assert response.status_code == 200
    assert response.json()["email"] == email
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test Update Password
      http://127.0.0.1:5000/reset_password PUT
     args: email, reset_token, new_password
    """
    update_url = f"{url}/reset_password"
    response = requests.put(update_url,
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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

import config
import requests

HEADERS = {'Authorization': f'Bearer {config.TOKEN}'}

ENDPOINTS = {
    'CREATE_USER': '/admin/v2/users/'
}


def menu_create_user():
    username = input('Username: ')
    password = input('Password: ')
    display_name = input('Display Name: ')
    full_username = f'@{username}:{config.URI}'
    url = config.MATRIX_URL + ENDPOINTS['CREATE_USER'] + full_username
    payload = {
        "password": password,
        "displayname": display_name,
        "admin": False,
        "deactivated": False
    }
    r = requests.put(url, headers=HEADERS, json=payload)
    if r.status_code >= 200 and r.status_code < 300:
        print('Success!')
        main()
    else:
        print(r)
        r.text


NAVIGATION = {
    1: menu_create_user
}


def main():
    print('(1) Create a new user')
    choice = int(input('Choose: '))
    NAVIGATION[choice]()


if __name__ == "__main__":
    main()

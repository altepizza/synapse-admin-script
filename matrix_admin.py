import config
import requests

HEADERS = {'Authorization': f'Bearer {config.TOKEN}'}

ENDPOINTS = {
    'USER_ADMIN': '/admin/v2/users'
}


def get_all_users():
    url = config.MATRIX_URL + ENDPOINTS['USER_ADMIN']
    r = requests.get(url, headers=HEADERS)
    users = r.json()['users']
    return users


def menu_list_all_users():
    users = get_all_users()
    for user in users:
        print(user)
    print(f'--- Total Users: {len(users)} ---')
    input("Press Enter to continue...")
    main()


def menu_create_user():
    username = input('Username: ')
    password = input('Password: ')
    display_name = input('Display Name: ')
    full_username = f'@{username}:{config.URI}'
    url = config.MATRIX_URL + '/' + ENDPOINTS['USER_ADMIN'] + full_username
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
    1: menu_create_user,
    2: menu_list_all_users
}


def main():
    print('(1) Create a new user')
    print('(2) List all users')
    choice = int(input('Choose: '))
    NAVIGATION[choice]()


if __name__ == "__main__":
    main()

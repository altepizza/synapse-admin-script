import config
import requests

HEADERS = {'Authorization': f'Bearer {config.TOKEN}'}

ENDPOINTS = {
    'DEACTIVATE': '/admin/v1/deactivate/',
    'ROOMS': '/admin/v1/rooms',
    'USER_ADMIN': '/admin/v2/users'
}


def deactivate_user(user_id, erase=True):
    url = config.MATRIX_URL + ENDPOINTS['DEACTIVATE'] + user_id
    payload = {'erase': erase}

    requests.post(url, headers=HEADERS, json=payload)


def get_all_users():
    url = config.MATRIX_URL + ENDPOINTS['USER_ADMIN']

    r = requests.get(url, headers=HEADERS)
    users = r.json()['users']
    return users


def menu_create_user():
    username = input('Username: ')
    password = input('Password: ')
    display_name = input('Display Name: ')
    full_username = f'@{username}:{config.URI}'
    url = config.MATRIX_URL + '/' + ENDPOINTS['USER_ADMIN'] + full_username
    payload = {
        'password': password,
        'displayname': display_name,
        'admin': False,
        'deactivated': False
    }

    r = requests.put(url, headers=HEADERS, json=payload)
    if r.status_code >= 200 and r.status_code < 300:
        print('Success!')
        main()
    else:
        print(r)
        r.text


def menu_deactivate_users():
    print('WARNING - EXPERIMENTAL')
    print('Going to delete users accounts')
    ok = input('Continue [y/N]? ')
    simulate = input('Simulate [Y/n]? ')
    if simulate == 'n':
        simulate = False
    else:
        simulate = True
    if ok.lower() == 'y':
        search = input('Match user_id by: ')
        users = get_all_users()
        filtered_users = [u for u in users if search in u['name']]
        print('Going to delete...')
        [print(user['name']) for user in filtered_users]
        if not simulate:
            if input('Continue [y/N]? ') == 'y':
                [deactivate_user(user['name']) for user in filtered_users]
    main()


def menu_list_all_rooms():
    url = config.MATRIX_URL + ENDPOINTS['ROOMS']

    r = requests.get(url, headers=HEADERS)
    rooms = r.json()['rooms']
    for room in rooms:
        print(room)


def menu_list_all_users():
    users = get_all_users()
    for user in users:
        print(user)
    print(f'--- Total Users: {len(users)} ---')
    input("Press Enter to continue...")
    main()


NAVIGATION = {
    1: menu_create_user,
    2: menu_list_all_users,
    3: menu_deactivate_users,
    4: menu_list_all_rooms
}


def main():
    print('(1) Create a new user')
    print('(2) List all users')
    print('(3) Delete users')
    print('(4) List all rooms')
    choice = int(input('Choose: '))
    NAVIGATION[choice]()


if __name__ == "__main__":
    main()

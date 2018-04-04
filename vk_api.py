import urllib.request
import json
import datetime
import argparse

url = 'https://api.vk.com/method/friends.get?fields=bdate&user_id={}&v=5.73'
id_url = 'https://api.vk.com/method/users.get?user_ids={}&v=5.73'


class Friend:
    def __init__(self, id, name, surname, bdate):
        self.id = id
        self.name = name
        self.surname = surname
        self.bday = bdate[0]
        self.bmth = bdate[1]
        self.byear = bdate[2]

    def __str__(self):
        day = self.bday if len(str(self.bday)) == 2 else '0' + str(self.bday)
        mth = self.bmth if len(str(self.bmth)) == 2 else '0' + str(self.bmth)
        years_str = str(2018 - self.byear) + ' years' if self.byear else ''
        return "{0:10} {1:10} {2:20} {3}.{4:5} {5}\n"\
            .format(str(self.id), self.name, self.surname, day, mth, years_str)


def get_data(id):
    try:
        with urllib.request.urlopen(url.format(id)) as page:
            res = page.read()
            js = res.decode()
            data = json.loads(js)
            data = data['response']['items']
            return data
    except urllib.error.URLError:
        print('VK API is not available')
        exit(1)


def get_near_bdays(users):
    month = datetime.datetime.now().month
    day = datetime.datetime.now().month
    bdays = []
    for user in users:
        if user.bmth == month and user.bday >= day:
            bdays.append(user)
        if day > 15 and user.bmth == month + 1:
            bdays.append(user)
    bdays.sort(key=lambda x: x.bday)
    bdays.sort(key=lambda x: x.bmth)
    return bdays


def make_base(data):
    friends = []
    for e in data:
        if e.get('bdate'):
            b = list(e.get('bdate').split('.'))
            day = int(b[0])
            mth = int(b[1])
            year = int(b[2]) if len(b) > 2 else None
            bdate = (day, mth, year)
            friend = Friend(e.get('id'), e.get('first_name'), e.get('last_name'), bdate)
            friends.append(friend)
    return friends


def get_id(name):
    try:
        with urllib.request.urlopen(id_url.format(name)) as page:
            res = page.read()
            js = res.decode()
            data = json.loads(js)
            data = data['response'][0]
            return int(data['id'])
    except urllib.error.URLError:
        print('VK API is not available')
        exit(1)


def get_id():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', help="id or user name", default=268333835)
    return parser.parse_args().id


def main():
    id = get_id()
    try:
        int(id)
    except ValueError:
        id = get_id(id)

    data = get_data(id)
    friends = make_base(data)
    print(*get_near_bdays(friends))


if __name__ == "__main__":
    main()
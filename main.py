from pprint import pprint
from requests import get
from os.path import isfile
from json import loads
from validate_email import validate_email

API_KEY_FILE = 'secret.txt'
EMAIL_API_URL = 'https://api.fullcontact.com/v2/person.json?email='
NAME_API_URL = 'https://api.fullcontact.com/v2/name/normalizer.json?q='


def get_api_key(file):
    assert isfile(file), "API key file does not exist."

    with open(file, 'r') as f:
        secret = f.readline().strip()
        assert secret, "API key returning empty string."

    return secret


def email_search(api_key, email):
    assert validate_email(email)

    url = EMAIL_API_URL + email
    req = get(url, headers={'X-FullContact-APIKey': api_key})
    json_data = loads(req.text)
    return json_data


def name_search(api_key, name):
    assert name, "Name cannot be an empty string."

    url = NAME_API_URL + name
    req = get(url, headers={'X-FullContact-APIKey': api_key})
    assert req.status_code == 200

    json_data = loads(req.text)
    return json_data


if __name__ == '__main__':
    key = get_api_key(API_KEY_FILE)

    while True:
        target = input("Please enter a name or email address").strip()
        if not validate_email(target):
            pprint(name_search(key, target))
        else:
            pprint(email_search(key, target))

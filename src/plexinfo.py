import requests
import argparse
import sys
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

PLEX_ENDPOINT = 'https://plex.tv'
PLEX_SIGN_IN = 'users/sign_in.json'

PLEX_STATUS = 'status/sessions'
PLEX_TRANSCODES = 'transcode/sessions'

PLEX_PRODUCT = 'plexinfo'
PLEX_VERSION = '1'
PLEX_CLIENT = 'plexinfoclient'


def get_token(user, password):
    url = urljoin(PLEX_ENDPOINT, PLEX_SIGN_IN)
    headers = {
        'x-plex-product': PLEX_PRODUCT,
        'x-plex-version': PLEX_VERSION,
        'x-plex-client-identifier': PLEX_CLIENT,
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(user, password))

    if response.status_code == 201:
        return response.json().get('user').get('authentication_token')
    else:
        sys.exit('ERROR: Connection error, check user, password and endpoint')


def get_total_sessions(host, token):
    url = urljoin(host, PLEX_STATUS)
    headers = {
        'x-plex-product': PLEX_PRODUCT,
        'x-plex-version': PLEX_VERSION,
        'x-plex-client-identifier': PLEX_CLIENT,
        'x-plex-token': token,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return response.json().get('MediaContainer').get('size')
    else:
        sys.exit('ERROR: Connection error, check user, password and endpoint')


def get_total_transcoding_sessions(host, token):
    url = urljoin(host, PLEX_TRANSCODES)
    headers = {
        'x-plex-product': PLEX_PRODUCT,
        'x-plex-version': PLEX_VERSION,
        'x-plex-client-identifier': PLEX_CLIENT,
        'x-plex-token': token,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return response.json().get('MediaContainer').get('size')
    else:
        sys.exit('ERROR: Connection error, check user, password and endpoint')



if __name__ == "__main__":
    """
        E.G: python plexinfo.py --user=myuser --password=mypass --endpoint=http//plex.myserver.com:32400 --mode=session
        E.G: python plexinfo.py --user=myuser --password=mypass --endpoint=http//plex.myserver.com:32400 --mode=transcoding
    :return: number of concurrent viewers in that mode
    """
    # Load arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', action='store', dest='user',
                        help='Your plex.tv user', required=True)
    parser.add_argument('-p', '--password', action='store', dest='password',
                        help='Your plex.tv password', required=True)
    parser.add_argument('-e', '--endpoint', action='store', dest='endpoint',
                        help='HTTP url of the plex server', required=True)
    parser.add_argument('-m', '--mode', action='store', dest='mode',
                        help='session or transcoding', required=True)

    args = parser.parse_args()

    token = get_token(args.user, args.password)
    if args.mode == 'session':
        print(get_total_sessions(args.endpoint, token))
    elif args.mode == 'transcoding':
        print(get_total_transcoding_sessions(args.endpoint, token))
    else:
        sys.exit('ERROR: Mode {} is invalid, please set a valid one (session or transcoding)'.format(args.mode))

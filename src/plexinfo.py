import requests
import urlparse
import sys, getopt
from requests.auth import HTTPBasicAuth

PLEX_ENDPOINT = 'https://plex.tv'
PLEX_SIGN_IN = 'users/sign_in.json'

PLEX_SERVER_ENDPOINT = 'http://joker.ratxi.com:32400'
PLEX_STATUS = 'status/sessions'
PLEX_TRANSCODES = 'transcode/sessions'

PLEX_PRODUCT = 'plexinfo'
PLEX_VERSION = '1'
PLEX_CLIENT = 'tyrion'


def usage():
    print "Set parameters:"
    print " -u, --user: your plex.tv user"
    print " -p, --password: your plex.tv password"
    print " -e, --endpoint: url of the plex server"
    print " -m, --mode: session or transcoding"
    print " -h, --help: "


def get_token(user, password):
    url = urlparse.urljoin(PLEX_ENDPOINT, PLEX_SIGN_IN)
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
    url = urlparse.urljoin(host, PLEX_STATUS)
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
    url = urlparse.urljoin(host, PLEX_TRANSCODES)
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


def main(argv):
    """
        E.G: python plexinfo.py --user=jokeruser --password=xxxxx --endpoint=http//joker.ratxi.com:32400 --mode=session
        E.G: python plexinfo.py --user=jokeruser --password=xxxxx --endpoint=http//joker.ratxi.com:32400 --mode=transcoding
        E.G: python plexinfo.py --user=jokeruser --password=xxxxx --mode=session
    :param argv:
    :return:
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:p:e:m:h', ['user=', 'password=', 'endpoint=', 'mode=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-m', '--mode'):
            mode = arg
        else:
            usage()
            sys.exit(2)

    if not 'user' in locals():
        sys.exit('ERROR: User not set, please use -u to set it')
    if not 'password' in locals():
        sys.exit('ERROR: Password not set, please use -p to set it')
    if not 'endpoint' in locals():
        endpoint = PLEX_SERVER_ENDPOINT
    if not 'mode' in locals():
        sys.exit('ERROR: Mode not set, please use -m to set it')

    token = get_token(user, password)
    if mode == 'session':
        print get_total_sessions(endpoint, token)
    elif mode == 'transcoding':
        print get_total_transcoding_sessions(endpoint, token)
    else:
        sys.exit('ERROR: Mode {} is invalid, please set a valid one (session or transcoding)'.format(mode))


if __name__ == "__main__":
    main(sys.argv[1:])

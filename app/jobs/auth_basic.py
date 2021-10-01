import base64
from flask import request

def wsgi_to_bytes(data):
    """coerce wsgi unicode represented bytes to real ones"""
    if isinstance(data, bytes):
        return data
    return data.encode("latin1")  # XXX: utf8 fallback?


def bytes_to_wsgi(data):
    assert isinstance(data, bytes), "data must be bytes"
    if isinstance(data, str):
        return data
    else:
        return data.decode("latin1")


def get_authorization_header():
    """
    Return request's 'Authorization:' header as
    a two-tuple of (type, info).
    """
    header = request.environ.get('HTTP_AUTHORIZATION')

    if not header:
        return None

    header = wsgi_to_bytes(header)

    try:
        auth_type, auth_info = header.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        return None

    return auth_type, auth_info



class Authorization(dict):
    """
    A class to hold the authorization data.
    :param str auth_type: The authorization type. e.g: basic, bearer.
    """
    def __init__(self, auth_type, **kwargs):
        super(Authorization, self).__init__(**kwargs)

        self.auth_type = auth_type

class HTTPBasicAuth():
    """
    HTTP Basic authentication.
    """
    www_authenticate_realm = 'Authentication Required'

    def get_authorization(self):
        """
        Get the username and password for Basic authentication header.
        :return Authentication: The authentication data or None if it is not present or invalid.
        """
        auth = get_authorization_header()

        if not auth:
            return None

        auth_type, auth_info = auth

        if auth_type != b'basic':
            return None

        try:
            username, password = base64.b64decode(auth_info).split(b':', 1)
        except Exception:
            return None

        return Authorization('basic', username=bytes_to_wsgi(username), password=bytes_to_wsgi(password))

    def get_authenticate_header(self):
        """
        Return the value of `WWW-Authenticate` header in a
        `401 Unauthenticated` response.
        """
        return 'Basic realm="%s"' % self.www_authenticate_realm
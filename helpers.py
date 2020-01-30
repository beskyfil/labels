import hashlib
import hmac

class HookError(Exception):
    """Base class for custom exceptions"""
    pass

class NoSignatureError(HookError):
    """Exception is raised when incoming hook does not include 'X-Hub-Signature' in headers"""
    pass
class InvalidSignatureError(HookError):
    """Exception is raised when HMAC is computed from payload and it does not match with expected digest"""
    pass

class ConfigError(Exception):
    """Exception is raised when configuration file is invalid, or when required environment variables are not set"""
    pass

class HTTPError(Exception):
    """Exception raised when HTTP request fails for some reason"""
    pass


def check_github_hook(hook, secret):
    """
    Checks integrity of the webhook which app receives from GITHUB,
    it computes HMAC.

    :param hook: Hook with its original content including header and payload
    :param secret: Secret string which was included when creating webhook, it's used in HMAC
    :return: tuple of (string, integer) where string is verbose interpretation of integer status code
    """

    if not "X-Hub-Signature" in hook.headers:
        # return "OK, but unsafe", 200
        raise NoSignatureError
    request_signature = hook.headers["X-Hub-Signature"].split('=')
    secret = secret.encode("utf-8")
    digest = hmac.new(secret, hook.data, hashlib.sha1).hexdigest()
    if len(request_signature) < 2 or request_signature[0] != 'sha1' or not hmac.compare_digest(request_signature[1], digest):
        # return 'Invalid signature!', 400
        raise InvalidSignatureError
    return 'OK, valid signature', 200

def build_label(label):
    l = {}
    l['name'] = label['name']
    l['color'] = f"#{label['color']}"
    l['new_name'] = label['name']
    if 'description' in label.keys():
        l['description'] = label['description']
    return l
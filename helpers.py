import hashlib
import hmac

class HookError(Exception):
    """Base class for custom exceptions"""
    pass

class NoSignatureError(HookError):
    """This exception is raised when incoming hook does not include 'X-Hub-Signature' in headers"""
    pass
class InvalidSignatureError(HookError):
    """This exception is raised when HMAC is computed from payload and is does not match with expected digest"""
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
        raise NoSignatureError
    request_signature = hook.headers["X-Hub-Signature"].split('=')
    secret = secret.encode("utf-8")
    digest = hmac.new(secret, hook.data, hashlib.sha1).hexdigest()
    if len(request_signature) < 2 or request_signature[0] != 'sha1' or not hmac.compare_digest(request_signature[1], digest):
        raise InvalidSignatureError
    return 'OK, valid signature', 200
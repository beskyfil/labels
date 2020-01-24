import hashlib
import hmac

def check_github_hook(hook, secret):
        if not "X-Hub-Signature" in hook.headers:
            return "OK, but unsafe", 200
        request_signature = hook.headers["X-Hub-Signature"].split('=')
        secret = secret.encode("utf-8")
        digest = hmac.new(secret, hook.data, hashlib.sha1).hexdigest()
        if len(request_signature) < 2 or request_signature[0] != 'sha1' or not hmac.compare_digest(request_signature[1], digest):
            return 'Invalid signature!', 400
        return 'OK, valid signature', 200
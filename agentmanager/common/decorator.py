from agentmanager.common import log

import time

LOG = log.logger(__name__)


class Retry(object):
    default_exceptions = (Exception,)

    def __init__(self, tries, exceptions=None, delay=0, keyword=None):
        """Decorator for retrying a function if exception occurs

        tries -- num tries
        exceptions -- exceptions to catch
        delay -- wait between retries
        keyword -- keywork in exception message
        """
        self.tries = tries
        if exceptions is None:
            exceptions = Retry.default_exceptions
        self.exceptions = exceptions
        self.delay = delay
        self.keyword = keyword

    def __call__(self, f):
        def fn(*args, **kwargs):
            exception = None
            for _ in range(self.tries):
                try:
                    return f(*args, **kwargs)
                except self.exceptions as e:
                    if self.keyword is None or self.keyword in e.message:
                        LOG.warning("Retry, exception: " + str(e))
                        time.sleep(self.delay)
                        exception = e
                    else:
                        raise
            # if no success after tries, raise last exception
            raise exception
        return fn

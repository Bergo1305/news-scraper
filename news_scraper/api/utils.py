import time
from functools import wraps


def retry(exceptions, tries=5, delay=5, back_off=1, logger=None):

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            a_tries, a_delay = tries, delay

            while a_tries > 1:

                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.exception(e)
                    msg = '{}, Retrying in {} seconds...'.format(e, a_delay)

                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)

                    time.sleep(a_delay)
                    a_tries -= 1
                    a_delay *= back_off

            return f(*args, **kwargs)

        return f_retry

    return deco_retry

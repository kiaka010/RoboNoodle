import requests
import logging
import requests_cache

logger = logging.getLogger("discord.external-request")
requests_cache.install_cache('system_cache', backend='sqlite', expire_after=1)


class Request:

    def get(self, url, headers=None, params=None, expire_after='default'):
        # @todo add some exception handling here
        logger.info("Making External GET Request %s" % url)
        response = requests.request('GET', url, headers=headers, params=params, expire_after=expire_after)
        logger.debug(response)
        logger.debug("Is request cached: %s" % response.from_cache)
        if response.status_code != 200:
            logger.error("Request Failed. Status Code %s" % response.status_code)
            return False

        return response

    def post(self, url, params=None, expire_after='default'):
        # @todo add some exception handling here
        logger.info("Making External GET Request %s" % url)
        response = requests.request('POST', url, params=params, expire_after=expire_after)
        logger.debug(response)
        logger.debug("Is request cached: %s" % response.from_cache)
        if response.status_code != 200:
            logger.error("Request Failed. Status Code %s" % response.status_code)
            return False

        return response

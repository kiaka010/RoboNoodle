import requests
import logging
logger = logging.getLogger("discord.external-request")


class Request:

    def get(self, url, headers=None):
        response = requests.request('GET', url, headers=headers)
        logger.info(response)

        return response

import logging

from requests import Response

logger = logging.getLogger(__name__)


def raise_for_status_hook(response: Response, *args, **kwargs):
    logger.info(
        f"Request {response.request.url} took {response.elapsed.total_seconds()}s and returned {response.status_code}."
    )
    response.raise_for_status()

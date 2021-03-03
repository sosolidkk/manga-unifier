import requests

from urllib3.util.retry import Retry

from unifier.support.http_adapters import TimeoutHTTPAdapter
from unifier.support.http_hooks import raise_for_status_hook

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
)

adapter = TimeoutHTTPAdapter(max_retries=retries)

http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
http.hooks["response"] = [raise_for_status_hook]
http.headers.update({"Accept": "application/json"})
http.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        )
    }
)

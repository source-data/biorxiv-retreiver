from typing import Dict, List
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
#from . import logger, SCOPUS_API_KEY


def requests_retry_session(
                            retries=4,
                            backoff_factor=0.3,
                            status_forcelist=(500, 502, 504),
                            session=None,
                            ):
    """Creates a resilient session that will retry several times when a query fails.
    from  https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    Parameters
    ----------
    retries : int, optional
        As in [`urllib3.util.Retry`](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry)
    backoff_factor : float, optional
        As in [`urllib3.util.Retry`](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry)
    status_forcelist : tuple, optional
        As in [`urllib3.util.Retry`](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry)
    session : requests.Session, optional
        If existing, a valid [`requests.Session` object](https://docs.python-requests.org/en/master/user/advanced/).
        If let to `None` it will create it.

        Usage:
        ```python
        session_retry = self.requests_retry_session()
        session_retry.headers.update({
            "Accept": "application/json",
            "From": "thomas.lemberger@embo.org"
        })
        response = session_retry.post(url, data=params, timeout=30)
        ```
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class Service:
    """Parent class to setup HTTP services.
    """
    REST_URL: str = ''
    HEADERS: Dict[str, str] = {}

    def __init__(self):
        self.retry_request = requests_retry_session()
        self.retry_request.headers.update(self.HEADERS)


class BiorxivRequester(Service):
    """
    Generates resilient calls to [biorxiv API](https://api.biorxiv.org/)
    """
    def __init__(self, url: str, headers: Dict[str, str]):
        Service.__init__(self)
        """
        Generates resilient calls to [biorxiv API](https://api.biorxiv.org/)
        Parameters
        ----------
        url : str,
            URL for the API call to [biorxiv API](https://api.biorxiv.org/)
        headers : dict,
            `dict` containing the headers for the API request. Should include 'From' and 'Accept' as keys.

        Usage:
        ```python
        datagen = DatasetGenerator()
        url = datagen.url
        headers = {
                    "From": "my.email@email.acme",
                    "Accept": "application/json",
                    }
        service = BioRxivService(url, headers)
        ```
        """
        self.url = url
        self.headers = headers

    def __call__(self) -> Dict[str, str]:
        response = self.retry_request.get(self.url)
        assert response.status_code == 200, f"""problem with biorxiv api ({response.status_code}) with request {self.url}"""
        assert response.json()['messages'][0]['status'] == 'ok', f"""⚠️ The API request shows no matching results. 
                                                          {response.json()['messages'][0]['status']} ⚠️, \n{self.url}"""
        return response.json()



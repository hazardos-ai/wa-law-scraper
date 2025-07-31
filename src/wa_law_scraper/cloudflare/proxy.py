import json
from typing import Any, Dict, List, Optional

import requests


class Proxy:
    """
    A class used to manage proxies.

    Attributes
    ----------
    url : str
        URL for the request to get proxies.
    params : dict
        Parameters for the request to get proxies.
    proxies : list
        The list of proxies obtained from the request.

    Methods
    -------
    set_params(request='displayproxies', \
                protocol='all', \
                timeout='10000', \
                country='all', \
                ssl='yes', \
                anonymity='all'):
        Define the parameters for the request.
    get_list():
        Fetch the list of proxies based on the parameters.
    """

    def __init__(self, url: str = "https://api.proxyscrape.com/v2/"):
        """
        Constructs all the necessary attributes for the Proxy object.

        Parameters
        ----------
        url : str, optional
            URL for the request to get proxies (default is 'https://api.proxyscrape.com/v2/').
        """
        self.url = url
        self.params = self.set_params()
        self.proxies = self.get_list()

    def set_params(
        self,
        request: str = "displayproxies",
        protocol: str = "all",
        timeout: str = "10000",
        country: str = "all",
        ssl: str = "yes",
        anonymity: str = "all",
    ) -> Dict[str, str]:
        """
        Define the parameters for the request.

        Parameters
        ----------
        request : str, optional
            Define whether the proxies should download or display in the browser (default is 'displayproxies').
            Options:
                - 'displayproxies': display the proxies in the browser
                - 'getproxies': download the proxies
        protocol : str, optional
            Protocol of the proxies that should be downloaded. If you want to download two protocols at once, the values can be separated by a comma, E.G., protocol=socks4,socks5 (default is 'all').
        timeout : str, optional
            Timeout for the request (default is '10000').
        country : str, optional
            Country for the proxies (default is 'all').
        ssl : str, optional
            SSL for the proxies (default is 'yes').
        anonymity : str, optional
            Anonymity for the proxies (default is 'all').

        Returns
        -------
        dict
            The parameters for the request.
        """
        return {
            "request": request,
            "protocol": protocol,
            "timeout": timeout,
            "country": country,
            "ssl": ssl,
            "anonymity": anonymity,
        }

    def get_list(self) -> Optional[List[str]]:
        """
        Fetch the list of proxies based on the parameters.

        Returns
        -------
        list
            The list of proxies.
        """
        response = requests.get(self.url, params=self.params, timeout=20)
        response.raise_for_status()
        return response.text.splitlines()

    def rotate(self) -> Dict[str, str]:
        """
        Rotate the proxies

        Returns
        -------
        Dict[str, str]
            The rotated proxy
        """
        return self.proxies.pop(0) if self.proxies else None

    def length(self) -> int:
        """
        Get the number of proxies

        Returns
        -------
        int
            The number of proxies
        """
        return len(self.proxies)

    def details(self, info: str = "proxy_count") -> Any:
        """
        Get detailed information about the available proxies.

        Parameters
        ----------
        info: str, optional
            Choose what information to display about the proxies (default is 'all').
            Options:
                - "proxy_count": the number of proxies available
                - "last_updated": the last time the proxies were updated
                - "organizations": the organizations that own the proxies
                - "ports": the ports the proxies are using
                "countries": the countries the proxies are from

        Returns
        -------
        dict
            Detailed information about the available proxies, or None if the request fails.
        """
        params = {"request": "proxyinfo"}
        response = requests.get(self.url, params=params, timeout=20)
        response.raise_for_status()
        return json.loads(response.text)[info]

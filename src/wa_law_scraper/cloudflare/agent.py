from typing import List, Dict
from fake_useragent import UserAgent


class Agent:
    """
    A class used to manage user agents.

    Attributes
    ----------
    registry : dict
        The registry of operating systems, platforms, and browsers.
    generate : dict
        The generated user agent header.

    Methods
    -------
    fetch_registry(option: str) -> List[str]:
        Fetch the registry list for the given option.
    generate_user(os: str, platforms: str, browsers: str) -> Dict[str, str]:
        Generate a random user agent header.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Agent object.
        """
        self.registry = {
            "os": self.fetch_registry("os"),
            "platforms": self.fetch_registry("platforms"),
            "browsers": self.fetch_registry("browsers"),
        }
        self.generate = self.generate_user(
            self.registry["os"][2],
            self.registry["platforms"][0],
            self.registry["browsers"][2],
        )

    @staticmethod
    def fetch_registry(option: str) -> List[str]:
        """
        Fetch the registry list for the given option.

        Parameters:
        ----------
        option : str
            The option to fetch the registry list for.

        Returns:
        -------
        List[str]
            The registry list for the given option.
        """
        registry = {
            "os": ["windows", "linux", "macos"],
            "browsers": ["chrome", "firefox", "safari", "edge"],
            "platforms": ["mobile", "tablet", "pc"],
        }

        return registry.get(option, [])

    def generate_user(self, os: str, platforms: str, browsers: str) -> Dict[str, str]:
        """
        Generate a random user agent header.

        Parameters
        ----------
        os : str
            The operating system to generate the user agent header for.
        platforms : str
            The platform to generate the user agent header for.
        browsers : str
            The browser to generate the user agent header for.

        Returns
        -------
        Dict[str, str]
            The generated user agent header.
        """
        ua = UserAgent(os=os, platforms=platforms, browsers=browsers)
        browser_methods = {
            "chrome": ua.chrome,
            "firefox": ua.firefox,
            "safari": ua.safari,
            "edge": ua.edge,
        }
        if browsers in browser_methods:
            return {"User-Agent": browser_methods[browsers]}

        return {"User-Agent": ua.random}

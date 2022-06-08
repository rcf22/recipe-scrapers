import inspect
from collections import OrderedDict
from typing import Optional, Tuple, Union
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from recipe_scrapers.settings import settings

from ._schemaorg import SchemaOrg

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
}

COOKIES = {
    '_gid': 'GA1.2.482745774.1654701397',
    '_gcl_au': '1.1.298279625.1654701397',
    '_derived_epik': 'dj0yJnU9OGlZRmZhOVBLanIwdFhlckxSeExDTnJRemNlWHNpTTYmbj0zSWpYYXVieTBYODlwUkQ2S2xXRzBnJm09MSZ0PUFBQUFBR0tndlZZJnJtPTEmcnQ9QUFBQUFHS2d2Vlk',
    '_pin_unauth': 'dWlkPVlqYzFNVGMyWTJNdFlqRTVaaTAwTXpCbUxXSmlaak10WWpJMVkyUXpOV0poWXpnNA',
    'LD_U': 'https%3A%2F%2Fwww.cooksmarts.com%2F',
    'LD_R': '',
    'LD_T': '4dc37888-1598-4a78-f41e-2feda9ce4bff',
    'ahoy_visitor': 'b61fd6a6-4ce3-472e-bea9-f4176b27089f',
    'LD_L': '%7B%22p%22%3A%22true%22%2C%22email%22%3A%22elleandryanfalk%40gmail.com%22%7D',
    'remember_user_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczJOak00TlYwc0lpUXlZU1F4TUNReVUwSjBjWEJOY0RjNU1uZHpZaTVYUlZCd1NraDFJaXdpTVRZMU5EY3dNVFF3Tnk0NE1UYzBOakV6SWwwPSIsImV4cCI6IjIwMjMtMDYtMDhUMTU6MTY6NDcuODE3WiIsInB1ciI6ImNvb2tpZS5yZW1lbWJlcl91c2VyX3Rva2VuIn19--1f7093327f278590cfca82bb605c1fa8d3d8b434',
    'LD_H': '%7B%22check%22%3A%22%22%2C%22val%22%3A%2223deb2d2446305bce343034e3b841899%22%7D',
    'ahoy_visit': '20709d3c-b006-41a1-a8ab-ca65faafe220',
    '_ga': 'GA1.2.1546690630.1654701397',
    '_ga_2PGCNECQKY': 'GS1.1.1654719017.2.1.1654719018.0',
    '_cook_smarts_session': 'Kd7GY1VaxxebAGubk4srC%2BfhA6wNiV5hhFNhcl%2BdHTkcCutwk50RevnS%2Bg2qTZoZnj7UqfLiG0nFRxbuKES3QJ5NIBgtVGH%2B8QlJctjozomTUF0zBnrM4KZ78UIldmuVL5HW6OGXk6wTeTrKGeaQmN0j4vpJzkxBB53BxVUFDwoLpAE6%2FlGjH5FBG5ycFoRA0tuD1ivBgGaVBrcCFDMXhbEOaiegGyxVH%2FkagpRKx2Nh8vuI8NmYxoXyO6VbbOnh3Fm3LsJR9fpJxBAuJQIpAXckGM3nOu4JRv%2BAzCg9cVVOrlot%2BnRWMZy2LeIzDmwVYD57Qn8tRxFO8Vc1zpwUV7Fy2RD9b%2FbhxaZWxbPjRx42U0vRlgc9MuswxJtPI2pdSB8KVR9Ve7HLiy%2FRH287uJOZmTk%3D--nkTZD6JnxhWcYa8B--DShWUrjAbzO2q0t2dKABag%3D%3D',
    '_dc_gtm_UA-34061159-1': '1',
}

COOKSMARTS_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_gid=GA1.2.482745774.1654701397; _gcl_au=1.1.298279625.1654701397; _derived_epik=dj0yJnU9OGlZRmZhOVBLanIwdFhlckxSeExDTnJRemNlWHNpTTYmbj0zSWpYYXVieTBYODlwUkQ2S2xXRzBnJm09MSZ0PUFBQUFBR0tndlZZJnJtPTEmcnQ9QUFBQUFHS2d2Vlk; _pin_unauth=dWlkPVlqYzFNVGMyWTJNdFlqRTVaaTAwTXpCbUxXSmlaak10WWpJMVkyUXpOV0poWXpnNA; LD_U=https%3A%2F%2Fwww.cooksmarts.com%2F; LD_R=; LD_T=4dc37888-1598-4a78-f41e-2feda9ce4bff; ahoy_visitor=b61fd6a6-4ce3-472e-bea9-f4176b27089f; LD_L=%7B%22p%22%3A%22true%22%2C%22email%22%3A%22elleandryanfalk%40gmail.com%22%7D; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczJOak00TlYwc0lpUXlZU1F4TUNReVUwSjBjWEJOY0RjNU1uZHpZaTVYUlZCd1NraDFJaXdpTVRZMU5EY3dNVFF3Tnk0NE1UYzBOakV6SWwwPSIsImV4cCI6IjIwMjMtMDYtMDhUMTU6MTY6NDcuODE3WiIsInB1ciI6ImNvb2tpZS5yZW1lbWJlcl91c2VyX3Rva2VuIn19--1f7093327f278590cfca82bb605c1fa8d3d8b434; LD_H=%7B%22check%22%3A%22%22%2C%22val%22%3A%2223deb2d2446305bce343034e3b841899%22%7D; ahoy_visit=20709d3c-b006-41a1-a8ab-ca65faafe220; _ga=GA1.2.1546690630.1654701397; _ga_2PGCNECQKY=GS1.1.1654719017.2.1.1654719018.0; _cook_smarts_session=Kd7GY1VaxxebAGubk4srC%2BfhA6wNiV5hhFNhcl%2BdHTkcCutwk50RevnS%2Bg2qTZoZnj7UqfLiG0nFRxbuKES3QJ5NIBgtVGH%2B8QlJctjozomTUF0zBnrM4KZ78UIldmuVL5HW6OGXk6wTeTrKGeaQmN0j4vpJzkxBB53BxVUFDwoLpAE6%2FlGjH5FBG5ycFoRA0tuD1ivBgGaVBrcCFDMXhbEOaiegGyxVH%2FkagpRKx2Nh8vuI8NmYxoXyO6VbbOnh3Fm3LsJR9fpJxBAuJQIpAXckGM3nOu4JRv%2BAzCg9cVVOrlot%2BnRWMZy2LeIzDmwVYD57Qn8tRxFO8Vc1zpwUV7Fy2RD9b%2FbhxaZWxbPjRx42U0vRlgc9MuswxJtPI2pdSB8KVR9Ve7HLiy%2FRH287uJOZmTk%3D--nkTZD6JnxhWcYa8B--DShWUrjAbzO2q0t2dKABag%3D%3D; _dc_gtm_UA-34061159-1=1',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class CookSmartsScraper:
    def __init__(
        self,
        url,
        proxies: Optional[str] = None,  # allows us to specify optional proxy server
        timeout: Optional[
            Union[float, Tuple, None]
        ] = None,  # allows us to specify optional timeout for request
        wild_mode: Optional[bool] = False,
        html: Union[str, None] = None,
    ):
        if html:
            self.page_data = html
        else:
            self.page_data = requests.get(url, headers=COOKSMARTS_HEADERS, cookies=COOKIES).content
		
        self.wild_mode = wild_mode
        self.soup = BeautifulSoup(self.page_data, "html.parser")
        self.url = url
        self.schema = SchemaOrg(self.page_data)

        # attach the plugins as instructed in settings.PLUGINS
        if not hasattr(self.__class__, "plugins_initialized"):
            for name, func in inspect.getmembers(self, inspect.ismethod):
                current_method = getattr(self.__class__, name)
                for plugin in reversed(settings.PLUGINS):
                    if plugin.should_run(self.host(), name):
                        current_method = plugin.run(current_method)
                setattr(self.__class__, name, current_method)
            setattr(self.__class__, "plugins_initialized", True)

    @classmethod
    def host(cls) -> str:
        raise NotImplementedError("This should be implemented.")

    def canonical_url(self):
        canonical_link = self.soup.find("link", {"rel": "canonical", "href": True})
        if canonical_link:
            return urljoin(self.url, canonical_link["href"])
        return self.url

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def category(self):
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """total time it takes to preparate and cook the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def cook_time(self):
        """cook time of the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def prep_time(self):
        """preparation time of the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def yields(self):
        """The number of servings or items in the recipe"""
        raise NotImplementedError("This should be implemented.")

    def image(self):
        raise NotImplementedError("This should be implemented.")

    def nutrients(self):
        raise NotImplementedError("This should be implemented.")

    def language(self):
        """
        Human language the recipe is written in.

        May be overridden by individual scrapers.
        """
        candidate_languages = OrderedDict()
        html = self.soup.find("html", {"lang": True})
        candidate_languages[html.get("lang")] = True

        # Deprecated: check for a meta http-equiv header
        # See: https://www.w3.org/International/questions/qa-http-and-lang
        meta_language = (
            self.soup.find(
                "meta",
                {
                    "http-equiv": lambda x: x and x.lower() == "content-language",
                    "content": True,
                },
            )
            if settings.META_HTTP_EQUIV
            else None
        )
        if meta_language:
            language = meta_language.get("content").split(",", 1)[0]
            if language:
                candidate_languages[language] = True

        # If other langs exist, remove 'en' commonly generated by HTML editors
        if len(candidate_languages) > 1:
            candidate_languages.pop("en", None)

        # Return the first candidate language
        return candidate_languages.popitem(last=False)[0]

    def ingredients(self):
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
        raise NotImplementedError("This should be implemented.")

    def ratings(self):
        raise NotImplementedError("This should be implemented.")

    def author(self):
        raise NotImplementedError("This should be implemented.")

    def cuisine(self):
        raise NotImplementedError("This should be implemented.")

    def description(self):
        raise NotImplementedError("This should be implemented.")


    def reviews(self):    raise NotImplementedError("This should be implemented.")

    def links(self):
        invalid_href = {"#", ""}
        links_html = self.soup.findAll("a", href=True)

        return [link.attrs for link in links_html if link["href"] not in invalid_href]

    def site_name(self):
        meta = self.soup.find("meta", property="og:site_name")
        return meta.get("content") if meta else None


class AbstractScraper:
    def __init__(
        self,
        url,
        proxies: Optional[str] = None,  # allows us to specify optional proxy server
        timeout: Optional[
            Union[float, Tuple, None]
        ] = None,  # allows us to specify optional timeout for request
        wild_mode: Optional[bool] = False,
        html: Union[str, None] = None,
    ):
        if html:
            self.page_data = html
        else:
            self.page_data = requests.get(
                url, headers=HEADERS, proxies=proxies, timeout=timeout
            ).content

        self.wild_mode = wild_mode
        self.soup = BeautifulSoup(self.page_data, "html.parser")
        self.url = url
        self.schema = SchemaOrg(self.page_data)

       # attach the plugins as instructed in settings.PLUGINS
        if not hasattr(self.__class__, "plugins_initialized"):
            for name, func in inspect.getmembers(self, inspect.ismethod):
                current_method = getattr(self.__class__, name)
                for plugin in reversed(settings.PLUGINS):
                    if plugin.should_run(self.host(), name):
                        current_method = plugin.run(current_method)
                setattr(self.__class__, name, current_method)
            setattr(self.__class__, "plugins_initialized", True)

    @classmethod
    def host(cls) -> str:
        """get the host of the url, so we can use the correct scraper"""
        raise NotImplementedError("This should be implemented.")

    def canonical_url(self):
        canonical_link = self.soup.find("link", {"rel": "canonical", "href": True})
        if canonical_link:
            return urljoin(self.url, canonical_link["href"])
        return self.url

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def category(self):
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """total time it takes to preparate and cook the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def cook_time(self):
        """cook time of the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def prep_time(self):
        """preparation time of the recipe in minutes"""
        raise NotImplementedError("This should be implemented.")

    def yields(self):
        """The number of servings or items in the recipe"""
        raise NotImplementedError("This should be implemented.")

    def image(self):
        raise NotImplementedError("This should be implemented.")

    def nutrients(self):
        raise NotImplementedError("This should be implemented.")

    def language(self):
        """
        Human language the recipe is written in.

        May be overridden by individual scrapers.
        """
        candidate_languages = OrderedDict()
        html = self.soup.find("html", {"lang": True})
        candidate_languages[html.get("lang")] = True

        # Deprecated: check for a meta http-equiv header
        # See: https://www.w3.org/International/questions/qa-http-and-lang
        meta_language = (
            self.soup.find(
                "meta",
                {
                    "http-equiv": lambda x: x and x.lower() == "content-language",
                    "content": True,
                },
            )
            if settings.META_HTTP_EQUIV
            else None
        )
        if meta_language:
            language = meta_language.get("content").split(",", 1)[0]
            if language:
                candidate_languages[language] = True

        # If other langs exist, remove 'en' commonly generated by HTML editors
        if len(candidate_languages) > 1:
            candidate_languages.pop("en", None)

        # Return the first candidate language
        return candidate_languages.popitem(last=False)[0]

    def ingredients(self):
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
        raise NotImplementedError("This should be implemented.")

    def ratings(self):
        raise NotImplementedError("This should be implemented.")

    def author(self):
        raise NotImplementedError("This should be implemented.")

    def cuisine(self):
        raise NotImplementedError("This should be implemented.")

    def description(self):
        raise NotImplementedError("This should be implemented.")


    def reviews(self):    raise NotImplementedError("This should be implemented.")

    def links(self):
        invalid_href = {"#", ""}
        links_html = self.soup.findAll("a", href=True)

        return [link.attrs for link in links_html if link["href"] not in invalid_href]

    def site_name(self):
        meta = self.soup.find("meta", property="og:site_name")
        return meta.get("content") if meta else None

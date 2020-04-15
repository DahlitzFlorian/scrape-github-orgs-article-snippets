# scrape_github_orgs.py

import re

from typing import List

import lxml
import requests

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from lxml import etree
from lxml.html import clean

orgs_nav_classes = "subnav mb-2 d-flex flex-wrap"


def get_user_org_hyperlinks(username: str) -> ResultSet:
    url = f"https://github.com/users/{username}/contributions"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    nav = soup.find("nav", class_=orgs_nav_classes)
    tmp_orgs = nav.find_all("a")

    return tmp_orgs


def extract_orgs(tmp_orgs: ResultSet) -> List[str]:
    cleaner = clean.Cleaner()
    cleaner.safe_attrs_only = True
    cleaner.safe_attrs = frozenset(["class", "src", "href", "target"])

    html_tags = re.compile("<.*?>")
    orgs = []

    for org in tmp_orgs:
        tmp_org = str(org)
        org_name = re.sub(
            html_tags,
            "",
            re.search(r"<a(.*)@(.*)</a>", tmp_org, flags=re.DOTALL).group(2).strip(),
        )

        tree = lxml.html.fromstring(tmp_org)
        tree.attrib["href"] = f"https://github.com/{org_name}"
        tree.attrib["class"] = "org"
        tree.set("target", "_blank")
        etree.strip_tags(tree, "div")
        cleaned = cleaner.clean_html(tree)
        orgs.append(lxml.html.tostring(cleaned).decode("utf-8"))

    return orgs


def get_user_orgs(username: str) -> List[str]:
    tmp_orgs = get_user_org_hyperlinks(username)
    return extract_orgs(tmp_orgs)

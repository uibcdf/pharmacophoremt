"""Render the real footer against builder-provided paths at different depths."""

import unittest
from html.parser import HTMLParser
from pathlib import Path
from posixpath import normpath
from urllib.parse import urlsplit

from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parents[2]


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.active = [dict(attrs).get("href"), ""]

    def handle_data(self, data):
        if self.active is not None:
            self.active[1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.active is not None:
            self.anchors.append(self.active)
            self.active = None


class TestDocumentationFooter(unittest.TestCase):
    def check_page(self, page, expected_url):
        requested = []

        def pathto(document):
            requested.append(document)
            self.assertEqual(document, "content/about/who")
            self.assertTrue((ROOT / "docs" / (document + ".md")).is_file())
            # Independent declared builder-context URLs, not a local copy of
            # Sphinx's routing implementation. Full rendering is checked apart.
            return expected_url

        template = Environment(undefined=StrictUndefined, autoescape=True).from_string(
            (ROOT / "docs/_templates/copyright.html").read_text()
        )
        rendered = Anchors()
        rendered.feed(template.render(pathto=pathto))
        contributors = [
            href
            for href, label in rendered.anchors
            if "and contributors" in " ".join(label.split())
        ]
        self.assertEqual(contributors, [expected_url])
        self.assertEqual(requested, ["content/about/who"])
        url = urlsplit(contributors[0])
        target = normpath(str(Path(page).parent / url.path)) if url.path else page
        self.assertEqual(target, "content/about/who.html")

    def test_root_page_preserves_the_contributor_target(self):
        self.check_page("index.html", "content/about/who.html")

    def test_user_page_preserves_the_contributor_target(self):
        self.check_page("content/user/chemical_libraries.html", "../about/who.html")

    def test_deep_api_page_preserves_the_contributor_target(self):
        self.check_page(
            "api/users/autosummary/operation.html", "../../../content/about/who.html"
        )

    def test_contributor_page_keeps_its_self_link(self):
        self.check_page("content/about/who.html", "#")


if __name__ == "__main__":
    unittest.main()

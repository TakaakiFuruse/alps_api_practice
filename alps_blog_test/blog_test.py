from pandas.core.indexes.base import Index
import requests
from requests_toolbelt import sessions

SERVER_URL = "http://127.0.0.1:5000"
S = sessions.BaseUrlSession(base_url=SERVER_URL)


def test_Index_page_returns_200():
    assert S.get("/").status_code == 200


def test_Blog_page_returns_200():
    index = S.get("/").json()
    go_blog = list(filter(lambda x: x["id"] == "goBlog", index["alps"]["descriptor"]))
    assert S.get(go_blog[0]["href"]).status_code == 200


def test_Blog_page_shows_blog_postings():
    index = S.get("/").json()
    go_blog = list(filter(lambda x: x["id"] == "goBlog", index["alps"]["descriptor"]))
    blog_postings = S.get(go_blog[0]["href"]).json()
    assert (
        len(
            list(
                filter(
                    lambda x: x["id"] == "BlogPosting",
                    blog_postings["alps"]["descriptor"],
                )
            )
        )
        > 0
    )

import trafilatura
from bs4 import BeautifulSoup

URL = "https://as.its-kenpo.or.jp/apply/calendar?s=MDVXWXlWWFkwTlhaeTFUWndsSGRmVjJZcFpuY2xObko0TURNeTBEWnBaU1oxSkhkOWtIZHcxV1o%3D&join_date=2024-09-22"

if __name__ == "__main__":
    # python -m src.demo
    data = trafilatura.fetch_url(URL)
    print(data)

    # # とりあえずテキストをいい感じに抜き出す
    # formatted_text = trafilatura.extract(data, include_formatting=True)
    # not_formatted_text = trafilatura.extract(data, include_formatting=False)
    # if not formatted_text:
    #     msg = "No content found"
    #     raise ScrapeError(msg)

    # # BeautifulSoupでメタタグを取得
    # soup = BeautifulSoup(data, features="html.parser")
    # ogp_tags = {}
    # other_meta_tags = {}
    # for property_tag in soup.find_all("meta", attrs={"property": True}):
    #     key:str = property_tag["property"]
    #     value:str = property_tag.get("content") or property_tag.get("value")
    #     if value is None:
    #         continue
    #     if key.startswith("og:"):
    #         ogp_tags[key[3:]] = value
    #     else:
    #         other_meta_tags[key] = value

    # for name_tag in soup.find_all("meta", attrs={"name": True}):
    #     key:str = name_tag["name"]
    #     value:str = name_tag.get("content") or name_tag.get("value")
    #     if value is None:
    #         continue
    #     other_meta_tags[key] = value

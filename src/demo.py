import trafilatura
from bs4 import BeautifulSoup
import datetime

URL = "https://as.its-kenpo.or.jp/apply/calendar?s=MDVXWXlWWFkwTlhaeTFUWndsSGRmVjJZcFpuY2xObko0TURNeTBEWnBaU1oxSkhkOWtIZHcxV1o%3D&join_date=2024-09-22"

if __name__ == "__main__":
    # python -m src.demo
    data = trafilatura.fetch_url(URL)
    # print(data)

    # # HTMLファイルを読み込む
    # with open("/mnt/data/sample.html", "r", encoding="utf-8") as file:
    #     html_content = file.read()

    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(data, "html.parser")

    # タイトルを取得
    title = soup.find("h2", id="page-title").text
    print(f"レストラン: {title}")

    # 各タブの空き状況を取得する関数
    def get_availability(tab_content):
        availability = []
        # 各テーブルの行を取得
        for row in tab_content.find_all("tr"):
            # 時間を取得
            time_cell = row.find("td", class_="time-row")
            if not time_cell:
                continue
            time = time_cell.text.strip()

            # 各日付のセルを取得
            for cell in row.find_all("td")[1:]:
                date = cell.get("data-join-time")
                status = cell.text.strip()
                if date and status in ["○", "△"]:
                    datetime_str = f"{date} {time}"
                    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                    availability.append(dt)
        return availability

    # タブごとの空き状況を収集
    tabs = soup.find_all("div", class_="tabConBody")
    all_availability = []

    for tab in tabs:
        if tab.get("style") != "display:none;":
            availability = get_availability(tab)
            all_availability.extend(availability)

    # 結果を表示
    for slot in all_availability:
        print(slot)

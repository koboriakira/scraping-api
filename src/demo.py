from datetime import datetime, timedelta

import trafilatura
from bs4 import BeautifulSoup

from util.datetime import jst_now

# 「私はロボットではありません」にチェックをしてから入ったときに取得できるトークン
# "s=******" の部分を取得して貼り付ける
TOKEN = "PWN6TXdJVFBrbG1KbFZuYzAxVFp5Vkhkd0YyWWZWR2JuOTJiblpTWjFKSGQ5a0hkdzFXWg%3D%3D"

DOMAINN = "https://as.its-kenpo.or.jp"
PATH = "/apply/calendar"

SUSHI_APPLY_SERIVCE_ID_LIST = [
    2038,  # ディナー17時、テーブル席
    2039,  # ディナー19時、テーブル席
    2040,  # ディナー17時、カウンター席
    2041,  # ディナー19時、カウンター席
    2042,  # ランチ、カウンター席
    2043,  # ランチ、テーブル席
]


def get_availability(tab_content):
    """タブの空き状況を取得する"""
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


def create_url(params: dict) -> str:
    """URLを作成する"""
    param_str = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{DOMAINN}{PATH}?{param_str}"


def main():
    # 今日の日付を取得
    today = jst_now().date()

    # その週の日曜日の日付を取得
    sunday = today + timedelta(days=(6 - today.weekday()))

    # 翌週の日曜日の日付を取得
    sunday += timedelta(days=7)

    # とりあえず１回やる
    first_params = {
        "s": TOKEN,
        "join_date": sunday.strftime("%Y-%m-%d"),
        "apply_service_id": SUSHI_APPLY_SERIVCE_ID_LIST[0],
    }
    trafilatura.fetch_url(url)

    for apply_service_id in SUSHI_APPLY_SERIVCE_ID_LIST:
        url = f"{DOMAINN}{PATH}?s={TOKEN}&join_date={sunday.strftime('%Y-%m-%d')}&apply_service_id={apply_service_id}"
        print(url)
        data = trafilatura.fetch_url(url)

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(data, "html.parser")  # type: ignore

        # タイトルを取得
        title = soup.find("h2", id="page-title").text  # type: ignore
        print(f"レストラン: {title}")

        # タブごとの空き状況を収集
        tabs = soup.find_all("div", class_="tabConBody")
        all_availability = []

        for tab in tabs:
            if tab.get("style") != "display:none;":
                availability = get_availability(tab)
                all_availability.extend(availability)

        print(all_availability)


if __name__ == "__main__":
    # python -m src.demo
    main()

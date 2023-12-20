# -*- coding: utf-8 -*-

# Источник @cah_ek https://habr.com/ru/articles/565812/

import os
import googleapiclient.discovery
import csv

DEVELOPER_KEY = "******"


# Функция для скачивания корневых комментариев
def youtube(cur_video_id: str, nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.commentThreads().list(
        part="id,snippet", maxResults=100, pageToken=nextPageToken, videoId=cur_video_id
    )
    response = request.execute()
    return response


# Главная функция
def save_comment(cur_video_id: str):
    # Скачиваем комментарии
    print(f"download comments from video {cur_video_id}")
    response = youtube(cur_video_id)
    items = response.get("items")
    nextPageToken = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
    i = 1
    while nextPageToken is not None:
        print(str(i * 100))  # показываем какая сотня комментариев сейчас скачивается
        response = youtube(cur_video_id, nextPageToken)
        nextPageToken = response.get("nextPageToken")
        items = items + response.get("items")
        i += 1

    print(len(items))  # Отображаем количество скачаных комментариев

    # Сохраняем комментарии в файл csv
    print("Open csv file")
    with open(
        "youtuberesults.csv", "a", encoding="utf-8"
    ) as csv_file:  # конструкция with, чтобы файл закрылся автоматом после всех команд
        writer = csv.writer(
            csv_file, quoting=csv.QUOTE_ALL, lineterminator="\r"
        )  # использованы двойные кавычки и разделитель запятая

        # Заголовки столбцов
        row = ["id", "textOriginal"]
        print("Start write in csv")
        writer.writerow(row)  # Записываем заголовки в файл

        # Сохраняем комментарии
        print("Write comments in csv")
        for i, line in enumerate(items):
            if i == 0:
                continue
            topLevelComment = line.get("snippet").get("topLevelComment")
            row = [
                topLevelComment.get("id"),
                topLevelComment.get("snippet").get("textOriginal"),
            ]
            writer.writerow(row)

    print("done", "\n")


def main():
    video_id_list = [
        'iZov0zPBoYM',
        'v3HX345pODA'
    ]

    for cur_video_id in video_id_list:
        save_comment(cur_video_id)


if __name__ == "__main__":
    main()

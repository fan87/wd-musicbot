import aiohttp
import pytube
import json

import typing

import requests

API_KEY: str = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

class Search:

    continuation_token: str = ""
    videos: list[pytube.YouTube] = []

    def __init__(self, continuation_token: str, videos: list[pytube.YouTube]):
        self.continuation_token = continuation_token
        self.videos = videos



async def search_more(search: Search) -> Search:
    if search.continuation_token == "":
        return Search("", [])
    body: dict = {
        "context": {
            "client": {
                "clientName": 1,
                "clientVersion": "2.20210915.01.00"
            }
        },
        "continuation": search.continuation_token
    }
    videos: list[pytube.YouTube] = []
    token: str = ""
    async with aiohttp.ClientSession() as session:
        async with await session.post(url="https://www.youtube.com/youtubei/v1/search?key=" + API_KEY, json=body) as r:
            json_body = await r.json()
            for content in json_body["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]["itemSectionRenderer"]["contents"]:
                try:
                    vid: dict = content["videoRenderer"]
                    for badge in vid["badges"]:
                        try:
                            if "BADGE_STYLE_TYPE_LIVE_NOW" == badge["metadataBadgeRenderer"]["style"]:
                                is_live = True
                        except:
                            pass
                    if is_live:
                        continue
                    yt: pytube.YouTube = pytube.YouTube("https://www.youtube.com/watch?v=" + vid["videoId"])
                    yt.title = vid["title"]["runs"][0]["text"]
                    yt.author = vid["ownerText"]["runs"][0]["text"]
                    videos.append(yt)
                except:
                    pass
                try:
                    token = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                except:
                    pass

    return Search(token, videos)

async def search(query: str) -> Search:
    body: dict = {
        "context": {
            "client": {
                "clientName": 1,
                "clientVersion": "2.20210915.01.00"
            }
        },
        "query": query
    }
    videos: list[pytube.YouTube] = []
    token: str = ""
    async with aiohttp.ClientSession() as session:
        async with await session.post(url="https://www.youtube.com/youtubei/v1/search?key=" + API_KEY, json=body) as r:
            json_body = await r.json()

            for content in json_body["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
                try:
                    nc: dict = content["itemSectionRenderer"]["contents"]
                    for c in nc:
                        try:
                            vid: dict = c["videoRenderer"]
                            is_live = False
                            for badge in vid["badges"]:
                                try:
                                    if "BADGE_STYLE_TYPE_LIVE_NOW" == badge["metadataBadgeRenderer"]["style"]:
                                        is_live = True
                                except:
                                    pass
                            if is_live:
                                continue
                            yt: pytube.YouTube = pytube.YouTube("https://www.youtube.com/watch?v=" + vid["videoId"])
                            yt.title = vid["title"]["runs"][0]["text"]
                            yt.author = vid["ownerText"]["runs"][0]["text"]
                            videos.append(yt)
                        except:
                            pass
                except:
                    pass
                try:
                    token = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                except:
                    pass
    return Search(token, videos)


def sync_get_dir_url(itag: int, video_id: str) -> typing.Union[str, None]:
    body: dict = {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "16.20"
            }
        },
        "videoId": video_id
    }
    with requests.post(
            f"https://youtubei.googleapis.com/youtubei/v1/player?key={API_KEY}&contentCheckOk=true&racyCheckOk=true",
            json=body) as response:
        json_body = response.json()
        try:
            for format in json_body["streamingData"]["adaptiveFormats"]:
                try:
                    if int(format["itag"]) == itag:
                        return format["url"]
                except:
                    pass
        except:
            return pytube.YouTube("https://www.youtube.com/watch?v=" + video_id).streams.get_by_itag(itag).url
    return None

async def get_dir_url(itag: int, video_id: str) -> typing.Union[str, None]:
    body: dict = {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "16.20"
            }
        },
        "videoId": video_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://youtubei.googleapis.com/youtubei/v1/player?key={API_KEY}&contentCheckOk=true&racyCheckOk=true", json=body) as response:
            json_body = await response.json()
            try:
                for format in json_body["streamingData"]["adaptiveFormats"]:
                    try:
                        if int(format["itag"]) == itag:
                            return format["url"]
                    except:
                        pass
            except:
                return pytube.YouTube("https://www.youtube.com/watch?v=" + video_id).streams.get_by_itag(itag).url
    return None


async def get_video_details(video_id: str) -> typing.Optional[dict]:
    body: dict = {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "16.20"
            }
        },
        "videoId": video_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://youtubei.googleapis.com/youtubei/v1/player?key={API_KEY}&contentCheckOk=true&racyCheckOk=true", json=body) as response:
            json_body = await response.json()
            try:
                return json_body["videoDetails"]
            except:
                pass
    return None

def sync_get_video_details(video_id: str) -> typing.Optional[dict]:
    body: dict = {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "16.20"
            }
        },
        "videoId": video_id
    }
    json_body = requests.post(
        f"https://youtubei.googleapis.com/youtubei/v1/player?key={API_KEY}&contentCheckOk=true&racyCheckOk=true",
        json=body).json()
    try:
        return json_body["videoDetails"]
    except:
        return None

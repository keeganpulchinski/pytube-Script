import os
from pytube import Playlist, YouTube
from pytube.exceptions import AgeRestrictedError
from concurrent.futures import ThreadPoolExecutor

def download_video(video_url, download_path, downloaded_videos):
    try:
        video = YouTube(video_url)
        video_id = video.video_id

        if video_id not in downloaded_videos:
            print(f"Downloading: {video.title}")
            video.streams.get_highest_resolution().download(download_path)
            downloaded_videos.add(video_id)
        else:
            print(f"Skipping already downloaded video: {video.title}")

    except AgeRestrictedError as e:
        print(f"Skipped age-restricted video: {e.video_id}")

def download_playlist(playlist_url, download_path='./', max_threads=5):
    playlist = Playlist(playlist_url)
    downloaded_videos = set()

    # Load already downloaded videos
    if os.path.exists('downloaded_videos.txt'):
        with open('downloaded_videos.txt', 'r') as file:
            downloaded_videos.update(line.strip() for line in file.readlines())

    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(
            lambda url: download_video(url, download_path, downloaded_videos),
            playlist.video_urls
        )

    # Save the updated set of downloaded videos
    with open('downloaded_videos.txt', 'w') as file:
        file.write('\n'.join(downloaded_videos))

    print("Download completed!")

### change based on desired playlist and save location
playlist_url = "[INSERT DESIRED PLAYLIST HERE]"
download_path = "./Music"

download_playlist(playlist_url, download_path)

import youtube_dl
import re
from customexceptions import UrlException


class Downloader():
    @staticmethod
    def download_video(url):
        ydl_opts = {
            'outtmpl': './media/%(title)s.%(ext)s',
            'format': '-f bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info_dict = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info_dict)
                return filename
        except youtube_dl.utils.DownloadError:
            raise UrlException

    @staticmethod
    def download_audio(url):
        ydl_opts = {
            'outtmpl': './media/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info_dict = ydl.extract_info(url, download=False)
                filename = re.sub('m4a$', 'mp3', ydl.prepare_filename(info_dict))
                print('AAA', filename)
                return filename
        except youtube_dl.utils.DownloadError:
            raise UrlException



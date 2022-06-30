from io import BytesIO
from os import getenv
import requests
import tweepy
from PIL import Image

# Tweepy Config
auth = tweepy.OAuth1UserHandler(
    getenv("TWITTER_KEY"),
    getenv("TWITTER_SECRET"),
    getenv("ACCESS_TOKEN"),
    getenv("ACCESS_TOKEN_SECRET"),
)
api = tweepy.API(auth)


class User:
    """Convenience class to interact with Twitter API with user-context."""

    def __init__(self) -> None:
        user = api.verify_credentials(skip_status=True)
        self.screen_name = user.screen_name
        self.followers_count = user.followers_count
        self.profile_img_url = user.profile_image_url_https.replace(
            "_normal", "_400x400"
        )

    @staticmethod
    def update_avatar(file_: BytesIO) -> str:
        """Upload and update Twitter's profile image."""

        user = api.update_profile_image(filename="upload.png", file_=file_)
        return user.profile_image_url_https.replace("_normal", "_400x400")

    def fetch_avatar(self) -> Image.Image:
        """Download the untouched profile image from Twitter and save it."""

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        r = requests.get(self.profile_img_url, headers=headers)
        img = Image.open(BytesIO(r.content)).convert("RGB").resize((400, 400))
        return img

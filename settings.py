import os
from dotenv import load_dotenv


load_dotenv()

VK_LOGIN = os.environ.get("VK_LOGIN", None)
VK_PASSWORD = os.environ.get("VK_PASSWORD", None)
VK_ALBUM_URL = os.environ.get("VK_ALBUM_URL", None)
VK_APP_ID = os.environ.get("VK_APP_ID", None)


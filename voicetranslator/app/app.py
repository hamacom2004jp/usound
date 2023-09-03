from pathlib import Path
from voicetranslator.app import common
from voicetranslator.app import voicetranslator
import eel


def main(data_dir:str):
    global app_data_dir, logger
    app_data_dir = Path(data_dir)
    common.load_config()
    common.APP_DATA_DIR = app_data_dir
    eel.init("voicetranslator/app/web")
    eel.start("/index.html", size=(480, 640), port=8080, close_callback=None)


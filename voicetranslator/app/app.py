from voicetranslator.app import common
from voicetranslator.app import voicetranslator
from pathlib import Path
import eel


def main(data_dir:str):
    global app_data_dir, logger
    app_data_dir = Path(data_dir)

    common.load_config()
    common.APP_DATA_DIR = app_data_dir
    eel.init("voicetranslator/app/web")
    eel.write_intext('')
    eel.write_status('', 0, 0, 0)
    eel.start("/index.html", size=(480, 320), port=8080, close_callback=None)


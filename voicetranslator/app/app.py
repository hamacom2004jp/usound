from voicetranslator.app import common
from voicetranslator.app import voicetranslator
from pathlib import Path
import eel
import multiprocessing
import threading

def main(data_dir:str):
    global app_data_dir
    app_data_dir = Path(data_dir)

    common.APP_DATA_DIR = app_data_dir
    logger_main, _, _, _ = common.load_config()
    eel.init("voicetranslator/app/web")
    eel.write_intext('')
    eel.write_outtext('')
    eel.write_status('', 0, 0, 0)
    eel.loading_mask(False)

    logger_main.info(f"Starting run_main.")
    th_main = threading.Thread(target=voicetranslator.run_main,
                               args=(voicetranslator.RUN_MAIN,))
    th_main.start()
    logger_main.info(f"Starting run_segments.")
    voicetranslator.PROC_SEGMENT = multiprocessing.Process(target=voicetranslator.run_segments,
                                                           args=(common.APP_DATA_DIR,
                                                                 voicetranslator.RUN_MAIN,
                                                                 voicetranslator.RUN_SEGMENT))
    voicetranslator.PROC_SEGMENT.start()
    logger_main.info(f"Starting run_translate.")
    voicetranslator.PROC_TRANSFORM = multiprocessing.Process(target=voicetranslator.run_translate,
                                                             args=(common.APP_DATA_DIR,
                                                                   voicetranslator.RUN_MAIN,
                                                                   voicetranslator.RUN_TRANSFORM))
    voicetranslator.PROC_TRANSFORM.start()
    logger_main.info(f"Starting eel.")
    #eel.start("/index.html", size=(480, 320), port=8080, close_callback=None)
    eel.start("/index.html", size=(480, 320), port=8080, close_callback=voicetranslator.shutdown)

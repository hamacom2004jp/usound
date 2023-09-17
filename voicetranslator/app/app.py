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
    eel.write_status('', 0, 0, 0)
    eel.loading_mask(False)

    logger_main.info(f"Starting run_main.")
    th_main = threading.Thread(target=voicetranslator.run_main,
                               args=(voicetranslator.RUN_MAIN,))
    th_main.start()
    logger_main.info(f"Starting run_segments.")
    pr_seg = multiprocessing.Process(target=voicetranslator.run_segments,
                                     args=(common.APP_DATA_DIR,
                                           voicetranslator.RUN_MAIN,
                                           voicetranslator.RUN_SEGMENT,
                                           voicetranslator.RUN_TRANSFORM))
    pr_seg.start()
    '''
    logger_main.info(f"Starting run_translate.")
    pr_trs = multiprocessing.Process(target=voicetranslator.run_translate,
                                     args=(common.APP_DATA_DIR,
                                           voicetranslator.RUN_MAIN,
                                           voicetranslator.RUN_TRANSFORM))
    pr_trs.start()
    '''
    logger_main.info(f"Starting eel.")
    eel.start("/index.html", size=(480, 320), port=8080, close_callback=voicetranslator.shutdown)

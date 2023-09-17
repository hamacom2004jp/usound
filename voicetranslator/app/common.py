from faster_whisper import WhisperModel
from pathlib import Path
from transformers import pipeline
import eel
import logging
import logging.config
import traceback
import sys
import yaml


PGM_DIR = Path("voicetranslator")
APP_ID = 'voicetranslate'
SPEAKER_NUM = 30
APP_DATA_DIR = None


def load_config():
    global MODEL_SIZE
    global CALC_DEVICE
    global COMPUTE_TYPE
    logging.config.dictConfig(yaml.safe_load(open(PGM_DIR / "logconf.yml", encoding='UTF-8').read()))
    logger_main = logging.getLogger('vt_main')
    logger_cap = logging.getLogger('vt_cap')
    logger_seg = logging.getLogger('vt_seg')
    logger_trs = logging.getLogger('vt_trs')
    with open(PGM_DIR / 'config.yaml') as f:
        config = yaml.safe_load(f)
        c = config['voicetranslator']['common']
        MODEL_SIZE = c['MODEL_SIZE']
        CALC_DEVICE = c['CALC_DEVICE']
        COMPUTE_TYPE = c['COMPUTE_TYPE']
    return logger_main, logger_cap, logger_seg, logger_trs

def mkdirs(dir_path:Path):
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    if not dir_path.is_dir():
        raise BaseException(f"Don't make diredtory.({str(dir_path)})")
    return dir_path

def e_msg(e:Exception, logger):
    tb = sys.exc_info()[2]
    logger.error(traceback.format_exc())
    return e.with_traceback(tb)

def load_v2t_model(run_main, logger):
    logger.info(f"Load whisper model. MODEL_SIZE={MODEL_SIZE}, CALC_DEVICE={CALC_DEVICE}, COMPUTE_TYPE={COMPUTE_TYPE}")
    run_main.put('eel.loading_mask(True)')
    try:
        model_dir = mkdirs(APP_DATA_DIR / "model")
        v2t_model = WhisperModel(MODEL_SIZE, device=CALC_DEVICE, compute_type=COMPUTE_TYPE, download_root=model_dir)
        return v2t_model
    except Exception as e:
        e_msg(e, logger)
        run_main.put(f"status('{e}')")
        raise e
    finally:
        run_main.put('eel.loading_mask(False)')

def load_en2ja_model(run_main, logger):
    logger.info(f"Load translate model. en2ja_model=staka/fugumt-en-ja")
    run_main.put('eel.loading_mask(True)')
    try:
        en2ja_model = pipeline("translation", model="staka/fugumt-en-ja")
        return en2ja_model
    except Exception as e:
        e_msg(e, logger)
        run_main.put(f"status('{e}')")
        raise e
    finally:
        run_main.put('eel.loading_mask(False)')

def load_ja2en_model(run_main, logger):
    logger.info(f"Load translate model. ja2en_model=staka/fugumt-ja-en")
    run_main.put('eel.loading_mask(True)')
    try:
        ja2en_model = pipeline("translation", model="staka/fugumt-ja-en")
        return ja2en_model
    except Exception as e:
        e_msg(e, logger)
        run_main.put(f"status('{e}')")
        raise e
    finally:
        run_main.put('eel.loading_mask(False)')

def status(text, run_main=None, logger=None, start=0, end=100, now=0):
    #text = "" if text is None or text=="" else f"{text} ( remnant = {now} )"
    text = "" if text is None or text=="" else f"{text}"
    if logger is not None:
        logger.info(text)
    if run_main is None:
        eel.write_status(text, start, end, now)
    else:
        run_main.put(f'common.status("{text}")')

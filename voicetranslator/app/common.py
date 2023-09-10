from faster_whisper import WhisperModel
from pathlib import Path
from transformers import pipeline
import eel
import logging
import logging.config
import os
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
    global logger
    logging.config.dictConfig(yaml.safe_load(open(PGM_DIR / "logconf.yml", encoding='UTF-8').read()))
    logger = logging.getLogger(APP_ID)
    with open(PGM_DIR / 'config.yaml') as f:
        config = yaml.safe_load(f)
        c = config['voicetranslator']['common']
        MODEL_SIZE = c['MODEL_SIZE']
        CALC_DEVICE = c['CALC_DEVICE']
        COMPUTE_TYPE = c['COMPUTE_TYPE']

def mkdirs(dir_path:Path):
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    if not dir_path.is_dir():
        raise BaseException(f"Don't make diredtory.({str(dir_path)})")
    return dir_path

def e_msg(e:Exception, logger):
    tb = sys.exc_info()[2]
    logger.debug(traceback.format_exc())
    status(f"{e}")
    return e.with_traceback(tb)

def load_model():
    logger.info(f"Load whisper model. MODEL_SIZE={MODEL_SIZE}, CALC_DEVICE={CALC_DEVICE}, COMPUTE_TYPE={COMPUTE_TYPE}")
    model_dir = mkdirs(APP_DATA_DIR / "model")
    v2t_model = WhisperModel(MODEL_SIZE, device=CALC_DEVICE, compute_type=COMPUTE_TYPE, download_root=model_dir)
    #os.environ['HUGGINGFACE_HUB_CACHE'] = str(model_dir)
    os.environ['TRANSFORMERS_CACHE'] = str(model_dir)
    #os.environ['PYTORCH_TRANSFORMERS_CACHE'] = str(model_dir)
    logger.info(f"Load translate model. en2ja_model=staka/fugumt-en-ja, ja2en_model=staka/fugumt-ja-en model_dir={os.environ['TRANSFORMERS_CACHE']}")
    en2ja_model = pipeline("translation", model="staka/fugumt-en-ja")
    ja2en_model = pipeline("translation", model="staka/fugumt-ja-en")

    return v2t_model, en2ja_model, ja2en_model

def status(text, start=0, end=100, now=0):
    #text = "" if text is None or text=="" else f"{text} ( remnant = {now} )"
    text = "" if text is None or text=="" else f"{text}"
    eel.write_status(text, start, end, now)

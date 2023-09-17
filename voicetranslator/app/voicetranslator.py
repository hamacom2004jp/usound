from pathlib import Path
from voicetranslator.app import common
from voicetranslator.app import setting
import datetime
import glob
import eel
import multiprocessing
import queue
import soundcard as sc
import soundfile as sf
import time
import sys


@eel.expose
def load_speaker_list(spname=None):
    speakers = list()
    for sp in sc.all_speakers():
        try:
            if spname is not None and spname==sp.name:
                return sp
            speakers.append(dict(index=sp.id,
                                 name=sp.name,
                                 channels=sp.channels))
        except:
            break
    return speakers

@eel.expose
def get_default_speacker():
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    if 'default_sp' not in setting_data:
        setting_data['default_sp'] = ''
    return setting_data['default_sp']

@eel.expose
def set_default_speacker(spname):
    sp = load_speaker_list(spname)
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    setting_data['default_sp'] = sp.name
    setting.save_setting(common.APP_DATA_DIR, setting_data)

@eel.expose
def load_duration():
    duration = 3
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    if 'duration' in setting_data:
        duration = setting_data['duration']
    return duration

@eel.expose
def set_duration(duration):
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    setting_data['duration'] = duration
    setting.save_setting(common.APP_DATA_DIR, setting_data)

RUN_MAIN = multiprocessing.Queue()
RUN_CAPS = multiprocessing.Queue()
RUN_SEGMENT = multiprocessing.Queue()
RUN_TRANSFORM = multiprocessing.Queue()
@eel.expose
def start(spname, mode_translate, duration):
    eel.loading_mask(True)
    logger_main, _, _, _ = common.load_config()
    common.status(f"Starting capture..", logger=logger_main)
    temp_dir = common.mkdirs(common.APP_DATA_DIR / 'temp')
    for f in glob.glob(str(temp_dir)+"/*.wav"):
        Path(f).unlink(missing_ok=True)
    RUN_CAPS.put(True)
    pr_cap = multiprocessing.Process(target=run_cap, args=(common.APP_DATA_DIR, spname, mode_translate, int(duration), RUN_MAIN, RUN_CAPS, RUN_SEGMENT))
    eel.loading_mask(False)
    pr_cap.start()

@eel.expose
def stop():
    logger_main, _, _, _ = common.load_config()
    common.status(f"Speacker recoding stop.", logger=logger_main)
    try:
        RUN_CAPS.get(block=False)
    except:
        pass

def shutdown(page, sockets):
    stop()
    RUN_MAIN.put(None)
    RUN_SEGMENT.put((None, None))
    RUN_TRANSFORM.put((None, None))
    sys.exit()

def run_main(run_main):
    eel.loading_mask(True)
    while True:
        try:
            eval_str = run_main.get(timeout=1)
            if eval_str is None:
                break
            eval(eval_str)
        except queue.Empty:
            pass
        
def run_cap(app_data_dir, spname, mode_translate, duration, run_main, run_caps, run_segment):
    common.APP_DATA_DIR = app_data_dir
    _, logger_cap, _, _ = common.load_config()
    common.status(f"Start run_cap(spname={spname}, mode_translate={mode_translate}, duration={duration})", run_main=run_main, logger=logger_cap)
    temp_dir = common.mkdirs(app_data_dir / 'temp')
    samplerate = 48000

    common.status(f"Opening Capture. spname={spname}", run_main=run_main, logger=logger_cap)
    with sc.get_microphone(id=spname, include_loopback=True).recorder(samplerate=samplerate) as mic:
        while run_caps.qsize() > 0:
            try:
                common.status(f"Capturing. now={run_segment.qsize()}", run_main=run_main, logger=logger_cap)
                rec = mic.record(numframes=samplerate * duration)
                wav_file = temp_dir / Path(datetime.datetime.now().strftime("%y%m%d%H%M%S")+'.wav')
                sf.write(wav_file, rec, samplerate)
                run_segment.put((mode_translate, wav_file))
            except KeyboardInterrupt as e:
                common.e_msg(e, logger_cap)
                stop()
                break
            except Exception as e:
                common.e_msg(e, logger_cap)
                time.sleep(1)
    common.status(f"Ready.", run_main=run_main, logger=logger_cap)

def run_segments(app_data_dir, run_main, run_segment, run_transform):
    common.APP_DATA_DIR = app_data_dir
    _, _, logger_seg, _ = common.load_config()
    v2t_model = common.load_v2t_model(run_main, logger_seg)
    common.status(f"Start run_segments.", run_main=run_main, logger=logger_seg)
    while True:
        try:
            common.status(f"Ready Sengments.", run_main=run_main, logger=logger_seg)
            mode_translate, wav_file = run_segment.get(timeout=10)
            if mode_translate is None:
                break
            v2t_mode = mode_translate[:2]
            common.status(f"Transcribing. segment={run_segment.qsize()+1}, v2t_mode={v2t_mode}, wav_file={wav_file.name}", run_main=run_main, logger=logger_seg)
            segments, info = v2t_model.transcribe(
                str(wav_file),
                language=v2t_mode,
                vad_filter=True,
                vad_parameters=dict(
                    threshold=0.5,
                    min_speech_duration_ms=250,
                    max_speech_duration_s=float("inf"),
                    min_silence_duration_ms=2000,
                    window_size_samples=1024,
                    speech_pad_ms=400))
            wav_file.unlink(missing_ok=True)
            text = ''.join([segment.text for segment in segments])
            run_transform.put((mode_translate, text))
        except queue.Empty:
            pass
        except KeyboardInterrupt as e:
            common.e_msg(e, logger_seg)
            stop()
            break
        except Exception as e:
            common.e_msg(e, logger_seg)
            time.sleep(1)

def run_translate(app_data_dir, run_main, run_transform):
    common.APP_DATA_DIR = app_data_dir
    _, _, _, logger_trs = common.load_config()
    en2ja_model = common.load_en2ja_model(run_main, logger_trs)
    ja2en_model = common.load_ja2en_model(run_main, logger_trs)
    common.status(f"Start run_translate.", run_main=run_main, logger=logger_trs)
    while True:
        try:
            common.status(f"Ready translate.", run_main=run_main, logger=logger_trs)
            mode_translate, input_text = run_transform.get(timeout=10)
            if mode_translate is None:
                break
            common.status(f"Text input. transform={run_transform.qsize()+1}", run_main=run_main, logger=logger_trs)
            results = None
            if mode_translate=='en2ja':
                results = en2ja_model(input_text)
            elif mode_translate=='ja2en':
                results = ja2en_model(input_text)
            else:
                run_main.put(f'eel.write_intext("{input_text}")')
            if results is not None:
                for r in results:
                    txt = r['translation_text']
                    common.status(f"{txt}", run_main=run_main, logger=logger_trs)
                    run_main.put(f'eel.write_intext("{txt}")')
        except queue.Empty:
            pass
        except KeyboardInterrupt as e:
            common.e_msg(e, logger_trs)
            stop()
            break
        except Exception as e:
            common.e_msg(e, logger_trs)
            time.sleep(1)



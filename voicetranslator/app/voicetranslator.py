from voicetranslator.app import common
from voicetranslator.app import setting
import eel
import io
import queue
import numpy as np
#import sounddevice as sd
import soundcard as sc
import soundfile as sf
import time
import threading
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
    common.logger.info(f"Set default speacker.vlue={spname}")
    sp = load_speaker_list(spname)
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    setting_data['default_sp'] = sp.name
    setting.save_setting(common.APP_DATA_DIR, setting_data)

"""
@eel.expose
def load_microphone_list(micname=None):
    microphones = list()
    for mic in sc.all_microphones():
        try:
            if micname is not None and micname==mic.name:
                return mic
            microphones.append(dict(index=mic.id,
                                 name=mic.name,
                                 channels=mic.channels))
        except:
            break
    return microphones

@eel.expose
def get_default_microphone():
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    if 'default_mic' not in setting_data:
        setting_data['default_mic'] = ''
    return setting_data['default_mic']

@eel.expose
def set_default_microphone(micname):
    common.logger.info(f"Set default microphone.vlue={micname}")
    mic = load_microphone_list(micname)
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    setting_data['default_mic'] = mic.name
    setting.save_setting(common.APP_DATA_DIR, setting_data)
"""

@eel.expose
def load_duration():
    duration = 3
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    if 'duration' in setting_data:
        duration = setting_data['duration']
    return duration

@eel.expose
def set_duration(duration):
    common.logger.info(f"Set duration.vlue={duration}")
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    setting_data['duration'] = duration
    setting.save_setting(common.APP_DATA_DIR, setting_data)

V2T_MODEL = None
EN2JA_MODEL = None
JA2EN_MODEL = None

RUN_CAPS = queue.Queue()
RUN_SEGMENT = queue.Queue()
RUN_TRANSFORM = queue.Queue()
@eel.expose
def start(spname, mode_translate, duration):
    global V2T_MODEL, EN2JA_MODEL, JA2EN_MODEL
    common.status(f"Loading models..")
    if V2T_MODEL is None:
        V2T_MODEL, EN2JA_MODEL, JA2EN_MODEL = common.load_model()
    common.logger.info(f"Speacker recoding start.spname={spname}, mode_translate={mode_translate}, duration={duration}")
    common.status(f"Starting capture..")
    RUN_CAPS.put(True)
    th_cap = threading.Thread(target=run_cap, args=(spname, mode_translate, int(duration), RUN_CAPS, RUN_SEGMENT))
    th_cap.start()
    th_seg = threading.Thread(target=run_segments, args=(RUN_CAPS, mode_translate, RUN_SEGMENT, RUN_TRANSFORM))
    th_seg.start()
    th_seg = threading.Thread(target=run_translate, args=(RUN_CAPS, mode_translate, RUN_TRANSFORM))
    th_seg.start()

@eel.expose
def stop():
    common.logger.info(f"Speacker recoding stop.")
    try:
        RUN_CAPS.get(block=False)
    except:
        pass

@eel.expose
def loaded_model():
    global V2T_MODEL, EN2JA_MODEL, JA2EN_MODEL
    common.status(f"Loading models..")
    if V2T_MODEL is None:
        V2T_MODEL, EN2JA_MODEL, JA2EN_MODEL = common.load_model()
    common.status(f"Ready.")
    return True

def shutdown(page, sockets):
    stop()
    sys.exit()

def run_cap(spname, mode_translate, duration, run_caps, run_segment):
    common.logger.info(f"Start run_cap(spname={spname}, mode_translate={mode_translate}, duration={duration})")
    common.status(f"Loading setting..")
    setting_data = setting.load_setting(common.APP_DATA_DIR)
    wav_file = common.mkdirs(common.APP_DATA_DIR / 'temp') / 'rec.wav'
    #wav_file = io.BytesIO()
    samplerate = 48000

    v2t_mode = mode_translate[:2]
    t2t_mode = mode_translate[-2:]

    while run_caps.qsize() > 0:
        with sc.get_microphone(id=spname, include_loopback=True).recorder(samplerate=samplerate) as mic:
            common.status(f"Recording.", now=run_segment.qsize())
            rec = mic.record(numframes=samplerate * duration)
            common.status(f"Writing.", now=run_segment.qsize())
            sf.write(wav_file, rec, samplerate)
            try:
                common.status(f"Transcribing.", now=run_segment.qsize())
                segments, info = V2T_MODEL.transcribe(
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

                #common.logger.debug(f"language={info.language}, language_probability={info.language_probability}, duration={info.duration}, all_language_probs={info.all_language_probs}, transcription_options={info.transcription_options}, vad_options={info.vad_options}")

                run_segment.put(segments)

            except KeyboardInterrupt as e:
                common.e_msg(e, common.logger)
                stop()
                sys.exit()
            except Exception as e:
                common.e_msg(e, common.logger)
                time.sleep(1)
    common.status(f"Ready.")

def run_segments(run_caps, mode_translate, run_segment, run_transform):
    common.logger.info(f"Start run_segments(mode_translate={mode_translate})")
    while run_caps.qsize() > 0:
        try:
            segments = run_segment.get()
            common.status(f"Text output.", now=run_segment.qsize()+1)
            for segment in segments:
                common.logger.debug(f"run_segments: {segment.text}")
                if mode_translate=='ja' or mode_translate=='en':
                    eel.write_intext(segment.text)
                else:
                    run_transform.put(segment.text)
        except KeyboardInterrupt as e:
            common.e_msg(e, common.logger)
            stop()
            sys.exit()
        except Exception as e:
            common.e_msg(e, common.logger)
            time.sleep(1)

def run_translate(run_caps, mode_translate, run_transform):
    common.logger.info(f"Start run_translate(mode_translate={mode_translate})")
    while run_caps.qsize() > 0:
        try:
            input_text = run_transform.get()
            common.status(f"Text output.", now=run_transform.qsize()+1)
            results = None
            if mode_translate=='en2ja':
                results = EN2JA_MODEL(input_text)
            elif mode_translate=='ja2en':
                results = JA2EN_MODEL(input_text)
            else:
                time.sleep(0.1)
            if results is not None:
                for r in results:
                    common.logger.debug(f"{r['translation_text']}")
                    eel.write_intext(r['translation_text'])
        except KeyboardInterrupt as e:
            common.e_msg(e, common.logger)
            stop()
            sys.exit()
        except Exception as e:
            common.e_msg(e, common.logger)
            time.sleep(1)



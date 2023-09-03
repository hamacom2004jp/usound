from voicetranslator.app import common
from voicetranslator.app import setting
import eel
import numpy as np
#import sounddevice as sd
import soundcard as sc
import soundfile as sf
import threading


print(sc.all_speakers())

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
    setting_data = setting.load_speacker(common.APP_DATA_DIR)
    if 'default' not in setting_data:
        setting_data['default'] = ''
    return setting_data['default']

@eel.expose
def set_default_speacker(spname):
    common.logger.info(f"Set default speacker.vlue={spname}")
    sp = load_speaker_list(spname)
    setting_data = setting.load_speacker(common.APP_DATA_DIR)
    setting_data['default'] = sp.name
    setting.save_speacker(common.APP_DATA_DIR, setting_data)

@eel.expose
def load_duration():
    duration = 3
    setting_data = setting.load_speacker(common.APP_DATA_DIR)
    if 'duration' in setting_data:
        duration = setting_data['duration']
    return duration

@eel.expose
def set_duration(duration):
    common.logger.info(f"Set duration.vlue={duration}")
    setting_data = setting.load_speacker(common.APP_DATA_DIR)
    setting_data['duration'] = duration
    setting.save_speacker(common.APP_DATA_DIR, setting_data)

STATUS = [True]
@eel.expose
def start(spname, duration):
    common.logger.info(f"Speacker recoding start.STATUS={STATUS}.duration={duration}")
    STATUS[0] = True
    th = threading.Thread(target=run, args=(spname, int(duration), STATUS))
    th.start()

@eel.expose
def stop():
    common.logger.info(f"Speacker recoding stop.STATUS={STATUS}")
    STATUS[0] = False

MODEL = None
def run(spname, duration, status):
    global MODEL
    if MODEL is None:
        MODEL = common.load_model()

    setting_data = setting.load_speacker(common.APP_DATA_DIR)

    wav_file = common.mkdirs(common.APP_DATA_DIR / 'temp') / 'rec.wav'
    samplerate = 48000

    while status[0]:
        rec = sc.get_microphone(id=spname, include_loopback=True).record(samplerate=samplerate, numframes=samplerate * duration)
        sf.write(wav_file, rec[:,0], samplerate)
        print(f"save={wav_file}")
        segments, _ = MODEL.transcribe(rec, vad_filter=True,
                                   vad_parameters=dict(
                                       threshold=0.5,
                                       min_speech_duration_ms=250,
                                       max_speech_duration_s=float("inf"),
                                       min_silence_duration_ms=2000,
                                       window_size_samples=1024,
                                       speech_pad_ms=400
                                   ))
        print(segments)
    """
    with sc.get_microphone(id=spname, include_loopback=True).recorder(samplerate=samplerate) as mic:
        common.logger.info(f"Recoder opened. id={spname}")
        while status[0]:
            #rec = mic.record(numframes=samplerate * duration)
            rec = sc.get_microphone(id=spname, include_loopback=True).record(numframes=samplerate * duration)
            sf.write(wav_file, rec[:,0], samplerate)
            print(f"save={wav_file}")
            segments, _ = MODEL.transcribe(rec, vad_filter=True,
                                       vad_parameters=dict(
                                           threshold=0.5,
                                           min_speech_duration_ms=250,
                                           max_speech_duration_s=float("inf"),
                                           min_silence_duration_ms=2000,
                                           window_size_samples=1024,
                                           speech_pad_ms=400
                                       ))
            print(segments)
    """
    """
    while status[0]:
        rec = sd.rec(duration * int(speaker['default_samplerate']), samplerate=int(speaker['default_samplerate']), channels=2, blocking=True)
        #print(rec)
        #with sd.InputStream(channels=2, samplerate=int(speaker['default_samplerate']), device=setting_data['default']) as stream:
        #    rec = stream.read(duration * int(speaker['default_samplerate']))
        #    print(rec)
        sf.write(wav_file, rec, int(speaker['default_samplerate']))
        segments, _ = MODEL.transcribe(wav_file, vad_filter=True,
                                       vad_parameters=dict(
                                           threshold=0.5,
                                           min_speech_duration_ms=250,
                                           max_speech_duration_s=float("inf"),
                                           min_silence_duration_ms=2000,
                                           window_size_samples=1024,
                                           speech_pad_ms=400
                                       ))
        print(segments)
    
    #while status[0]:
    #    with sd.OutputStream(channels=2, dtype=common.COMPUTE_TYPE, callback=process):
    #        sd.sleep(int(duration) * 1000)
    """

#def process(outdata: np.ndarray, frames: int, time, status: sd.CallbackFlags):
#    common.logger.info(f"shape={outdata.shape},outdata={outdata}")
    """
    global MODEL
    segments, _ = MODEL.transcribe(outdata, vad_filter=True,
                                   vad_parameters=dict(
                                       threshold=0.5,
                                       min_speech_duration_ms=250,
                                       max_speech_duration_s=float("inf"),
                                       min_silence_duration_ms=2000,
                                       window_size_samples=1024,
                                       speech_pad_ms=400
                                   ))
    common.logger.info(f"segments={segments}")
    eel.write_intext(segments)
    pass
    """



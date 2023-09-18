# Voice Translator App

PCのスピーカーの音声を翻訳するアプリケーションです。
顔認識モデルのダウンロードのためにインターネットに接続しますが、それ以降はローカルで動作しデータのアップロードなどは行いません。


## 動作確認OS
- `Windows 10 Pro`
- `Windows 11 Pro`

## ビルド方法

### SoundCardのビルド
```
git clone https://github.com/bastibe/SoundCard.git
cd SoundCard
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip setuptools wheel
python setup.py bdist_wheel
deactivate
```
- setup.pyのビルドで以下のエラーが発生する場合は、setup.pyを修正してあげる必要があります。
- エラー：```UnicodeDecodeError: 'cp932' codec can't decode byte 0x97 in position 3341: illegal multibyte sequence```
- 修正前:```long_description=open('README.rst').read(),```
- 修正後:```long_description=open('README.rst', encoding="utf-8").read(),```
- ```dist/SoundCard-0.4.2-py3-none-any.whl```ファイルをvoice-translatorのビルド環境構築にコピーする

### voice-translatorのビルド環境構築
```
git clone https://github.com/hamacom2004jp/voice-translator.git
cd voice-translator
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install SoundCard-0.4.2-py3-none-any.whl
deactivate
```

### pyinstallerのブートローダービルド環境構築
ブートローダーをビルドしないと、peepdetがマルウエア判定されてしまう。
vc++のコンパイラを使うため、下記のツールをインストールする。
⇒管理者権限を持ったPowerShellで実行する必要がある

#### Chocolateryインストール
```
AdminPowerShell > Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
#### vcbuildtoolsインストール
```
AdminPowerShell > choco install -y python vcbuildtools
```

#### pyinstallerのブートローダービルド＆インストール
voice-translatorのビルドフォルダで新しいcmdを開いて実行する
```
cd voice-translator
.venv\Scripts\activate
git clone https://github.com/pyinstaller/pyinstaller
cd pyinstaller\bootloader
python ./waf all
cd ..
pip install wheel
pip install .
deactivate
```

#### voice-translatorのビルド
```
cd voice-translator
.venv\Scripts\activate
powershell wget https://raw.githubusercontent.com/bottlepy/bottle/master/bottle.py -OutFile .venv\Lib\site-packages\bottle.py
python -m eel voicetranslator/__main__.py voicetranslator/app/web -n voicetranslator --onefile -i voicetranslator/v2t.ico -w --clean ^
            --collect-all voicetranslator ^
            --collect-all voicetranslator.app ^
            --collect-all altgraph ^
            --collect-all av ^
            --collect-all bottle ^
            --collect-all bottle-websocket ^
            --collect-all certifi ^
            --collect-all cffi ^
            --collect-all charset-normalizer ^
            --collect-all click ^
            --collect-all colorama ^
            --collect-all coloredlogs ^
            --collect-all ctranslate2 ^
            --collect-all Eel ^
            --collect-all faster-whisper ^
            --collect-all filelock ^
            --collect-all flatbuffers ^
            --collect-all fsspec ^
            --collect-all future ^
            --collect-all gevent ^
            --collect-all gevent-websocket ^
            --collect-all greenlet ^
            --collect-all huggingface-hub ^
            --collect-all humanfriendly ^
            --collect-all idna ^
            --collect-all Jinja2 ^
            --collect-all joblib ^
            --collect-all MarkupSafe ^
            --collect-all mpmath ^
            --collect-all networkx ^
            --collect-all numpy ^
            --collect-all onnxruntime ^
            --collect-all packaging ^
            --collect-all pefile ^
            --collect-all Pillow ^
            --collect-all pip ^
            --collect-all protobuf ^
            --collect-all pycparser ^
            --collect-all pyinstaller ^
            --collect-all pyinstaller-hooks-contrib ^
            --collect-all pyparsing ^
            --collect-all pyreadline3 ^
            --collect-all pywin32-ctypes ^
            --collect-all PyYAML ^
            --collect-all regex ^
            --collect-all requests ^
            --collect-all sacremoses ^
            --collect-all safetensors ^
            --collect-all sentencepiece ^
            --collect-all setuptools ^
            --collect-all six ^
            --collect-all SoundCard ^
            --collect-all soundfile ^
            --collect-all sympy ^
            --collect-all tokenizers ^
            --collect-all torch ^
            --collect-all torchaudio ^
            --collect-all torchvision ^
            --collect-all tqdm ^
            --collect-all transformers ^
            --collect-all typing_extensions ^
            --collect-all urllib3 ^
            --collect-all whichcraft ^
            --collect-all zope.event ^
            --collect-all zope.interface

set VERSION=0.0.1
mkdir dist\licenses
mkdir dist\voicetranslator
copy README.md dist\
copy LICENSE.txt dist\
copy licenses\* dist\licenses\
copy voicetranslator\config.yaml dist\voicetranslator\
copy voicetranslator\logconf.yml dist\voicetranslator\
copy voicetranslator\v2t.ico dist\voicetranslator\
powershell compress-archive -Force dist/* voicetranslator-v%VERSION%.zip
deactivate
```


#### 開発環境でのvoice-translatorの実行方法
```
cd voice-translator
.venv\Scripts\activate
python -m voicetranslator
deactivate
```

#### 実行時データの保存場所
```
pathlib.Path(HOME_DIR) / '.voice-translator'
```


# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details

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
pyinstaller voicetranslator/__main__.py -n voicetranslator --onefile --collect-all voicetranslator -i voicetranslator/v2t.ico -w --clean

mkdir dist\voicetranslator
copy README.md dist\voicetranslator\
copy voicetranslator\config.yaml dist\voicetranslator\
copy voicetranslator\logconf.yml dist\voicetranslator\
copy voicetranslator\v2t.ico dist\voicetranslator\
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

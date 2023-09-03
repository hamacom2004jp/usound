# Voice Translator App

PCのスピーカーの音声を翻訳するアプリケーションです。
顔認識モデルのダウンロードのためにインターネットに接続しますが、それ以降はローカルで動作しデータのアップロードなどは行いません。


## 動作確認OS
- `Windows 10 Pro`
- `Windows 11 Pro`

## ビルド方法

### voice-translatorのビルド環境構築
```
git clone https://github.com/hamacom2004jp/voice-translator.git
cd voice-translator
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 開発環境でのpeepdetの実行方法
```
cd voice-translator
.venv\Scripts\activate
python -m voicetranslator
```


# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details

from voicetranslator.app import app
from pathlib import Path
import argparse
import os


HOME_DIR = os.path.expanduser("~")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Voice Translator App')
    
    parser.add_argument('--data',
                        help='Setting the data directory.',
                        default=Path(os.getenv('VOT_DATA', HOME_DIR)) / ".voice-translator")
    
    args = parser.parse_args()
    
    app.main(str(args.data))

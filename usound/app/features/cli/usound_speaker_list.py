from cmdbox.app import common, feature
from typing import Dict, Any, Tuple, Union, List
import argparse
import datetime
import logging
import soundcard

class SpeakerList(feature.Feature):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "speaker"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'list'

    def get_option(self):
        """
        この機能のオプションを返します

        Returns:
            Dict[str, Any]: オプション
        """
        return dict(
            type="str", default=None, required=False, multi=False, hide=False, use_redis=self.USE_REDIS_FALSE,
            discription_ja="スピーカーのリストを取得します。",
            discription_en="Get a list of speakers.",
            choice=[
                dict(opt="spid", type="str", default=None, required=False, multi=False, hide=False, choice=None,
                     discription_ja="スピーカーIDでフィルタします。",
                     discription_en="Filter by speaker name."),
                dict(opt="spname", type="str", default=None, required=False, multi=False, hide=False, choice=None,
                     discription_ja="スピーカー名でフィルタします。",
                     discription_en="Filter by speaker name."),
                dict(opt="output_json", short="o", type="file", default="", required=False, multi=False, hide=True, choice=None, fileio="out",
                     discription_ja="処理結果jsonの保存先ファイルを指定。",
                     discription_en="Specify the destination file for saving the processing result json."),
                dict(opt="output_json_append", short="a", type="bool", default=False, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="処理結果jsonファイルを追記保存します。",
                     discription_en="Save the processing result json file by appending."),
                dict(opt="stdout_log", type="bool", default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をConsole logに出力します。",
                     discription_en="Available only in GUI mode. Outputs standard output during command execution to Console log."),
                dict(opt="capture_stdout", type="bool", default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をキャプチャーし、実行結果画面に表示します。",
                     discription_en="Available only in GUI mode. Captures standard output during command execution and displays it on the execution result screen."),
                dict(opt="capture_maxsize", type="int", default=self.DEFAULT_CAPTURE_MAXSIZE, required=False, multi=False, hide=True, choice=None,
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力の最大キャプチャーサイズを指定します。",
                     discription_en="Available only in GUI mode. Specifies the maximum capture size of standard output when executing commands."),
            ])

    def apprun(self, logger:logging.Logger, args:argparse.Namespace, tm:float, pf:List[Dict[str, float]]=[]) -> Tuple[int, Dict[str, Any], Any]:
        """
        この機能の実行を行います

        Args:
            logger (logging.Logger): ロガー
            args (argparse.Namespace): 引数
            tm (float): 実行開始時間
            pf (List[Dict[str, float]]): 呼出元のパフォーマンス情報

        Returns:
            Tuple[int, Dict[str, Any], Any]: 終了コード, 結果, オブジェクト
        """
        try:
            speakers = list()
            for s in soundcard.all_speakers():
                sp = dict(id=s.id, name=s.name, channels=s.channels)
                if args.spid is not None or args.spname is not None:
                    if args.spid==s.id:
                        speakers.append(sp)
                        break
                    if args.spname==s.name:
                        speakers.append(sp)
                        break
                    continue
                speakers.append(sp)
            ret = dict(success=dict(data=speakers))
        except Exception as e:
            logger.error(f'{e} speaker={s}', exc_info=True)
            ret = dict(error=f'{e} speaker={s}')
        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, None
        return 0, ret, None

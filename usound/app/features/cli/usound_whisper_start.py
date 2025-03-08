from cmdbox.app import common, client, feature
from cmdbox.app.commons import redis_client
from cmdbox.app.options import Options
from faster_whisper import WhisperModel
from pathlib import Path
from typing import Dict, Any, Tuple, Union, List
import argparse
import logging
import json


class WhisperStart(feature.OneshotNotifyEdgeFeature):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "whisper"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'start'

    def get_option(self):
        """
        この機能のオプションを返します

        Returns:
            Dict[str, Any]: オプション
        """
        return dict(
            use_redis=self.USE_REDIS_TRUE, nouse_webmode=False,
            discription_ja="配備済みモデルを開始します。",
            discription_en="Start deployed model.",
            choice=[
                dict(opt="host", type=Options.T_STR, default=self.default_host, required=True, multi=False, hide=True, choice=None, web="mask",
                     discription_ja="Redisサーバーのサービスホストを指定します。",
                     discription_en="Specify the service host of the Redis server."),
                dict(opt="port", type=Options.T_INT, default=self.default_port, required=True, multi=False, hide=True, choice=None, web="mask",
                     discription_ja="Redisサーバーのサービスポートを指定します。",
                     discription_en="Specify the service port of the Redis server."),
                dict(opt="password", type=Options.T_STR, default=self.default_pass, required=True, multi=False, hide=True, choice=None, web="mask",
                     discription_ja="Redisサーバーのアクセスパスワード(任意)を指定します。省略時は `password` を使用します。",
                     discription_en="Specify the access password of the Redis server (optional). If omitted, `password` is used."),
                dict(opt="svname", type=Options.T_STR, default="server", required=True, multi=False, hide=True, choice=None, web="readonly",
                     discription_ja="サーバーのサービス名を指定します。省略時は `server` を使用します。",
                     discription_en="Specify the service name of the inference server. If omitted, `server` is used."),
                dict(opt="name", type=Options.T_STR, default=None, required=True, multi=False, hide=False, choice=None,
                     discription_ja="AIモデルの登録名を指定します。",
                     discription_en="Specify the registration name of the AI model."),
                dict(opt="retry_count", type=Options.T_INT, default=3, required=False, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーへの再接続回数を指定します。0以下を指定すると永遠に再接続を行います。",
                     discription_en="Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever."),
                dict(opt="retry_interval", type=Options.T_INT, default=5, required=False, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーに再接続までの秒数を指定します。",
                     discription_en="Specifies the number of seconds before reconnecting to the Redis server."),
                dict(opt="timeout", type=Options.T_INT, default="1800", required=False, multi=False, hide=True, choice=None,
                     discription_ja="サーバーの応答が返ってくるまでの最大待ち時間を指定。",
                     discription_en="Specify the maximum waiting time until the server responds."),
                dict(opt="output_json", short="o", type=Options.T_FILE, default=None, required=False, multi=False, hide=True, choice=None, fileio="out",
                     discription_ja="処理結果jsonの保存先ファイルを指定。",
                     discription_en="Specify the destination file for saving the processing result json."),
                dict(opt="output_json_append", short="a", type=Options.T_BOOL, default=False, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="処理結果jsonファイルを追記保存します。",
                     discription_en="Save the processing result json file by appending."),
                dict(opt="stdout_log", type=Options.T_BOOL, default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をConsole logに出力します。",
                     discription_en="Available only in GUI mode. Outputs standard output during command execution to Console log."),
                dict(opt="capture_stdout", type=Options.T_BOOL, default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をキャプチャーし、実行結果画面に表示します。",
                     discription_en="Available only in GUI mode. Captures standard output during command execution and displays it on the execution result screen."),
                dict(opt="capture_maxsize", type=Options.T_INT, default=self.DEFAULT_CAPTURE_MAXSIZE, required=False, multi=False, hide=True, choice=None,
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力の最大キャプチャーサイズを指定します。",
                     discription_en="Available only in GUI mode. Specifies the maximum capture size of standard output when executing commands."),
            ])

    def get_svcmd(self):
        """
        この機能のサーバー側のコマンドを返します

        Returns:
            str: サーバー側のコマンド
        """
        return 'whisper_start'

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
        if args.name is None:
            msg = dict(warn=f"Please specify the --name option.")
            common.print_format(msg, args.format, tm, args.output_json, args.output_json_append, pf=pf)
            return 1, msg, None

        cl = client.Client(logger, redis_host=args.host, redis_port=args.port, redis_password=args.password, svname=args.svname)
        ret = cl.redis_cli.send_cmd(self.get_svcmd(), [args.name],
                                    retry_count=args.retry_count, retry_interval=args.retry_interval, timeout=args.timeout)

        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, None
        return 0, ret, None

    def is_cluster_redirect(self):
        """
        クラスター宛のメッセージの場合、メッセージを転送するかどうかを返します

        Returns:
            bool: メッセージを転送する場合はTrue
        """
        return True

    def svrun(self, data_dir:Path, logger:logging.Logger, redis_cli:redis_client.RedisClient, msg:List[str],
              sessions:Dict[str, Dict[str, Any]]) -> int:
        """
        この機能のサーバー側の実行を行います

        Args:
            data_dir (Path): データディレクトリ
            logger (logging.Logger): ロガー
            redis_cli (redis_client.RedisClient): Redisクライアント
            msg (List[str]): 受信メッセージ
            sessions (Dict[str, Dict[str, Any]]): セッション情報
        
        Returns:
            int: 終了コード
        """
        msg = [None if m=="None" or m=="" else m for m in msg]

        reskey = msg[1]
        name = msg[2]
        if name is None:
            logger.warning(f"name is empty.")
            redis_cli.rpush(reskey, dict(warn=f"name is empty."))
            return self.RESP_WARN

        deploy_dir = data_dir / name

        if name in sessions:
            logger.warning(f"{name} has already started a session.")
            redis_cli.rpush(reskey, dict(warn=f"{name} has already started a session."))
            return self.RESP_WARN
        conf_path = deploy_dir / "conf.json"
        if not conf_path.exists():
            logger.warning(f"Conf path {str(conf_path)} does not exist")
            redis_cli.rpush(reskey, dict(warn=f"Conf path {str(conf_path)} does not exist"))
            return self.RESP_WARN

        try:
            with open(conf_path, "r") as cf:
                conf = json.load(cf)
                model_size = conf["model_size"]
                device = conf["device"]
                device_index = conf["device_index"]
                compute_type = conf["compute_type"]
                cpu_threads = conf["cpu_threads"]
                num_workers = conf["num_workers"]
                model_dir = conf["model_dir"]
                whisper = WhisperModel(model_size, device=device, device_index=device_index, compute_type=compute_type,
                            cpu_threads=cpu_threads, num_workers=num_workers, download_root=model_dir)
                sessions[name] = dict(session=whisper, model_size=model_size, device=device, device_index=device_index, compute_type=compute_type,
                                    cpu_threads=cpu_threads, num_workers=num_workers, model_dir=model_dir)
        except Exception as e:
            logger.warning(f"Failed start of {name} session.: {e}", exc_info=True)
            redis_cli.rpush(reskey, dict(warn=f"Failed start of {name} session.: {e}"))
            return self.RESP_WARN

        logger.info(f"Successful start of {name} session.")
        redis_cli.rpush(reskey, dict(success=f"Successful start of {name} session."))
        return self.RESP_SCCESS

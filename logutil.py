#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""ログ出力ユーティリティ
todo: configフォルダ/configファイルが無い場合にデフォルト値を設定
todo: logフォルダが無い場合に自動作成
todo: 出力ファイル名にタイムスタンプをつける
"""

import copy
from datetime import datetime
import inspect
from logging import getLogger, StreamHandler, Formatter, config
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import os.path


class LogUtil(object):
    u"""ログ出力ユーティリティクラス
    """
    __LOGGER = None

    # デフォルトの出力モード(root, console, file, dual)
    # モードによって出力先が違う
    # ※logging.confのloggersセクションのkeysキーに設定してない
    # モードが指定された場合はroot扱いになる
    _DEFAULT_MODE = 'root'

    # 日付時刻出力パターン
    _TIME_PATTERN = {
        'pattern1': '%Y-%m-%d',
        'pattern2': '%Y-%m-%d_%H%M',
        'pattern3': '%Y-%m-%d_%H%M%S',
        'pattern4': '%Y/%m/%d %H:%M:%S',
        'pattern5': '%Y%m%d%H%M%S'
    }
    # ファイル書き込みオプション
    WRITE_OPTION = {
        'LineSep': True,
        'TimeStamp_in_filename': True,
        'TimePreFix': 'pattern2',
        'TimePreFix_msec': False,
        'OutDirectory': './log/',
        'Extension': '.log'
    }

    def __init__(self, prefix=_DEFAULT_MODE):
        u""" ロガーの初期化
        prefix: 出力モード
        """
        config.fileConfig('./config/logging.conf')
        self.__LOGGER = getLogger(prefix)

    def _call_info(self, f_backcode):
        flp = f_backcode.co_filename
        fnc = f_backcode.co_name
        fnm = os.path.basename(flp)
        d = {"file": fnm, "func": fnc}
        return "[{file} {func}] ".format(**d)

    def _joinstr(self, v1, v2):
        u"""文字列の連結(intの場合は変換)"""
        conv1, conv2 = [v1, v2]
        if isinstance(v1, int):
            conv1 = str(v1)
        if isinstance(v2, int):
            conv2 = str(v2)
        return conv1 + conv2

    def set_log_level(self, level='DEBUG'):
        u"""ログレベルをセット"""
        if level.upper() == 'DEBUG':
            self.__LOGGER.setLevel(DEBUG)
        elif level.upper() == 'INFO':
            self.__LOGGER.setLevel(INFO)
        elif level.upper() == 'WARNING':
            self.__LOGGER.setLevel(WARNING)
        elif level.upper() == 'ERROR':
            self.__LOGGER.setLevel(ERROR)
        elif level.upper() == 'CRITICAL':
            self.__LOGGER.setLevel(CRITICAL)

    def get_write_option(self):
        return copy.deepcopy(self.WRITE_OPTION)

    def debug(self, val):
        # strでない場合は値をそのまま出力
        if isinstance(val, str):
            self.__LOGGER.debug(
                self._joinstr(
                    self._call_info(inspect.currentframe().f_back.f_code),
                    val
                )
            )
        else:
            self.__LOGGER.debug(val)

    def info(self, val):
        if isinstance(val, str):
            self.__LOGGER.info(
                self._joinstr(
                    self._call_info(inspect.currentframe().f_back.f_code),
                    val
                )
            )
        else:
            self.__LOGGER.info(val)

    def warning(self, val):
        if isinstance(val, str):
            self.__LOGGER.warning(
                self._joinstr(
                    self._call_info(inspect.currentframe().f_back.f_code),
                    val
                )
            )
        else:
            self.__LOGGER.warning(val)

    def error(self, val):
        if isinstance(val, str):
            self.__LOGGER.error(
                self._joinstr(
                    self._call_info(inspect.currentframe().f_back.f_code),
                    val
                )
            )
        else:
            self.__LOGGER.error(val)

    def critical(self, val):
        if isinstance(val, str):
            self.__LOGGER.critical(
                self._joinstr(
                    self._call_info(inspect.currentframe().f_back.f_code),
                    val
                )
            )
        else:
            self.__LOGGER.critical(val)

    def debug_nc(self, val):
        u"""呼び出し元のクラス、メソッドを記述せずに出力
        """
        self.__LOGGER.debug(val)

    def info_nc(self, val):
        u"""呼び出し元のクラス、メソッドを記述せずに出力
        """
        self.__LOGGER.info(val)

    def warning_nc(self, val):
        u"""呼び出し元のクラス、メソッドを記述せずに出力
        """
        self.__LOGGER.warning(val)

    def error_nc(self, val):
        u"""呼び出し元のクラス、メソッドを記述せずに出力
        """
        self.__LOGGER.error(val)

    def critical_nc(self, val):
        u"""呼び出し元のクラス、メソッドを記述せずに出力
        """
        self._LOGGER.critical(val)

    def dump(self, val):
        u"""値のみをファイル出力
        debug_ncと同じ
        """
        self.__LOGGER.debug(val)

    def write_file(self, val, filename='', option=None):
        if option is None:
            option = self.WRITE_OPTION

        now = datetime.today()
        prefix = unicode(self._TIME_PATTERN[option['TimePreFix']])
        tm = now.strftime(prefix)
        if option['TimePreFix_msec']:
            tm = tm + '%03d' % (now.microsecond // 1000)

        # 出力先のチェック
        if not os.path.exists(option['OutDirectory']):
            os.makedirs(option['OutDirectory'])

        # ファイル名の指定がなければ、デフォルト
        if filename == '':
            filename = option['DefaultName'] + option['Extension']

        # パスと名前に分離
        path, name = os.path.split(filename)
        # パス指定が無ければデフォルト
        if path == '':
            path = option['OutDirectory']
        # ファイル名と拡張子を分離
        nm, ext = os.path.splitext(name)
        # 拡張子の指定がなければデフォルト
        if ext == '':
            ext = option['Extension']
        # タイムスタンプ有り
        if option['TimeStamp_in_filename']:
            nm = nm + '_' + tm

        name = nm + ext
        filename = os.path.join(path, name)
        with open(filename, 'a') as f:
            if option['LineSep']:
                val = val + '\n'
            f.write(val)


def main():
    u"""Example
    """
    # Output on the Console
    # 2016-09-23 11:08:09,477    DEBUG [logutil.py main] hello debug
    # 2016-09-23 11:08:09,477     INFO [logutil.py main] hello info
    # 2016-09-23 11:08:09,477  WARNING [logutil.py main] hello warning
    # 2016-09-23 11:08:09,477    ERROR [logutil.py main] hello error
    # 2016-09-23 11:08:09,477 CRITICAL [logutil.py main] hello critical
    log = LogUtil()
    log.debug('hello debug')
    log.info('hello info')
    log.warning('hello warning')
    log.error('hello error')
    log.critical('hello critical')

    # Output on the Console Only
    # log = LogUtil('console')

    # Output on the File Only(./log/app.log)
    # log = LogUtil('file')

    # Output on the Console and in the File(./log/app.log)
    # log = LogUtil('dual')

    # log level: debug < info < warning < error < critical
    # default: debug
    # change level: log.set_log_level('error')

if __name__ == "__main__":
    main()

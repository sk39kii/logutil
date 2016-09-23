# logutil
ログ出力ユーティリティ

## 概要
Pythonでログ出力する。

## 使用方法

### インポート

ログ出力したいスクリプトで以下のようにインポートする。

```py
from logutil import LogUtil 
```

### 使い方

#### コンソールに出力する

インスタンス生成時にパラメータをつけない場合はコンソール(標準出力)に出力します。
```py
log = LogUtil()
log.debug('hello debug')
log.info('hello info')
log.warning('hello warning')
log.error('hello error')
log.critical('hello critical')
```

パラメータに'console'としても同様です。
```py
## Output on the Console Only
log = LogUtil('console')
```
#### 出力イメージ

```sh
## Output example
2016-09-23 11:08:09,477    DEBUG [logutil.py main] hello debug
2016-09-23 11:08:09,477     INFO [logutil.py main] hello info
2016-09-23 11:08:09,477  WARNING [logutil.py main] hello warning
2016-09-23 11:08:09,477    ERROR [logutil.py main] hello error
2016-09-23 11:08:09,477 CRITICAL [logutil.py main] hello critical
```

#### ファイルに出力する

パラメータに'file'を渡すとファイルに出力します。  
出力先のファイルは./log/app.logです。
```py
## Output on the File Only(./log/app.log)
log = LogUtil('file')
```

#### コンソールとファイルに出力する
パラメータに'dual'を渡すとコンソールとファイルに出力します。
```py
## Output on the Console and in the File(./log/app.log)
log = LogUtil('dual')
```
#### ログレベルについて

ログレベルの優先順位は以下の通りです。
- log level: debug < info < warning < error < critical

デフォルトは'debug'です。

#### ログレベルを変更する

ログレベルを変更したい場合はインスタンス生成後に以下のようにします。
```py
## change level
log = LogUtil()
log.set_log_level('error')
```

### カスタマイズ

ログレベルやファイルの出力先は、./config/logging.confに記載している。  

#### ファイルの出力先を変えたい場合

- [handler_fileHandler]のargsを変更

#### 出力形式を変えたい場合

- [formatter_logFormatter]のformatを変更

## 課題・検討

- todo: configフォルダ/configファイルが無い場合にデフォルト値を設定
- todo: logフォルダが無い場合に自動作成
- todo: 出力ファイル名にタイムスタンプをつける

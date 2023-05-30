# Component-Test

組込みモジュールそれぞれのテストをするためのディレクトリです．

## 組み込み部品リスト
|部品名|型番号|
|----|----|
|温湿度気圧センサ|[LPS25HB](https://akizukidenshi.com/catalog/g/gK-13460/)|
|9軸センサ|[BNO055](https://akizukidenshi.com/catalog/g/gK-16996/)|
|GNSSモジュール|[現行版](https://akizukidenshi.com/catalog/g/gK-13849/)|
|通信モジュール|[RM-92A](https://www.green-house.co.jp/products/rm-92as/)|

# ファイル説明
|ファイル名|説明|
|----|----|
|lps25hb_data.py|温湿度気圧センサlps25hbからそれぞれの情報を取得するためのプログラム|
|bno055_data.py|9軸センサbno055からそれぞれの軸のデータを取得するためのプログラム|
|maxb_data.py|GNSSモジュールから3次元座標と時刻を取得するためのプログラム|

# 関連ライブラリ
|ライブラリ名|説明|
|LPS25HB.py|LPS25HB動作用のライブラリ|
|adafruit_bno055.py|adafruit社製BNO055動作用ライブラリ|
|......|......|

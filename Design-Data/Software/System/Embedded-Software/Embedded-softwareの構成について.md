# Embedded-software
走行で実際に使用するプログラムとそれらのModuleをまとめるディレクトリです。
このディレクトリ上でmain.pyを実行すると、統合された組み込みプログラムが実行され、
打ち上げ開始からの一連の動作が始まります。

## ディレクトリ/ファイルの説明
|ディレクトリ/ファイル名|説明|
|----|-----|
|Modules|各種クラスを定義したプログラムをまとめたディレクトリ|
|main.py|mainとして実行するプログラム|


## 注意
- sleeptime.txtの数値を確認する。
    - この数値が-1だと、すぐに落下判定のフェーズに入る。実行からsleepする時間はこの数値を変更することで設定できる。
    - 数値はmain.pyの実行ごとに変更されていくため、毎回チェックする必要がある。
- 今後追加します。
# 説明
RM92Aは地上局に機体情報をダウンリンクさせるために用いる無線モジュールです．
本プログラムでは機体側にRaspberry Pi Pico，地上局側にNUCLEO-F303K8を使用しています．

# セッティング
RM92Aは使用前にセッティングが必要になります．
## セッティング方法
地上局にRM92Aを乗せた状態で*setting_rm92a.NUCLEO_F303K8.bin*ファイルを書き込んでください．
pcにつないぎTeraTermを開いた状態でトグルスイッチを押したらセッティング画面へ移行できます．（TeraTermのbaurateは115200に変更してください）
## セッティングの内容
セッティングする内容については，RM92Aの販売元であるGreenHouseの[pdf](https://www.green-house.co.jp/book/iot-wireless/SimpleMACstd92A-92C_instruction%20manual-rev2.9.15.pdf)をご参照ください．

基本的なセッティングでは
|コマンド|指定する値（機体側）|指定する値（地上局側）|
|----|----|----|
|a|24|24|
|c|0|1|
|d|65535|0|
|e|0|1|
|i|0|0|
|t|0|0|

上のように書き込みが終わったらxで変更内容を保存してください．

# 使い方
## 機体側
**機体側**はpythonファイルを2つ書き込んでください．
*FUSiON_RM92A.py*は自作ライブラリになってます．
*RM92A_TEST.py*が実際に動かしてもらうプログラムです．

## 地上局側
**地上局側**はmbedのオンライン開発環境となります．[公式ページ](https://os.mbed.com/)にアクセスし，アカウント登録してください．
その後以下のように3つのファイル全てを記述し，ビルドしてください．

### ビルドのやり方
上のリンクからアカウント作成，ログインしたのち，以下のようにFile>New>Mbed Progectと進みます．
![](setting_images/"mbed_1.png")

そうすると以下のような画面が出てくるため，**Example Projectをmbed2-example-blinky**に設定して新規プロジェクトを作成します．
![](setting_images/"mbed_2.png")

次に以下のようにActive Projectの確認とBuild targetの設定を行います．
![](setting_images/"mbed_4.png")

設定が行えたらプロジェクトを右クリックし，新規ファイルを追加します．
ここに*main.cpp*，*FUSiON_RM92A.h*，*FUSiON_RM92A.cpp*を作成（コピペ）してください．
![](setting_images/"mbed_5.png")

記述が完了したらビルドを完了してください．
![](setting_images/"mbed_6.png")
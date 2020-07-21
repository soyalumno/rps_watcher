# RPS_WATCHER

楽天市場の在庫を監視するためのスクリプトです。

## Requirement

- Python3 or more
    - beautifulsoup4 4.9.1
    - requests 2.24.0
    - schedule 0.6.0

- 楽天APIのアプリケーションID

## Installation

```bash
$ git clone https://github.com/soyalumno/rps_watcher.git
$ cd rps_watcher
```

## Usage

1. `watch_list.csv`に在庫を監視したい商品のURLを記入

![](https://user-images.githubusercontent.com/33917383/88071714-280edf00-cbaf-11ea-9698-d01ce4be44bd.png)

2. 楽天APIのアプリケーションIDを取得して、ソースコードに記入

[楽天API](https://webservice.rakuten.co.jp/document/)

![](https://user-images.githubusercontent.com/33917383/88071726-2b09cf80-cbaf-11ea-966a-1097fd5c68bd.png)

```python
# 楽天APIのアプリケーションID
CREDENTIAL = {
  'app_id' : 'アプリケーションIDを入力',
}
```

3. スケジューラを起動

```bash
$ python cron.py
```

10分毎に指定された商品ページをスクレイピング＋`watch_list.csv`をアップデート

![](https://user-images.githubusercontent.com/33917383/88071740-2f35ed00-cbaf-11ea-8576-2260608f68b8.png)

|パラメータ |概要|
|---      |---|
|url      |商品ページURL|
|itemcode |商品コード|
|jancode  |JANコード|
|itemname |商品名|
|itemprice|商品価格|
|shopname |ショップ名|
|shopcode |ショップコード|
|avail    |在庫有無(0...売切／1...在庫有り)|

4. `command+c`(windowsの場合、`ctrl+c`)でスケジューラが終了


## Note

**通知機能について**

通知機能は未実装ですが、   
在庫復活時は以下の関数がコールされます。

```python
def Notificate(row):
  logger.log(10, f"{os.getpid()} : Restocked! ¥{row['itemprice']}_{row['itemname']}_{row['url']}")
```

本関数のカスタマイズにより、在庫復活を通知することが可能です  
(LINE,Gmail等)

**スクレイピングについて**

本プログラムはWebサーバへのアクセスを伴います  
過度な頻度でのプログラムの実行は、サーバの負荷上昇に繋がるため  
ご自身の責任において実行するようお願い致します。  
(デフォルトのままであれば、自然アクセスの範囲で動作します)

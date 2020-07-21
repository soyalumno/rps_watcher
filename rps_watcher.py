#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs4
import time
import os
import csv
import re
import copy
from logger import gene_logger

# 監視対象ファイルのパス
LIST_PATH = './'
LIST_FILE = 'watch_list.csv'

# 楽天APIのアプリケーションID
CREDENTIAL = {
  'app_id' : 'アプリケーションIDを入力',
}

# ロガー
logger = None

# HTTP_GETの実行
def req_GET(url, params={}):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
  }
  print(f"GET...{url}")
  return requests.get(url, headers=headers, params=params)

# APIの実行
def searchByItemcode(code):
  params = {
      'applicationId': CREDENTIAL['app_id'],
      'itemCode': code,
      'availability': 0,
      'formatVersion': 2,
  }
  r = req_GET('https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?params', params=params)
  # APIの制限を考慮してwait
  time.sleep(1.0)
  return r.json()

# 商品ページからitemcodeを取得
def getItemCode(url):
  # html取得
  soup = bs4(req_GET(url).content, 'lxml')
  s = soup.prettify()
  time.sleep(0.5)

  # itemcodeの検索
  jan = ic = ''
  rslt = re.search(r'.*itemid.*[^a-z\-0-9]([a-z\-0-9]+):([0-9]+).*\n', s, re.IGNORECASE)
  if rslt:
    ic = f'{rslt.group(1)}:{rslt.group(2)}'

  # jancodeの検索
  tag = soup.select_one('#ratRanCode')
  if tag:
    jan = tag.get('value')
  return ic, jan

# 入力されたデータベースを最新の状態に更新
def updateDB(db):
  # itemcodeが空の行にitemcodeをセット
  for row in db:
    if (row['itemcode'] is None or len(row['itemcode']) is 0):
      row['itemcode'], row['jancode'] = getItemCode(row['url'])

    # itemcodeをキーにAPI経由で各種情報を取得
    res = searchByItemcode(row['itemcode'])
    if res.get('Items'):
      item = res['Items'][0]
      row['shopname'] = item['shopName']
      row['shopcode'] = item['shopCode']
      row['itemname'] = item['itemName']
      row['itemprice'] = item['itemPrice']
      row['avail'] = str(item['availability'])
  return db

# 通知処理
# ダミー処理...自由な方法で通知してください(mailとかLINEがオススメ)
def Notificate(row):
  logger.log(10, f"{os.getpid()} : Restocked! ¥{row['itemprice']}_{row['itemname']}_{row['url']}")

# データベースの比較
def cmpDB(before, after):
  restocks = []
  for b, a in zip(before, after):
    # 在庫0 -> 1に変化した商品をセット
    if b['avail'] == '0' and a['avail'] == '1':
      restocks.append(b)
  return restocks

# 監視リストファイルの読み込み
def readWatchList():
  # データベースをOrderDictの配列形式に変換
  db = []
  with open(os.path.join(LIST_PATH, LIST_FILE), encoding='utf-8') as f:
    db = [row for row in csv.DictReader(f)]
  return db

def writeWatchList(db):
  # アップデート後データベースの書き込み
  with open(os.path.join(LIST_PATH, LIST_FILE), 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    # ヘッダ行＋データベース本体の書き込み
    writer.writerow(list(db[0].keys()))
    writer.writerows([list(row.values()) for row in db])

def main():
  global logger
  # ロガーの生成
  logger = gene_logger('log/rps_watcher.log')
  logger.log(10, f'{os.getpid()} : On main.')

  # 監視リストの読み込み
  db = readWatchList()

  # 比較用に更新前のリストを保持
  _db = copy.deepcopy(db)

  # データベースのアップデート
  updateDB(db)

  # データベースの比較 → リストックされたアイテム一覧を取得
  for row in cmpDB(_db, db):
    Notificate(row)

  # 監視リストの書き込み
  writeWatchList(db)

# 本処理
if __name__ == '__main__':
  main()

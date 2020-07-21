#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import subprocess
from schedule import Scheduler
from logger import gene_logger

# ロガー
logger = None
procs = []

# 指定されたコマンドの実行
def proc(args, sche):
  global procs
  try:
    p = subprocess.Popen(args, stdout=sys.stdout, stderr=subprocess.STDOUT)
    procs.append(p)
    logger.log(10, f'{os.getpid()} : proc(#{p.pid})...{" ".join(args)}')
    logger.log(10, f'Next : {sche.next_run}')
  except Exception as e:
    logger.log(10, e.args)

# スケジューラの開始処理
def main():
  global procs
  global logger
  # ロガーの生成
  logger = gene_logger('log/cron.log')
  logger.log(10, f'{os.getpid()} : On main.')

  # スケジュールのセット
  s = Scheduler()
  s.every(10).minutes.do(proc, args=['python', './rps_watcher.py'], sche=s)

  # セットされたジョブを出力
  for j in s.jobs:
    logger.log(10, f'{os.getpid()} : Jobs...{j}')

  # ジョブの実行待ちループ
  while True:
    s.run_pending()
    # プロセスの実行状態をチェック
    for p in procs:
      if p.poll() is not None:
        logger.log(10, f'{os.getpid()} : #{p.pid} has exited({p.returncode})')
        procs.remove(p)
    time.sleep(1)

  logger.log(10, f'{os.getpid()} : On exit.')

if __name__ == '__main__':
  main()

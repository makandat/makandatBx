#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
# -*- coding: utf-8 -*-
# slideview.cgi フォルダ内画像のスライド表示  2019-05-19 画像幅のバグフィックス
#   MySQL を利用
import WebPage as page
import FileSystem as fs
from MySQL import MySQL
import Text
import Common
import sys, os
#from syslog import syslog

## ページクラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    #Common.init_logger('C:/temp/Logger.log')
    self.adjust = '0'
    if self.isParam('folder') :
      # Postback のとき
      folder = self.getParam('folder')
      slide = self.getParam('slide')
      if self.isParam('width') :
        # 画像幅調整あり
        if self.isCookie('adjust_width') :
          self.adjust = self.getCookie('adjust_width')
          if self.adjust == '1' :
            # 反転させる。
            self.adjust = '0'
          else :
            self.adjust = '1'
        else :
          self.adjust = '1'
        self.setCookie('adjust_width', self.adjust)
      else :
        # 画像調整指定なし(width=なし)
        self.adjust = self.getCookie('adjust_width')
      parts = folder.split('/')
      n = len(parts) - 1
      self.setPlaceHolder('title', parts[n])
      self.setPlaceHolder('folder', folder)
    else :
      # Postback でない
      self.setPlaceHolder('folder', '')
      self.setPlaceHolder('message', '')
      self.setPlaceHolder('title', 'スライド表示')
      self.setPlaceHolder('filename', '')
      self.setCookie('adjust_width', '0')
    self.showPicture(folder, slide)
    return


  # id から path を得る。
  def getPath(self, id) :
    path = self.__mysql.getValue(f"SELECT `path` FROM Pictures WHERE id={id}")
    return path


  # 画像を表示する。
  def showPicture(self, folder, slide) :
    current = int(self.getCookie('current_image', '0'))
    files = os.listdir(folder.encode('utf8'))
    n = len(files)
    m = n - 1
    files2 = sorted(files)
    if slide == "first" :
      current = 0
      self.setPlaceHolder('message', "最初の画像です。No.0")
    elif slide == "prev" :
      current = (current - 1) if current > 0 else 0
      if current == 0 :
        self.setPlaceHolder('message', '最初の画像です。No.0')
      else :
        self.setPlaceHolder('message', f"No.{current} / {m}の画像です。")
    elif slide == "next" :
      current = (current + 1) if current < (n - 1) else (n - 1)
      if current == n - 1 :
        self.setPlaceHolder('message', f"最後の画像です。No.{current}")
      else :
        self.setPlaceHolder('message', f"No.{current} / {m} の画像です。")
    elif slide == "last" :
      current = n - 1
      self.setPlaceHolder('message', f"最後の画像です。No.{current}")
    elif slide == 'current' :
      self.setPlaceHolder('message', f"No.{current} / {m}の画像です。")
    else :
      # CURRENT
      current = int(slide)
      self.setPlaceHolder('message', f"No.{current} / {m} の画像です。")
    filename = files2[current].decode('utf8')
    filePath = folder + "/" + filename
    self.setPlaceHolder('filename', '')
    self.setPlaceHolder('filename', filePath)
    self.setCookie('current_image', str(current))
    if self.adjust == '1' :
      self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={filePath}\" style=\"padding:10px;width:100%;\" />")
    else :
      self.setPlaceHolder('picture', f"<img src=\"getImage.cgi?path={filePath}\" style=\"padding:10px;\" />")
    self.setPlaceHolder('path', filePath)
    return

  # 画像ファイルなら True を返す。
  @staticmethod
  def isPicture(path) :
    ext = Text.tolower(fs.getExtension(path))
    return (ext == '.jpg' or ext == '.png' or ext == '.gif')



# メイン開始位置
wp = MainPage('templates/slideview.html')
wp.echo()

#!/usr/bin/env python3
# WIKI showContent.cgi  v1.00 2019-10-27
from WebPage import WebPage
from MySQL import MySQL
from DateTime import DateTime
import Text
import Common


SELECT = "SELECT id, title, author, date, content, info, type, revision FROM Wiki WHERE id={0}"

# ページクラス
class ShowPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    Common.init_logger("/home/user/log/showContent.log")
    if self.isParam("id") :
      id = self.getParam("id")
      rows = self.__mysql.query(SELECT.format(id))
      if len(rows) == 0 :
        self.embed({"title":"Unknown", "message":"エラー： id が正しくありません。", "prop":"", "content":""})
        return
      row = rows[0]
      data = {"title":row[1], "author": "" if row[2] == None else row[2], "date": str(row[3]), "content":row[4], "info":row[5], "type":row[6], "revision":row[7]}
      doctype = row[6]
      if doctype.lower() == "text" :
        self.showAsText(id, data)
      elif doctype.lower() == "html" :
        self.showAsHTML(id, data)
      else :
        self.showAsMarkup(id, data)
    else :
      self.embed({"title":"Unknown", "message":"エラー： id が指定されていません。", "prop":"", "content":""})
    return
    
  # 内容を平文として表示する。
  def showAsText(self, id, data) :
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span> revision=" + data["revision"] + " date=" + data["date"] + " doctype=" + data["type"]
    content = WebPage.escape(data["content"]).replace("\\n", "\n")
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    return
    
  # 内容をHTMLとして表示する。
  def showAsHTML(self, id, data) :
    content = data["content"].replace("\\n", "\n")
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span>, revision=" + data["revision"] + ", date=" + data["date"] + ", doctype=" + data["type"]
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    return

  # 内容をMarkupとして表示する。
  def showAsMarkup(self, id, data) :
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span>, revision=" + data["revision"] + ", date=" + data["date"] + ", doctype=" + data["type"]
    content = ShowPage.markup(WebPage.escape(data["content"]))
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    return
  
  # マークアップ言語を HTML にする。
  @staticmethod
  def markup(data) :
    html = ""
    lines = data.split("\n")
    ulmode = False
    for line in lines :
      if ulmode and line.startswith("- ") == False :
        line = "</ul>" + line
        ulmode = False
      if line.startswith("#### ") :
        line = WebPage.tag("h4", Text.substring(line, 5), "class='default'")
      elif line.startswith("### ") :
        line = WebPage.tag("h3", Text.substring(line, 4), "class='default'")
      elif line.startswith("## ") :
        line = WebPage.tag("h2", Text.substring(line, 3), "class='default'")
      elif line.startswith("# ") :
        line = WebPage.tag("h1", Text.substring(line, 2), "class='default'")
      elif line.startswith("&gt; ") :
        line = WebPage.tag("blockquote", "> " + Text.substring(line, 5), "class='default' style='color:brown;'")
      elif line.startswith("- ") :
        if ulmode :
          line = WebPage.tag("li", Text.substring(line, 2), "class='default'")
        else :
          ulmode = True
          line = "<ul>" + WebPage.tag("li", Text.substring(line, 2), "class='default'")          
      elif Text.re_contain("^.*\!\[.+\]\(.+\).*$", line) :
        sstr1 = Text.split("![", line)
        sstr2 = Text.split("]", sstr1[1])
        str1 = sstr2[0]
        shref1 = Text.split("(", line)
        shref2 = Text.split(")", shref1[1])
        href = shref2[0]
        line = f"{sstr1[0]}<img src='{href}' alt='{str1}' />{shref2[1]}"        
      elif Text.re_contain("^.*\[.+\]\(.+\).*$", line) :
        sstr1 = Text.split("[", line)
        sstr2 = Text.split("]", sstr1[1])
        str1 = sstr2[0]
        shref1 = Text.split("(", line)
        shref2 = Text.split(")", shref1[1])
        href = shref2[0]
        line = f"{sstr1[0]}<a href='{href}'>{str1}</a>{shref2[1]}"
      else :
        pass
      if Text.re_contain("^.*\*\*.+\*\*.*$", line) :
        line = line.replace("**", "<b>", 1)
        line = line.replace("**", "</b>", 1)
      elif Text.re_contain("^.*\*.+\*.*$", line) :
        line = line.replace("*", "<i>", 1)
        line = line.replace("*", "</i>", 1)
      elif Text.re_contain("^.*~~.+~~.*$", line) :
        line = line.replace("*", "<strike>", 1)
        line = line.replace("*", "</strike>", 1)
      else :
        pass
      html += line
    return html
    
# 応答を返す。
page = ShowPage('templates/showContent.html')
page.echo()

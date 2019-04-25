#/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
#!/usr/bin/python3
# -*- code=utf-8 -*-
import WebPage as page
import MySQL
import Common
#from syslog import syslog

SELECT = f"SELECT DISTINCT creator FROM Pictures "

# CGI WebPage クラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("C:/temp/PyLogger.log")
    self.__mysql = MySQL.MySQL()
    if self.isParam('filter') :
      self.setPlaceHolder('word', self.getParam('filter'))
      self.filter()
    else :
      self.all()
      self.setPlaceHolder('word', '---')
    self.setPlaceHolder("message", "クエリー OK")
    return

  # 条件に合う作者を列挙
  def filter(self) :
    filt = self.getParam('filter')
    where = f"WHERE creator LIKE '%{filt}%' OR `path` LIKE '%{filt}%' OR info LIKE '%{filt}%' OR mark='{filt}'"
    sql = "SELECT creator, count(creator) as count, sum(count) as refer, sum(fav) as favor FROM Pictures " + where + "  GROUP BY creator ORDER BY creator"
    rows = self.__mysql.query(sql)
    list = self.makelist(rows)
    self.setPlaceHolder('list', list)
    return

  # すべての作者を列挙
  def all(self) :
    sql = "SELECT creator, count(creator) as count, sum(count) as refer, sum(fav) as favor FROM Pictures GROUP BY creator ORDER BY creator"
    rows = self.__mysql.query(sql)
    list = self.makelist(rows)
    self.setPlaceHolder('list', list)
    return

  # 作者一覧を作成
  def makelist(self, rows) :
    list = "<tr><th>作者名</th><th>出現総数</th><th>参照総数</th><th>お好み総数</th></tr>\n"
    for row in rows :
      creator = row[0]
      count = str(row[1])
      refer = str(row[2])
      favor = str(row[3])
      anchor = "<a href=\"index.cgi?creator=" + creator + "\">" + creator + "</a>"
      table_row = f"<tr><td>{anchor}</td><td>{count}</td><td>{refer}</td><td>{favor}</rd></tr>\n"
      list += table_row
    return list

# メイン開始位置
wp = MainPage('templates/creators.html')
wp.echo()
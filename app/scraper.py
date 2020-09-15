from bs4 import BeautifulSoup
import urllib.request as req
from googletrans import Translator


def url2list(url):
    # urlopen()でデータを取得
    res = req.urlopen(url)

    # BeautifulSoupにhtmlオブジェクト 渡す
    soup = BeautifulSoup(res, 'html.parser')

    # タイトル抽出
    h1 = soup.find("h1", class_="title mathjax")
    h1.find("span", {"class":"descriptor"}).extract()#h1内に含まれるtitle:を削除
    title_en = h1.get_text(strip=True)

    # アブスト抽出
    blqu = soup.find("blockquote", class_="abstract mathjax")
    blqu.find("span", {"class":"descriptor"}).extract()#h1内に含まれるtitle:を削除
    abst_en = blqu.get_text(strip=True)
    abst_en = ' '.join(abst_en.splitlines())

    # アブストを文章ごとに分ける
    abst_en_ls = abst_en.split(".")
    abst_en_ls.remove('')

    # 翻訳
    translator = Translator()
    title_jp = translator.translate(title_en, dest="ja").text
    abst_jp_ls =[]
    for abst_en_each in abst_en_ls:
        transed = translator.translate(abst_en_each, dest="ja").text
        abst_jp_ls.append(transed)
    
    return title_en, abst_en_ls, title_jp, abst_jp_ls


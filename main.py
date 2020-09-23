"""日本の有名人の誕生日を列挙するスクリプト"""

import sys
import os
import re
import calendar
from datetime import datetime
from urllib import request
from urllib import parse
from pathlib import Path

import bs4

import birthday

def fetch_html(url:str) -> bs4.BeautifulSoup:
    '''htmlをダウンロードしてbs4インスタンスをつくる'''
    # open
    response = request.urlopen(url)
    soup = bs4.BeautifulSoup(response, features='html.parser')

    return soup


def fetch_html_file(htmlfilepath:str) -> bs4.BeautifulSoup:
    '''htmlファイルからbs4インスタンスをつくる'''
    htmlfile = open(htmlfilepath, mode='r', encoding='utf_8')

    soup = bs4.BeautifulSoup(htmlfile, features='html.parser')

    htmlfile.close()

    return soup


def find_birthday_list( soup: bs4.BeautifulSoup ) -> list:
    '''誕生日リストのul要素を探してリストにして返す
    （ドキュメントによっては、複数のulに分かれているのでリスト。）
    '''
    elms = soup.select('#誕生日')

    if elms is None:
        print("birthday is not found")
        return None

    title_span = elms[0]
    h2elm = title_span.parent

    lis = []
    sibling = h2elm
    while sibling is not None:
        sibling = sibling.next_sibling

        if sibling.name == "ul":
            lis.append( sibling )
        elif sibling.name == "h2": # 次の章(h2)がきたら終了
            break

    if lis == []:
        print ("<ul> is not found.")
        return None
    # else:
    #     print(sibling)

    return lis


def extract_birthdays(ultag: bs4.element.Tag) -> list:
    '''ulタグ内のliから誕生日リストを全て取ってリストで返す'''
    ret = []
    li_elms = ultag.select("li")
    for litag in li_elms:
        brtdy: birthday.Birthday = birthday.parse_birthday(litag.get_text())
        if brtdy is None:
            continue

        yearstr = brtdy.yearstr if brtdy.year == birthday.YEAR_UNKNOWN else str(brtdy.year)

        print( yearstr + ": " + brtdy.name + "    (" + brtdy.occupation + ")" )

        ret.append(brtdy)

    return ret

def parse_commandline( args:list ) -> (int, int):
    '''コマンドライン解析'''
    if args is not None and len(args) >= 1:
        matchobj = re.match(r'(-?\d+)/(-?\d+)', args[0])
        if matchobj is None:
            print("Error: mm/dd 形式で指定してください: -> " + args[0])
            return None, None

        mgrp = matchobj.group(1)
        dgrp = matchobj.group(2)
        month = int(mgrp)
        day = int(dgrp)

        if month < 1 or month > 12:
            print("Error: '月' の値が不正です -> " + mgrp)
            return None, None

        max_day = calendar.monthrange( 2020, month )[1]

        if day < 1 or day > max_day:
            print("Error: '日' の値が不正です -> " + dgrp)
            return None, None

        return month, day
    else:
        now = datetime.now()
        month = now.month
        day = now.day
        return month, day

def save_html( soup:bs4.BeautifulSoup, month:int, day:int ):
    '''ダウンロードしたwebページを保存する'''
    # mkdir htmlsrc
    outfullpath = os.path.dirname(os.path.abspath(__file__))
    outfullpath = os.path.join( outfullpath, "htmlsrc" )

    Path(outfullpath).mkdir(parents=True, exist_ok=True)

    # save
    outfullpath = os.path.join( outfullpath, f"src_{month}_{day}.html" )
    with open(outfullpath, "w", encoding="utf_8") as file:
        file.write( str(soup) )


def main_process(args:list) -> (int):
    '''主処理'''
    month, day = parse_commandline( args )
    if month is None or day is None:
        return 1

    daystr = f"{month}月{day}日"

    daystrenc = parse.quote( daystr )
    url = f"https://ja.wikipedia.org/wiki/{daystrenc}"

    print( f"{daystr} 誕生日の有名人" )

    soup: bs4.BeautifulSoup = fetch_html(url)
    # soup: bs4.BeautifulSoup = fetch_html_file('example.html')

    # save html
    save_html(soup, month, day)

    # find
    birthday_ullist = find_birthday_list(soup)

    for ultag in birthday_ullist:
        extract_birthdays( ultag )

    return 0

# main program
if __name__ == '__main__':
    retcode = main_process(sys.argv[1:])
    sys.exit(retcode)

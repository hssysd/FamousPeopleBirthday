# coding:utf-8

from urllib import request
from urllib import parse
import sys
import os
import re
import bs4
import calendar
from datetime import datetime

from pathlib import Path


import birthday

def fetchHtml(url:str) -> bs4.BeautifulSoup:

    # open
    response = request.urlopen(url)
    soup = bs4.BeautifulSoup(response, features='html.parser')

    return soup


def fetchHtmlFromFile(htmlFile:str) -> bs4.BeautifulSoup:
    example_file = open(htmlFile, mode='r', encoding='utf_8')

    example_soup = bs4.BeautifulSoup(example_file, features='html.parser')

    return example_soup


def findBirthdayList( bs: bs4.BeautifulSoup ) -> bs4.element.Tag:
    elms = bs.select('#誕生日')

    if elms is None:
        print("birthday is not found")
        return None

    titleSpan = elms[0]
    h2elm = titleSpan.parent

    lis = []
    sibling = h2elm
    while sibling is not None:
        sibling = sibling.next_sibling

        if sibling.name == "ul":
            lis.append( sibling )
        elif sibling.name == "h2":
            break

    if lis == []:
        print ("<ul> is not found.")
        return None
    # else:
    #     print(sibling)

    return lis


def extractBirthDays(ul: bs4.element.Tag) -> list:

    ret = []

    lis = ul.select("li")
    for li in lis:
        b: Birthday = birthday.parseBirthday(li.get_text())
        if b is None:
            continue

        yearstr = b.yearstr if b.year == birthday.YEAR_UNKNOWN else str(b.year)

        print( yearstr + ": " + b.name + "    (" + b.occupation + ")" )

        ret.append(b)

    return ret

def parse_commandline( args:list ) -> (int, int):
    
    if args is not None and len(args) >= 1:
        matchobj = re.match(r'(-?\d+)/(-?\d+)', args[0])
        if matchobj is None:
            print("Error: mm/dd 形式で指定してください: -> " + args[0])
            return None, None

        m = matchobj.group(1)
        d = matchobj.group(2)
        month = int(m)
        day = int(d)

        if month < 1 or month > 12:
            print("Error: '月' の値が不正です -> " + m)
            return None, None
        
        maxDay = calendar.monthrange( 2020, month )[1]
        
        if day < 1 or day > maxDay:
            print("Error: '日' の値が不正です -> " + d)
            return None, None

        return month, day
    else:
        now = datetime.now()
        month = now.month
        day = now.day
        return month, day

def saveHtml( soup:bs4.BeautifulSoup, month:int, day:int ):
    # mkdir htmlsrc
    outfullpath = os.path.dirname(os.path.abspath(__file__))
    outfullpath = os.path.join( outfullpath, "htmlsrc" )

    Path(outfullpath).mkdir(parents=True, exist_ok=True)

    # save
    outfullpath = os.path.join( outfullpath, f"src_{month}_{day}.html" )
    with open(outfullpath, "w") as file:
        file.write( str(soup) )


def main_process(args:list) -> (int):
    '''主処理
    '''
    month, day = parse_commandline( args )
    if month is None or day is None:
        return 1

    daystr = f"{month}月{day}日"

    daystrenc = parse.quote( daystr )
    url = f"https://ja.wikipedia.org/wiki/{daystrenc}"

    print( f"{daystr} 誕生日の有名人" )

    bs: bs4.BeautifulSoup = fetchHtml(url)
    # bs: bs4.BeautifulSoup = fetchHtmlFromFile('example.html')

    # save html
    saveHtml(bs, month, day)

    # find
    birthdayUlList = findBirthdayList(bs)

    for ul in birthdayUlList:
        extractBirthDays( ul )
    
    return 0

# main program
if __name__ == '__main__':
    ret = main_process(sys.argv[1:])
    exit(ret)
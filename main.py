# coding:utf-8

from trello import TrelloApi


from urllib import request
from urllib import parse
import webbrowser
import requests
import re
import bs4
from datetime import datetime

YEAR_UNKNOWN: int = -1

def fetchHtml(url:str) -> bs4.BeautifulSoup:
    response = request.urlopen(url)

    example_soup = bs4.BeautifulSoup(response, features='html.parser')

    return example_soup


def fetchHtmlFromFile(htmlFile:str) -> bs4.BeautifulSoup:
    example_file = open(htmlFile, mode='r', encoding='utf_8')

    example_soup = bs4.BeautifulSoup(example_file, features='html.parser')

    return example_soup


class Birthday:
    year: int = 0
    yearstr: str = ""
    name: str = ""
    occupation: str = ""

def parseBirthday(text:str) -> Birthday:

    ret = Birthday()

    spl = text.split('-')
    if spl is None or len(spl) < 2:
        print("birthday parse error:" + text)
        return None

    # year
    ret.yearstr = spl[0].strip()

    matches = re.findall( r'(\d+?)年', ret.yearstr )
    if len(matches) > 0:
        m = matches[0]
        ret.year = int(m)
    else:
        ret.year = YEAR_UNKNOWN

    # name, occupation
    namespl = spl[1].split("、")
    if namespl is None or len(namespl) < 2:
        ret.name = spl[1]
    else:
        ret.name = namespl[0].strip()
        ret.occupation = namespl[1].strip()
        ret.occupation = re.sub( r'[\t\n]', '', ret.occupation)

    return ret

def findBirthdayList( bs: bs4.BeautifulSoup ) -> bs4.element.Tag:
    elms = bs.select('#誕生日')

    if elms is None:
        print("birthday is not found")
        return None

    titleSpan = elms[0]
    h2elm = titleSpan.parent

    sibling = h2elm
    while sibling is not None:
        sibling = sibling.next_sibling

        if sibling.name == "ul":
            break

    if sibling is None:
        print ("<ul> is not found.")
        return None
    # else:
    #     print(sibling)

    return sibling


def extractBirthDays(ul: bs4.element.Tag):

    ret = []

    lis = ul.select("li")
    for li in lis:
        b: Birthday = parseBirthday(li.get_text())
        if b is None:
            continue

        yearstr = b.yearstr if b.year == YEAR_UNKNOWN else str(b.year)

        print( yearstr + ": " + b.name + "(" + b.occupation + ")" )

        ret.append(b)

    return ret

# main program

now = datetime.now()
month = now.month
day = now.day

daystr = f"{month}月{day}日"

daystrenc = parse.quote( daystr )
url = f"https://ja.wikipedia.org/wiki/{daystrenc}"

print( f"{daystr} 誕生日の有名人" )

bs: bs4.BeautifulSoup = fetchHtml(url)
# bs: bs4.BeautifulSoup = fetchHtmlFromFile('example.html')

birthdayUl = findBirthdayList(bs)

birthdays = extractBirthDays( birthdayUl )

print("done.")

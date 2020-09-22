# coding:utf-8
import re

YEAR_UNKNOWN: int = -1

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

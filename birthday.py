"""誕生日情報クラス"""

import re

YEAR_UNKNOWN: int = -1

class Birthday:
    """誕生日情報"""

    year: int = 0
    yearstr: str = ""
    name: str = ""
    occupation: str = ""

def parse_birthday(text:str) -> Birthday:
    """引数で指定されたテキスト（li要素の中身）から誕生年や名前などを分離して
    Birthdayオブジェクトにして返す
    """
    ret = Birthday()

    spl = text.split('-')
    if spl is None or len(spl) < 2:
        print("birthday parse error:" + text)
        return None

    # year
    ret.yearstr = spl[0].strip()

    matches = re.findall( r'(\d+?)年', ret.yearstr )
    if len(matches) > 0:
        ret.year = int(matches[0])
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

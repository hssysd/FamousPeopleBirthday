# coding:utf-8

import time
import calendar

import unittest
import main

class TestMain(unittest.TestCase):
    # TODO: 範囲外の月/日を入力された時のテスト
    def test_invalidMonthAndDays(self):
        '''無効な月日を入力された時のテスト'''
        
        # month, day, expected return value
        testInputs = [
            [ 0, 0, 1 ],
            [ 1, 1, 0 ],
            [ 2, 30, 1],
            [ -1, 1, 1],
            [ 1, -1, 1],
            [ 13, 1, 1],
        ]
        
        for ti in testInputs:
            md = f'{ti[0]}/{ti[1]}'
            print( f'======== {md} ========' )
            ret = main.main_process( [md] )
            self.assertEqual( ret, ti[2], f"[test_monthAndDays]Failed Assertion: with {md}" )
        
    
    def test_allDays(self):
        '''全ての月日を入力して正しく取得できるかどうかテスト'''
        for month in range( 1, 12+1 ):
            mr = calendar.monthrange( 2020, month ) # 2020年は閏年
            # print( f'======== {year}/{month}: {mr[1]} ========' )
            for day in range( 1, mr[1]+1 ):
                md = f'{month}/{day}'
                print( f'======== {md} ========' )
                ret = main.main_process( [ md ] )
                self.assertEqual( ret, 0, f"[test_allDays]Failed Assertion: with {md}" )
                
                time.sleep(2.0)
        
# main
if __name__ == '__main__':
    unittest.main(verbosity=2)
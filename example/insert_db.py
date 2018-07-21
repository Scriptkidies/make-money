import time
import pandas as pd
import sqlite3
from datetime import datetime

def receiveRealData( code, realType, realData):
    """
    실시간 데이터 수신 이벤트

    실시간 데이터를 수신할 때 마다 호출되며,
    setRealReg() 메서드로 등록한 실시간 데이터도 이 이벤트 메서드에 전달됩니다.
    getCommRealData() 메서드를 이용해서 실시간 데이터를 얻을 수 있습니다.

    :param code: string - 종목코드
    :param realType: string - 실시간 타입(KOA의 실시간 목록 참조)
    :param realData: string - 실시간 데이터 전문
    """

    try:
        #print("receiveRealData:({})".format(realType))
        #self.log.debug("[receiveRealData]")
        #self.log.debug("({})".format(realType))

        if realType not in RealType.REALTYPE:
            return

        if code != "":
            codeOrNot = code
        else:
            codeOrNot = realType

        for fid in sorted(RealType.REALTYPE[realType].keys()):
            value = 10
            ohlcv[RealType.REALTYPE[realType][fid]].append(value)

            #print("fid:%d, value:%s" % (fid, value))
            #data.append(value)
        ohlcv['날짜'].append(str(datetime.today()))
        print(ohlcv)

        #df.to_sql(code, con, if_exists='append')

        #print(data)
        #self.log.debug(data)

    except Exception as e:
        print(e)
        #self.log.error('{}'.format(e))


class RealType(object):

    REALTYPE = {
        '주식시세': {
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            27: '최우선매도호가',
            28: '최우선매수호가',
            13: '누적거래량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비',
            29: '거래대금증감',
            30: '거일거래량대비',
            31: '거래회전율',
            32: '거래비용',
            311: '시가총액(억)'
        },

        '주식체결': {
            20: '체결시간(HHMMSS)',
            10: '체결가',
            11: '전일대비',
            12: '등락율',
            27: '최우선매도호가',
            28: '최우선매수호가',
            15: '체결량',
            13: '누적체결량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비(계약,주)',
            29: '거래대금증감',
            30: '전일거래량대비(비율)',
            31: '거래회전율',
            32: '거래비용',
            228: '체결강도',
            311: '시가총액(억)',
            290: '장구분',
            691: 'KO접근도'
        },

        '주식호가잔량': {
            21: '호가시간',
            41: '매도호가1',
            61: '매도호가수량1',
            81: '매도호가직전대비1',
            51: '매수호가1',
            71: '매수호가수량1',
            91: '매수호가직전대비1',
            42: '매도호가2',
            62: '매도호가수량2',
            82: '매도호가직전대비2',
            52: '매수호가2',
            72: '매수호가수량2',
            92: '매수호가직전대비2',
            43: '매도호가3',
            63: '매도호가수량3',
            83: '매도호가직전대비3',
            53: '매수호가3',
            73: '매수호가수량3',
            93: '매수호가직전대비3',
            44: '매도호가4',
            64: '매도호가수량4',
            84: '매도호가직전대비4',
            54: '매수호가4',
            74: '매수호가수량4',
            94: '매수호가직전대비4',
            45: '매도호가5',
            65: '매도호가수량5',
            85: '매도호가직전대비5',
            55: '매수호가5',
            75: '매수호가수량5',
            95: '매수호가직전대비5',
            46: '매도호가6',
            66: '매도호가수량6',
            86: '매도호가직전대비6',
            56: '매수호가6',
            76: '매수호가수량6',
            96: '매수호가직전대비6',
            47: '매도호가7',
            67: '매도호가수량7',
            87: '매도호가직전대비7',
            57: '매수호가7',
            77: '매수호가수량7',
            97: '매수호가직전대비7',
            48: '매도호가8',
            68: '매도호가수량8',
            88: '매도호가직전대비8',
            58: '매수호가8',
            78: '매수호가수량8',
            98: '매수호가직전대비8',
            49: '매도호가9',
            69: '매도호가수량9',
            89: '매도호가직전대비9',
            59: '매수호가9',
            79: '매수호가수량9',
            99: '매수호가직전대비9',
            50: '매도호가10',
            70: '매도호가수량10',
            90: '매도호가직전대비10',
            60: '매수호가10',
            80: '매수호가수량10',
            100: '매수호가직전대비10',
            121: '매도호가총잔량',
            122: '매도호가총잔량직전대비',
            125: '매수호가총잔량',
            126: '매수호가총잔량직전대비',
            23: '예상체결가',
            24: '예상체결수량',
            128: '순매수잔량(총매수잔량-총매도잔량)',
            129: '매수비율',
            138: '순매도잔량(총매도잔량-총매수잔량)',
            139: '매도비율',
            200: '예상체결가전일종가대비',
            201: '예상체결가전일종가대비등락율',
            238: '예상체결가전일종가대비기호',
            291: '예상체결가',
            292: '예상체결량',
            293: '예상체결가전일대비기호',
            294: '예상체결가전일대비',
            295: '예상체결가전일대비등락율',
            13: '누적거래량',
            299: '전일거래량대비예상체결률',
            215: '장운영구분'
        },

        '장시작시간': {
            215: '장운영구분(0:장시작전, 2:장종료전, 3:장시작, 4,8:장종료, 9:장마감)',
            20: '시간(HHMMSS)',
            214: '장시작예상잔여시간'
        },

        '업종지수': {
            20: '체결시간',
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            15: '거래량',
            13: '누적거래량',
            14: '누적거래대금',
            16: '시가',
            17: '고가',
            18: '저가',
            25: '전일대비기호',
            26: '전일거래량대비(계약,주)'
        },

        '업종등락': {
            20: '체결시간',
            252: '상승종목수',
            251: '상한종목수',
            253: '보합종목수',
            255: '하락종목수',
            254: '하한종목수',
            13: '누적거래량',
            14: '누적거래대금',
            10: '현재가',
            11: '전일대비',
            12: '등락율',
            256: '거래형성종목수',
            257: '거래형성비율',
            25: '전일대비기호'
        },

        '주문체결': {
            9201: '계좌번호',
            9203: '주문번호',
            9205: '관리자사번',
            9001: '종목코드',
            912: '주문분류(jj:주식주문)',
            913: '주문상태(10:원주문, 11:정정주문, 12:취소주문, 20:주문확인, 21:정정확인, 22:취소확인, 90,92:주문거부)',
            302: '종목명',
            900: '주문수량',
            901: '주문가격',
            902: '미체결수량',
            903: '체결누계금액',
            904: '원주문번호',
            905: '주문구분(+:현금매수, -:현금매도)',
            906: '매매구분(보통, 시장가등)',
            907: '매도수구분(1:매도, 2:매수)',
            908: '체결시간(HHMMSS)',
            909: '체결번호',
            910: '체결가',
            911: '체결량',
            10: '체결가',
            27: '최우선매도호가',
            28: '최우선매수호가',
            914: '단위체결가',
            915: '단위체결량',
            938: '당일매매수수료',
            939: '당일매매세금'
        },

        '잔고': {
            9201: '계좌번호',
            9001: '종목코드',
            302: '종목명',
            10: '현재가',
            930: '보유수량',
            931: '매입단가',
            932: '총매입가',
            933: '주문가능수량',
            945: '당일순매수량',
            946: '매도매수구분',
            950: '당일총매도손익',
            951: '예수금',
            27: '최우선매도호가',
            28: '최우선매수호가',
            307: '기준가',
            8019: '손익율'
        },

        '주식시간외호가': {
            21: '호가시간(HHMMSS)',
            131: '시간외매도호가총잔량',
            132: '시간외매도호가총잔량직전대비',
            135: '시간외매수호가총잔량',
            136: '시간외매수호가총잔량직전대비'
        }
    }





if __name__ == "__main__":


    realType = '주식체결'
    #print(RealType.REALTYPE[realType][10])
    realData = 'test'

    #ohlcv = {'종목코드': [], '현재가': [], '전일대비': [], '등락율': [], '누적거래량': []}

    ohlcv = {'날짜': [], '체결시간(HHMMSS)': [],
             '체결가': [], '전일대비': [], '등락율': [], '최우선매도호가': [], '최우선매수호가': [],
            '체결량': [], '누적체결량': [], '누적거래대금': [], '시가': [], '고가': [], '저가': [],
            '전일대비기호': [], '전일거래량대비(계약,주)': [], '거래대금증감': [], '전일거래량대비(비율)': [],
            '거래회전율': [], '거래비용': [], '체결강도': [], '시가총액(억)': [], '장구분': [], 'KO접근도': []}

    receiveRealData('214271', realType, realData)

    receiveRealData('214272', realType, realData)



    df = pd.DataFrame(ohlcv, columns=[
        '날짜', '체결시간(HHMMSS)', '체결가', '전일대비', '등락율', '최우선매도호가', '최우선매수호가', '체결량',
        '누적체결량', '누적거래대금', '시가', '고가', '저가', '전일대비기호', '전일거래량대비(계약,주)',
        '거래대금증감', '전일거래량대비(비율)', '거래회전율', '거래비용', '체결강도', '시가총액(억)', '장구분', 'KO접근도'])

    database = "c:/kiwoom_db/market_123.db"
    code = '000660'

    con = sqlite3.connect(database)
    df.to_sql(code, con, if_exists='append')


             #'누적거래대금': [], '거래량': [], '시가': [], '고가': [], '저가': [],
             #'체결시간': [], '전일대비': [], '전일거래량': [], '(최우선)매도호가': [], '(최우선)매수호가': [],
             #'거래대금증감': [], '전일거래량대비(비율)': [], '거래회전율': [], '거래비용': [], '체결강도': [],
             #'장구분': [], '시가총액': [], 'KO접근도': []}
'''
    ohlcv = {'종목코드': [], '현재가': [], '전일대비': [], '등락율': [], '누적거래량': []}


    realType = '주식체결'

    for fid in sorted(RealType.REALTYPE[realType].keys()):
        ohlcv['종목코드'].append('214271')
        ohlcv['현재가'].append(int('-2370'))
        ohlcv['전일대비'].append(int('-25'))
        ohlcv['등락율'].append(float('-1.04'))
        ohlcv['누적거래량'].append(int('125455'))

        #value = self.getCommRealData(codeOrNot, fid)
        # print("fid:%d, value:%s" % (fid, value))
        #data.append(value)
        #print(fid)

    del ohlcv['종목코드'][:]
    del ohlcv['현재가'][:]
    del ohlcv['전일대비'][:]
    del ohlcv['등락율'][:]
    del ohlcv['누적거래량'][:]



    df = pd.DataFrame(ohlcv, columns=['종목코드', '현재가', '전일대비', '등락율', '누적거래량'])

    database = "c:/kiwoom_db/market_123.db"
    code = '000660'

    con = sqlite3.connect(database)
    df.to_sql(code, con, if_exists='append')


    for fid in sorted(RealType.REALTYPE[realType].keys()):
        #value = self.getCommRealData(codeOrNot, fid)
        # print("fid:%d, value:%s" % (fid, value))
        #data.append(value)
        print(fid)




    #ohlcv['종목코드'].append('214270')
    #ohlcv['현재가'].append(int('-2370'))
    #ohlcv['전일대비'].append(int('-25'))
    #ohlcv['등락율'].append(float('-1.04'))
    #ohlcv['누적거래량'].append(int('125455'))


    #df = pd.DataFrame(ohlcv, columns=['종목코드', '현재가', '전일대비', '등락율', '누적거래량'])

    #print(df.head())

    #database = "c:/kiwoom_db/market_123.db"
    #code = '000660'

    #con = sqlite3.connect(database)
    #df.to_sql(code, con, if_exists='append')

    #data = [' 86100', ' 0', '0.00', '862', '74', '+1', '-0', '-0', '-0', '081823', '3', '-2106185', ' 86100', '-86000', '-181540085200', '-0.04', '0.00', '286', '40.39', '1', '626810', '0']

    #conn = create_connection(database)
    #with conn:
    #    project = ('projects', 'Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    #    project_id = create_project(conn, project)

    #con = sqlite3.connect("c:/kiwoom_db/market_test.db")
    #df.to_sql('039490', con, if_exists='replace')
    #df.to_sql('214270', con, if_exists='append')

    #['000660', ' 86100', ' 0', '0.00', '862', '74', '+1', '-0', '-0', '-0', '081823', '3', '-2106185', ' 86100', '-86000', '-181540085200', '-0.04', '0.00', '286', '40.39', '1', '626810', '0']

'''


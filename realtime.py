import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        # 메시지
        self.msg = ""

        self.createKiwoomInstance()
        self.setSignalSlots()

    def createKiwoomInstance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def setSignalSlots(self):
        self.OnEventConnect.connect(self.eventConnect)

        #self.OnReceiveTrData.connect(self.receiveTrData)
        self.OnReceiveRealData.connect(self.receiveRealData)

    def commConnect(self):
        self.dynamicCall("CommConnect()")
        self.loginLoop = QEventLoop()
        self.loginLoop.exec_()

    def getConnectState(self):
        """
        현재 접속상태를 반환합니다.

        반환되는 접속상태는 아래와 같습니다.
        0: 미연결, 1: 연결

        :return: int
        """
        state = self.dynamicCall("GetConnectState()")
        return state

    def eventConnect(self, returnCode):
        """
        통신 연결 상태 변경시 이벤트

        returnCode가 0이면 로그인 성공
        그 외에는 ReturnCode 클래스 참조.

        :param returnCode: int
        """

        try:
            if returnCode == ReturnCode.OP_ERR_NONE:

                self.server = self.GetServerGubun()

                if len(self.server) == 0 or self.server != "1":
                    #self.msg += "실서버 연결 성공" + "\r\n\r\n"
                    print("실서버 연결 성공" + "\r\n\r\n")

                else:
                    #self.msg += "모의투자서버 연결 성공" + "\r\n\r\n"
                    print("모의투자서버 연결 성공" + "\r\n\r\n")

            else:
                #self.msg += "연결 끊김: 원인 - " + ReturnCode.CAUSE[returnCode] + "\r\n\r\n"
                print("연결 끊김: 원인 - " + ReturnCode.CAUSE[returnCode] + "\r\n\r\n")

        except Exception as error:
            print (error)

        finally:
            # commConnect() 메서드에 의해 생성된 루프를 종료시킨다.
            # 로그인 후, 통신이 끊길 경우를 대비해서 예외처리함.
            try:
                self.loginLoop.exit()
            except AttributeError:
                pass

    def receiveRealData(self, code, realType, realData):
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
            print("receiveRealData")
            #self.log.debug("[receiveRealData]")
            #self.log.debug("({})".format(realType))

            if realType not in RealType.REALTYPE:
                return

            data = []

            if code != "":
                data.append(code)
                codeOrNot = code
            else:
                codeOrNot = realType

            for fid in sorted(RealType.REALTYPE[realType].keys()):
                value = self.getCommRealData(codeOrNot, fid)
                print(value)
                data.append(value)

            print(data)
            #self.log.debug(data)

        except Exception as e:
            print(e)
            #self.log.error('{}'.format(e))

    def getCommRealData(self, code, fid):
        """
        실시간 데이터 획득 메서드

        이 메서드는 반드시 receiveRealData() 이벤트 메서드가 호출될 때, 그 안에서 사용해야 합니다.

        :param code: string - 종목코드
        :param fid: - 실시간 타입에 포함된 fid
        :return: string - fid에 해당하는 데이터
        """
        if not (isinstance(code, str)
                and isinstance(fid, int)):
            raise ParameterTypeError()

        value = self.dynamicCall("GetCommRealData(QString, int)", code, fid)

        return value

    def setRealReg(self, screenNo, codes, fids, realRegType):
        """
        실시간 데이터 요청 메서드

        종목코드와 fid 리스트를 이용해서 실시간 데이터를 요청하는 메서드입니다.
        한번에 등록 가능한 종목과 fid 갯수는 100종목, 100개의 fid 입니다.
        실시간등록타입을 0으로 설정하면, 첫 실시간 데이터 요청을 의미하며
        실시간등록타입을 1로 설정하면, 추가등록을 의미합니다.

        실시간 데이터는 실시간 타입 단위로 receiveRealData() 이벤트로 전달되기 때문에,
        이 메서드에서 지정하지 않은 fid 일지라도, 실시간 타입에 포함되어 있다면, 데이터 수신이 가능하다.

        :param screenNo: string
        :param codes: string - 종목코드 리스트(종목코드;종목코드;...)
        :param fids: string - fid 리스트(fid;fid;...)
        :param realRegType: string - 실시간등록타입(0: 첫 등록, 1: 추가 등록)
        """

        print("setRealReg")
        if not self.getConnectState():
            raise KiwoomConnectError()

        if not (isinstance(screenNo, str)
                and isinstance(codes, str)
                and isinstance(fids, str)
                and isinstance(realRegType, str)):
            raise ParameterTypeError()

        self.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                         screenNo, codes, fids, realRegType)

    def GetServerGubun(self):
        """
        서버구분 정보를 반환한다.
        리턴값이 "1"이면 모의투자 서버이고, 그 외에는 실서버(빈 문자열포함).

        :return: string
        """

        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "" )
        return ret


class ParameterTypeError(Exception):
    """ 파라미터 타입이 일치하지 않을 경우 발생하는 예외 """

    def __init__(self, msg="파라미터 타입이 일치하지 않습니다."):
        self.msg = msg

    def __str__(self):
        return self.msg

class KiwoomConnectError(Exception):
    """ 키움서버에 로그인 상태가 아닐 경우 발생하는 예외 """

    def __init__(self, msg="로그인 여부를 확인하십시오"):
        self.msg = msg

    def __str__(self):
        return self.msg


class ReturnCode(object):
    """ 키움 OpenApi+ 함수들이 반환하는 값 """

    OP_ERR_NONE = 0 # 정상처리
    OP_ERR_FAIL = -10   # 실패
    OP_ERR_LOGIN = -100 # 사용자정보교환실패
    OP_ERR_CONNECT = -101   # 서버접속실패
    OP_ERR_VERSION = -102   # 버전처리실패
    OP_ERR_FIREWALL = -103  # 개인방화벽실패
    OP_ERR_MEMORY = -104    # 메모리보호실패
    OP_ERR_INPUT = -105 # 함수입력값오류
    OP_ERR_SOCKET_CLOSED = -106 # 통신연결종료
    OP_ERR_SISE_OVERFLOW = -200 # 시세조회과부하
    OP_ERR_RQ_STRUCT_FAIL = -201    # 전문작성초기화실패
    OP_ERR_RQ_STRING_FAIL = -202    # 전문작성입력값오류
    OP_ERR_NO_DATA = -203   # 데이터없음
    OP_ERR_OVER_MAX_DATA = -204 # 조회가능한종목수초과
    OP_ERR_DATA_RCV_FAIL = -205 # 데이터수신실패
    OP_ERR_OVER_MAX_FID = -206  # 조회가능한FID수초과
    OP_ERR_REAL_CANCEL = -207   # 실시간해제오류
    OP_ERR_ORD_WRONG_INPUT = -300   # 입력값오류
    OP_ERR_ORD_WRONG_ACCTNO = -301  # 계좌비밀번호없음
    OP_ERR_OTHER_ACC_USE = -302 # 타인계좌사용오류
    OP_ERR_MIS_2BILL_EXC = -303 # 주문가격이20억원을초과
    OP_ERR_MIS_5BILL_EXC = -304 # 주문가격이50억원을초과
    OP_ERR_MIS_1PER_EXC = -305  # 주문수량이총발행주수의1%초과오류
    OP_ERR_MIS_3PER_EXC = -306  # 주문수량이총발행주수의3%초과오류
    OP_ERR_SEND_FAIL = -307 # 주문전송실패
    OP_ERR_ORD_OVERFLOW = -308  # 주문전송과부하
    OP_ERR_MIS_300CNT_EXC = -309    # 주문수량300계약초과
    OP_ERR_MIS_500CNT_EXC = -310    # 주문수량500계약초과
    OP_ERR_ORD_WRONG_ACCTINFO = -340    # 계좌정보없음
    OP_ERR_ORD_SYMCODE_EMPTY = -500 # 종목코드없음

    CAUSE = {
        0: '정상처리',
        -10: '실패',
        -100: '사용자정보교환실패',
        -102: '버전처리실패',
        -103: '개인방화벽실패',
        -104: '메모리보호실패',
        -105: '함수입력값오류',
        -106: '통신연결종료',
        -200: '시세조회과부하',
        -201: '전문작성초기화실패',
        -202: '전문작성입력값오류',
        -203: '데이터없음',
        -204: '조회가능한종목수초과',
        -205: '데이터수신실패',
        -206: '조회가능한FID수초과',
        -207: '실시간해제오류',
        -300: '입력값오류',
        -301: '계좌비밀번호없음',
        -302: '타인계좌사용오류',
        -303: '주문가격이20억원을초과',
        -304: '주문가격이50억원을초과',
        -305: '주문수량이총발행주수의1%초과오류',
        -306: '주문수량이총발행주수의3%초과오류',
        -307: '주문전송실패',
        -308: '주문전송과부하',
        -309: '주문수량300계약초과',
        -310: '주문수량500계약초과',
        -340: '계좌정보없음',
        -500: '종목코드없음'
    }

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
            26: '전일거래량대비',
            29: '거래대금증감',
            30: '전일거래량대비',
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

    app = QApplication(sys.argv)

    try:
        kiwoom = Kiwoom()
        kiwoom.commConnect()

        server = kiwoom.GetServerGubun()

        if len(server) == 0 or server != "1":
            print("실서버 입니다.")
        else:
            print("모의투자 서버입니다.")

        kiwoom.setRealReg("6001", "214270", "20:228", "0")

    except Exception as e:
        print(e)

    sys.exit(app.exec_())
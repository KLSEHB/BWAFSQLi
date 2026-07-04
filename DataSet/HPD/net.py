#!/export/apps/anaconda3/bin/python3
# coding=utf-8
import requests
import re
import json
import sys

class Main():
    def __init__(self):
        self.services = {
            '鏍″洯缃?: '%e6%a0%a1%e5%9b%ad%e7%bd%91',
            '涓浗绉诲姩': '%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8',
            '涓浗鑱旈€?: '%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a',
            '涓浗鐢典俊': '%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1',
            '0': '%e6%a0%a1%e5%9b%ad%e7%bd%91',
            '1': '%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8',
            '2': '%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a',
            '3': '%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1'
        }
        self.url = 'http://auth.ysu.edu.cn/eportal/InterFace.do?method='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        }
        self.isLogined = None
        self.alldata = None

    def tst_net(self):
        res = requests.get('http://10.11.0.1', headers=self.header)
        if res.url.find('success.jsp')>0:
            self.isLogined = True
        else:
            self.isLogined = False
        return self.isLogined

    def isCode(self):
        pass
        return False

    def login(self,user,pwd,type,code=''):
        if self.isLogined == None:
            self.tst_net()
        if self.isLogined == False:
            if user == '' or pwd == '':
                return (False,'鐢ㄦ埛鍚嶆垨瀵嗙爜涓虹┖')
            self.data = {
                'userId': user,
                'password': pwd,
                'service': self.services[type],
                'operatorPwd': '',
                'operatorUserId': '',
                'validcode': code,
                'passwordEncrypt':'False'
            }
            res = requests.get('http://10.11.0.1', headers=self.header)
            queryString = re.findall(r"href='.*?\?(.*?)'", res.content.decode('utf-8'), re.S)
            self.data['queryString'] = queryString[0]

            res = requests.post(self.url + 'login', headers=self.header, data=self.data)
            login_json = json.loads(res.content.decode('utf-8'))
            self.userindex = login_json['userIndex']
            #self.info = login_json
            self.info = login_json['message']
            if login_json['result'] == 'success':
                return (True,'璁よ瘉鎴愬姛')
            else:
                return (False,self.info)
        return (True,'宸茬粡鍦ㄧ嚎')

    def get_alldata(self):
        res = requests.get('http://10.11.0.1/eportal/InterFace.do?method=getOnlineUserInfo')
        try:
            self.alldata = json.loads(res.content.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print('鏁版嵁瑙ｆ瀽澶辫触锛岃绋嶅悗閲嶈瘯銆?)
        return self.alldata

    def logout(self):
        if self.alldata==None:
            self.get_alldata()

        res = requests.post(self.url + 'logout', headers=self.header, data={'userIndex': self.alldata['userIndex']})
        logout_json = json.loads(res.content.decode('utf-8'))
        #self.info = logout_json
        self.info = logout_json['message']
        if logout_json['result'] == 'success':
            return (True,'涓嬬嚎鎴愬姛')
        else:
            return (False,self.info)

    def get_info(self):
        if self.isLogined == None:
            self.tst_net()
        if self.isLogined == False:
            return (False, "鏈璇?)
        if self.alldata==None:
            self.get_alldata()
        try:
            info_json = self.alldata
            tmp = ''
            for i,v in enumerate(info_json['userName']):
                if i!=0:
                    tmp += v
                else:
                    tmp += '*'
            info = "濮撳悕: " + tmp + '\n'
            tmp = ''
            for i, v in enumerate(str(info_json['userId'])):
                if i>4:
                    tmp += v
                else:
                    tmp += '*'
            info += "ID鍗″彿: " + tmp + '\n'
            if info_json['service'] == info_json['realServiceName']:
                info += "鏈嶅姟: " + info_json['service'] + '\n'
            else:
                info += "鏈嶅姟: " + info_json['service'] + ' 鎴?' + info_json['realServiceName'] + '\n'
            info += "鐢ㄦ埛缁? " + info_json['userGroup'] + '\n'
            try:
                stream = float(json.loads(info_json['ballInfo'])[1]['value'])
            except Exception:
                pass
            else:
                base = 'B'
                if(stream > 1024):
                    stream /= 1024
                    base = 'KB'
                if(stream > 1024):
                    stream /= 1024
                    base = 'MB'
                if (stream > 1024):
                    stream /= 1024
                    base = 'GB'

                info += "鍓╀綑娴侀噺: " + str(stream) + ' ' + base + '\n'


            return (True, info)
        except Exception:
            return (False, "璇风◢鍚庡啀璇?)

if __name__ == '__main__':
    loger = Main()
    l = len(sys.argv)
    name = sys.argv[0]
    if l==2:
        if sys.argv[1]=='logout':
            state,info = loger.logout()
        elif sys.argv[1]=='info':
            state, info = loger.get_info()
    elif l==3:
        state, info = loger.login(user=sys.argv[1], pwd=sys.argv[2], type='鏍″洯缃?)
    elif l==4:
        state, info = loger.login(user=sys.argv[1], pwd=sys.argv[2], type=sys.argv[3])
    else:
        print('鏍煎紡锛?)
        print('鐧诲叆锛?s userid password [service_type=鏍″洯缃慮 ' % name)
        print('\t濡傦細%s userid password ' % name)
        print('\t濡傦細%s userid password 涓浗绉诲姩' % name)
        print('娉ㄩ攢锛?s logout ' % name)
        print('鏌ョ湅淇℃伅锛?s info ' % name)
        sys.exit(0)
    if state:
        print (info)
    else:
        print ('鍑虹幇閿欒!')
        print (info)
    sys.exit(0)

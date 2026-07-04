import requests


class GrayBoxClient:
    def __init__(self, base_url, thresh):
        self.thresh = thresh
        self.base_url = base_url

    def _post_request(self, payload):
        resp = requests.post(url=self.base_url, data={'payload': payload})
        return resp.json()

    def get_score(self, payload):
        response = self._post_request(payload)
        score = response['score']
        return score

    def get_thresh(self):
        return self.thresh


def main():
    clsf = GrayBoxClient(base_url='http://127.0.0.1:9002/waf', thresh=0.5)

    # 测试不同的 payload 值
    payloads = [
        "0x1'\tor/*(*/'z,-D'!='z,-Dm'#/**/:0x3~/**/UUX3R",
        "0x1\t/*!union*//*8234*//*!select*/ 1,2,3",
        "1   )    )    As myyh WHeRE 'lL'='lL' OR 7427  =  dbms_pipe.receive_message  (  chr  (  116  )   or chr  (  "
        "87  )  ||chr  (  90  )  ||chr  (  109  )  ,5  )  --"
    ]

    for payload in payloads:
        print(clsf.get_score(payload=payload))


if __name__ == '__main__':
    main()

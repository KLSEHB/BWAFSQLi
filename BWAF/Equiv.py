import time

import requests

from SQLi import *
from entry.Leaf import Leaf, syntax_judge
from cfg.cfg_conf import CFG_CONF

BENIGN_PAYLOADS_PATH = 'text/payload_benign.txt'
MYSQL_FUNCTIONS_PATH = 'text/mysql_functions.txt'
DATABASE_NAMES_PATH = 'text/database_names.txt'
TABLE_NAMES_PATH = 'text/table_names.txt'
COLUMN_NAMES_PATH = 'text/column_names.txt'

char_map = {
    '%': '%25',
    '&': '%26',
    '#': '%23',
    '?': '%3F',
    '/': '%2F',
    '+': '%20',
    '=': '%3D',
}

injection_types = [
    "union", "error", "bool", "time"
]

String_classes = [
    "number", "single_quotation_mark", "double_quotation_mark",
    "single_quotation_mark_bracket", "double_quotation_mark_bracket",
    "single_quotation_mark_percent", "double_quotation_mark_percent"
]

manners = [
    'get', 'post'
]


class WebTest:
    def __init__(self, base_url, manner='get', sleep_time=0, injection_type='union', intercept_status=403, cookie=''):
        self.sleep_time = sleep_time
        self.base_url = base_url
        self.injection_type = injection_type
        self.intercept_status = intercept_status
        self.manner = manner
        self.headers = {
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.159 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        if self.manner == 'post':
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if cookie:
            self.headers['Cookie'] = cookie
        self.s = requests.Session()

    def get_content(self, payload, count):
        count = str(count)
        try:
            time.sleep(self.sleep_time)
            if self.manner == 'get':
                for char, replacement in char_map.items():
                    payload = payload.replace(char, replacement)
                request_url = (self.base_url + "?id=" + payload + "&difficulty="
                               + self.injection_type + "&count=" + count)
                resp = self.s.get(url=request_url, headers=self.headers, timeout=5)
            elif self.manner == 'post':
                request_url = self.base_url
                request_data = {'id': payload, 'difficulty': self.injection_type, 'count': count}
                resp = self.s.post(url=request_url, data=request_data, headers=self.headers, timeout=5)
            return resp.content
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    dataset_root = "dataset/SEJ/"
    http_root = "http://localhost/"
    attacker = SQLi()
    attacker.load_cfgs(CFG_CONF)
    load_benign_payloads(BENIGN_PAYLOADS_PATH)
    load_mysql_functions(MYSQL_FUNCTIONS_PATH)
    load_database_names(DATABASE_NAMES_PATH)
    load_table_names(TABLE_NAMES_PATH)
    load_column_names(COLUMN_NAMES_PATH)
    count = 0
    fail = 0

    for injection_type in injection_types:
        for String_class in String_classes:
            payloads = []
            payload_file = dataset_root + injection_type + "_" + String_class + ".txt"
            try:
                with open(payload_file, 'r') as f:
                    payloads.extend(f.read().splitlines())
            except FileNotFoundError:
                print(f"File {payload_file} not found")
            except Exception as e:
                print(f"Error reading file {payload_file}: {e}")

            for request_manner in manners:
                print(
                    f"Testing - Injection Type: {injection_type}, String Class: {String_class}, Request Method: {request_manner}")

                http_link = http_root + request_manner + "_" + String_class + '.php'

                webtest = WebTest(base_url=http_link, manner=request_manner, injection_type=injection_type)

                for payload in payloads:
                    print(f"Testing payload: {payload}")
                    leaf_entry = Leaf()

                    origin_response_content = webtest.get_content(payload, 0)

                    print(f"Original response content: {origin_response_content}")

                    leaf_entry.generate_leaf_lists(payload)

                    if not syntax_judge(leaf_entry.get_leaf_lists()):
                        raise ValueError("Syntax check failed for the generated leaf lists.")

                    search_before_attack(leaf_entry)

                    all_choices = leaf_entry.mutationPoints_and_mutationStrategies

                    for idx_tuple in all_choices:
                        count += 1

                        attacker.attack(leaf_entry, idx_tuple)

                        output = leaf_entry.get_payload()

                        start_time = time.time()

                        content = webtest.get_content(output, count)

                        end_time = time.time()

                        request_time = end_time - start_time

                        if injection_type == 'time' and request_time < 1:
                            fail += 1
                            print(f"Inconsistent response content, serial number: {count}")
                            print(f"Original payload: {payload.encode()}")
                            print(f"Mutated payload: {output.encode()}")
                            continue
                        if content != origin_response_content:
                            fail += 1
                            print(f"Inconsistent response content, serial number: {count}")
                            print(f"Original payload: {payload.encode()}")
                            print(f"Original response content: {origin_response_content}")
                            print(f"Mutated payload: {output.encode()}")
                            print(f"Mutated response content: {content}")

    print(f"Total mutations: {count}")
    print(f"Equivalence rate: {((count - fail) / count) * 100:.2f}%")
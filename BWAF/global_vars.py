import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--pattern', '-p', required=False, default='BlackBoxClient', choices=[
    'GrayBox', 'BlackBox'], help='attack pattern: ML or WAFaas; ML means local ML SQLi detector and WAFaas '
                                             'means real-world WAF-as-a-service; you need to specify request method '
                                             'when'
                                             ' WAFaas')
parser.add_argument('--guide', '-g', required=False, default='random', choices=[
    'random', 'greedWeight', 'greedWeightAndAllMutation', 'benign'],
                    help='guide method: mcts or random (default); mcts means Monte-Carlo Tree Search')
parser.add_argument('--request_method', '-r', required=False, default='GET(JSON)', choices=[
    'GET', 'GET(JSON)', 'POST', 'POST(JSON)'], help='request method: GET / GET(JSON) / POST / POST(JSON)')
parser.add_argument('--max_attempts', '-mat', required=False, default=1,
                    type=int, help='')
parser.add_argument('--max_steps', '-mst', required=False, default=10, type=int,
                    help='')
parser.add_argument('--payload_number', '-pn', required=False, default='single', choices=[
    'single', 'multiple'], help='payload pattern: single payloads or multi payloads, you need to '
                                'write your payload(s) to the corresponding files (payload_xxx.txt)')
parser.add_argument('--GrayBox_url', '-MLu', required=False, default='default',
                    help='the local ML SQLi detector url (the ML model needs to be deployed as a *service* in advance)')
parser.add_argument('--GrayBox_thresh', '-MLt', required=False, default=0.5,
                    type=float, help='threshold of the local ML SQLi detector')
parser.add_argument('--defend_test', '-d', required=False, action='store_true', help='Defense strategy testing')
parser.add_argument('--BlackBox_url', '-WAFu', required=False,
                    default='default', help='the url of your target WAFaas')
parser.add_argument('--cookie', '-c', required=False, default='', help='cookie')
parser.add_argument('--intercept_status', '-status', required=False, default=403, type=int,
                    help='WAF reject status code')
parser.add_argument('--dataset', '-ds', required=False, default='SQLiCFG', help='dataset')
input_args = parser.parse_args()

benign_payloads = []
mysql_functions = []
database_names = []
table_names = []
column_names = []
score_tables = []
leaf_list = []
request_count = 0
collect_request_count = 0
defend_count = 0


def add_request_count():
    global request_count
    request_count += 1


def get_request_count():
    global request_count
    return request_count


def add_defend_count():
    global defend_count
    defend_count += 1


def get_defend_count():
    global defend_count
    return defend_count


def add_collect_request_count():
    global collect_request_count
    collect_request_count += 1


def get_collect_request_count():
    global collect_request_count
    return collect_request_count


def verify_conditions(_type, token):
    left = 1
    right = 2
    s = token.value
    if s.find('like') != -1:
        left = token.value.split('like')[0].strip()
        right = token.value.split('like')[1].strip()
    elif s.find('=') != -1:
        left = token.value.split('=')[0].strip()
        right = token.value.split('=')[1].strip()
    if left == right:
        return True
    else:
        return False


def read_payloads(path):
    payloads = []
    with open(path) as f:
        while True:
            line = f.readline()
            if line:
                payloads.append(line.rstrip('\n'))
            else:
                break

    return payloads

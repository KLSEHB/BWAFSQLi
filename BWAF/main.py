import copy
import time
import numpy as np
from clients.GrayBoxClient import *
from clients.BlackBoxClient import *
from SQLi import *
from entry.Leaf import *
from entry.GreedWeight import *
import os
from global_vars import *


def run(idx, attacker, payload, log_path, clsf, guide, max_attempts, max_steps, pattern, request_method,
        greedWeight, defend_test):
    fdetail = open('{}/{}-{}-{}#detail.log'.format(log_path, pattern, request_method, guide), 'a+')
    fsuccess = open('{}/{}-{}-{}#success.log'.format(log_path, pattern, request_method, guide), 'a+')
    fpath = open('{}/{}-{}-{}#path.log'.format(log_path, pattern, request_method, guide), 'a+')
    fdefend = open('{}/{}-{}-{}#defend.log'.format(log_path, pattern, request_method, guide), 'a+')
    init_score = clsf.get_score(payload)
    threshold = clsf.get_thresh()
    min_score = init_score
    min_score_payload = payload
    if init_score <= threshold:
        run_res = {'success': False, 'except': None, 'benign': True}
        return run_res
    except_count = 0
    except_detail = ''
    leaf_entry = Leaf()
    leaf_entry.generate_leaf_lists(payload)
    if not syntax_judge(leaf_entry.get_leaf_lists()):
        return {'success': False, 'except': 'Syntax check failed for the generated leaf lists.', 'benign': False}
    search_before_attack(leaf_entry)
    if not leaf_entry.sum_mutationPoints_and_mutationStrategies():
        print('idx:{} [{}] can not parsed to a valid tree'.format(
            idx, payload))
        print('idx:{} [{}] can not parsed to a valid tree'.format(
            idx, payload), file=fdetail, flush=True)
        return {'success': False, 'except': 'can not parsed to a valid tree', 'benign': False}
    attacker.gen_before_attack(leaf_entry, max_attempts)
    greedWeight.add_time_step()
    origin_leaf_lists = copy.deepcopy(leaf_entry.leaf_lists)
    for attempt in range(max_attempts):
        greedWeight.empty_path()
        greedWeight.empty_position()
        try:
            if guide == 'random':
                leaf_entry.leaf_lists = copy.deepcopy(origin_leaf_lists)
                attack_res = attacker.random_attack(idx=idx, attempt=attempt + 1, max_attempts=max_attempts,
                                                    fdetail=fdetail, fsuccess=fsuccess, fpath=fpath,
                                                    leaf_entry=leaf_entry, clsf=clsf, max_steps=max_steps,
                                                    greedWeight=greedWeight)

            elif guide == 'greedWeight':
                leaf_entry.leaf_lists = copy.deepcopy(origin_leaf_lists)
                attack_res = attacker.greedWeight_attack(idx=idx, attempt=attempt + 1, max_attempts=max_attempts,
                                                         fdetail=fdetail, fsuccess=fsuccess, fpath=fpath,
                                                         leaf_entry=leaf_entry, clsf=clsf, max_steps=max_steps,
                                                         greedWeight=greedWeight)
            elif guide == 'greedWeightAndAllMutation':
                leaf_entry.leaf_lists = copy.deepcopy(origin_leaf_lists)
                attack_res = attacker.greedWeightAndAllMutation_attack(idx=idx, attempt=attempt + 1,
                                                                       max_attempts=max_attempts,
                                                                       fdetail=fdetail, fsuccess=fsuccess, fpath=fpath,
                                                                       fdefend=fdefend,
                                                                       leaf_entry=leaf_entry, clsf=clsf,
                                                                       max_steps=max_steps,
                                                                       greedWeight=greedWeight, defend_test=defend_test)

            if attack_res['success']:
                run_res = {'success': True, 'except': None, 'benign': False,
                           'min_score': attack_res['min_score'], 'min_score_payload': attack_res['min_score_payload']}
                return run_res

            if min_score < attack_res['min_score']:
                min_score = attack_res['min_score']
                min_score_payload = attack_res['min_score_payload']
        except Exception as e:
            except_detail = str(e)
            except_count += 1
            continue

    if except_count == max_attempts:
        run_res = {'success': False, 'except': 'Attack Fail:' + except_detail, 'benign': False}
        return run_res

    run_res = {'success': False, 'except': None, 'benign': False,
               'min_score': min_score, 'min_score_payload': min_score_payload}
    return run_res


def main():
    np.random.seed(0)

    if input_args.pattern == 'GrayBox':
        assert (not input_args.GrayBox_url == 'default')
        clsf = GrayBoxClient(base_url=input_args.GrayBox_url, thresh=input_args.GrayBox_thresh)
        request_method = 'GrayBox'

    elif input_args.pattern == 'BlackBox':
        assert (not input_args.BlackBox_url == 'default')
        clsf = BlackBoxClient(base_url=input_args.BlackBox_url, sleep_time=0.001, cookie=input_args.cookie,
                              manner=input_args.request_method, intercept_status=input_args.intercept_status)
        request_method = input_args.request_method

    BENIGN_PAYLOADS_PATH = 'text/payload_benign.txt'
    MYSQL_FUNCTIONS_PATH = 'text/mysql_functions.txt'
    DATABASE_NAMES_PATH = 'text/database_names.txt'
    TABLE_NAMES_PATH = 'text/table_names.txt'
    COLUMN_NAMES_PATH = 'text/column_names.txt'

    pattern = input_args.pattern
    guide = input_args.guide
    max_attempts = input_args.max_attempts
    max_steps = input_args.max_steps
    defend_test = input_args.defend_test
    dataset = input_args.dataset
    payload_path = "DataSet/" + dataset + "/sqli.txt"
    attacker = SQLi()
    attacker.load_cfgs(CFG_CONF)
    payloads = read_payloads(payload_path)
    load_benign_payloads(BENIGN_PAYLOADS_PATH)
    load_mysql_functions(MYSQL_FUNCTIONS_PATH)
    load_database_names(DATABASE_NAMES_PATH)
    load_table_names(TABLE_NAMES_PATH)
    load_column_names(COLUMN_NAMES_PATH)

    begin_time = time.time()
    begin_time_str = time.strftime("%m-%d#%H-%M-%S", time.localtime())
    log_path = 'logs/{}'.format(begin_time_str)
    os.mkdir(log_path)

    if guide == 'benign':
        fbenign = open('{}/{}-{}-{}#benign.log'.format(log_path, pattern, request_method, guide), 'a+')
        threshold = clsf.get_thresh()
        count = 0
        for idx, payload in enumerate(payloads):
            init_score = clsf.get_score(payload)
            if init_score <= threshold:
                count += 1
                print(idx, payload, file=fbenign, flush=True)
        print("benign_count：" + str(count), file=fbenign, flush=True)
        return

    fsummary = open('{}/{}-{}-{}#summary.log'.format(log_path, pattern, request_method, guide), 'a+')

    fbenign = open('{}/{}-{}-{}#benign.log'.format(log_path, pattern, request_method, guide), 'a+')

    fexcept = open('{}/{}-{}-{}#except.log'.format(log_path, pattern, request_method, guide), 'a+')

    counter = {'total': len(payloads), 'success': 0, 'benign': 0, 'except': 0, 'failure': 0}

    greedWeight = GreedWeight()
    for idx, payload in enumerate(payloads):
        run_res = run(idx=idx, attacker=attacker, payload=payload, log_path=log_path, clsf=clsf, guide=guide,
                      max_attempts=max_attempts, max_steps=max_steps, pattern=pattern, request_method=request_method,
                      greedWeight=greedWeight, defend_test=defend_test)

        if run_res['benign']:
            print(idx, payload, file=fbenign, flush=True)
            counter['benign'] += 1

        elif run_res['except']:
            print(idx, payload, run_res['except'], file=fexcept, flush=True)
            counter['except'] += 1

        elif run_res['success']:
            print(idx, 'success', run_res['min_score_payload'].encode())
            counter['success'] += 1

        else:
            counter['failure'] += 1
    end_time = time.time()
    time_consume = end_time - begin_time

    print("================Summary================")
    if input_args.pattern == 'GrayBox':
        print("Guide: {}, GrayBox url: {}, GrayBox thresh: {}".format(
            guide, input_args.GrayBox_url, input_args.GrayBox_thresh))
        print("Guide: {}, GrayBox url: {}, GrayBox thresh: {}".format(
            guide, input_args.GrayBox_url, input_args.GrayBox_thresh, file=fsummary, flush=True))
    elif input_args.pattern == 'BlackBox':
        print("Guide: {}, BlackBox url: {}, Request method:{}, Cookie:{}".format(
            guide, input_args.BlackBox_url, input_args.request_method, input_args.cookie))
        print("Guide: {}, BlackBox url: {}, Request method:{}, Cookie:{}".format(
            guide, input_args.BlackBox_url, input_args.request_method, input_args.cookie), file=fsummary, flush=True)

    print("Total payloads: {}, Success: {}, Failure: {}, Benign: {}, Except: {}".format(
        counter['total'], counter['success'], counter['failure'], counter['benign'], counter['except']))
    print("Total payloads: {}, Success: {}, Failure: {}, Benign: {}, Except: {}".format(
        counter['total'], counter['success'], counter['failure'], counter['benign'], counter['except']), file=fsummary,
        flush=True)

    bypass_rate = round(counter['success'] / (counter['success'] + counter['failure']) if (counter['success'] + counter[
        'failure']) != 0 else 0, 3)
    request_count_rate = round(get_request_count() / counter['success'] if counter['success'] != 0 else 0, 3)

    print("Total time consuming: {}h/{}m/{}s".format(
        round(time_consume / 3600, 4), round(time_consume / 60, 4), round(time_consume, 4)))
    print("Total time consuming: {}h/{}m/{}s".format(
        round(time_consume / 3600, 4), round(time_consume / 60, 4), round(time_consume, 4)), file=fsummary, flush=True)

    print("payload bypass rate: {}, single payload bypass request count: {}".format(bypass_rate, request_count_rate))
    print("payload bypass rate: {}, single payload bypass request count: {}".format(bypass_rate, request_count_rate),
          file=fsummary, flush=True)
    request_time = get_request_count()
    print("Total request time: {}".format(request_time))
    print("Total request time: {}".format(request_time), file=fsummary, flush=True)

    print(greedWeight.print_R())
    print(greedWeight.print_R(), file=fsummary, flush=True)

    if defend_test:
        denominator = counter['total'] - counter['benign'] - counter['except']
        if denominator == 0:
            payload_bypass_rate_after_defense = 0.0
        else:
            payload_bypass_rate_after_defense = round(
                (counter['success'] - get_defend_count()) / denominator, 4
            )

        print("payload bypass rate after defense: {}".format(payload_bypass_rate_after_defense))
        print("payload bypass rate after defense: {}".format(payload_bypass_rate_after_defense),
              file=fsummary, flush=True)

    print("For detail log, please see {}/".format(log_path), file=fsummary, flush=True)
    print("For detail log, please see {}/".format(log_path))


if __name__ == "__main__":
    main()

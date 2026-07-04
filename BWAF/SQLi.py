import traceback
from collections import defaultdict
from cfg.cfg_conf import *
from cfg.cfg_func import *
from clients.defend import *


def load_benign_payloads(path):
    with open(path) as f:
        while True:
            line = f.readline().strip()
            if line:
                benign_payloads.append(line)
            if not line:
                break


def load_mysql_functions(path):
    with open(path) as f:
        while True:
            line = f.readline().strip()
            if line:
                mysql_functions.append(line)
            if not line:
                break


def load_database_names(path):
    with open(path) as f:
        while True:
            line = f.readline().strip()
            if line:
                database_names.append(line)
            if not line:
                break


def load_table_names(path):
    with open(path) as f:
        while True:
            line = f.readline().strip()
            if line:
                table_names.append(line)
            if not line:
                break


def load_column_names(path):
    with open(path) as f:
        while True:
            line = f.readline().strip()
            if line:
                column_names.append(line)
            if not line:
                break


def search_before_attack(leaf_entry):
    for entry in CFG_CONF_ENTRY:
        leaf_entry.generate_mutationPoints_and_mutationStrategies(entry)


def generate_terminal(sym, arg):

    if sym.startswith('F_'):
        try:
            return eval(sym)()
        except Exception as e:
            print(f"Error while generating terminal {sym}: {e}")
            return ''
    elif sym.startswith('A_'):
        try:
            return eval(sym)(arg)
        except Exception as e:
            print(f"Error while generating terminal {sym}: {e}")
            return ''
    else:
        return sym


class SQLi:
    def __init__(self):
        self.cfg_prods = defaultdict(list)
        self.payload = None
        self.processed_payload = None

    def add_cfg(self, lhs, rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.cfg_prods[lhs].append(tuple(prod.split()))

    def load_cfgs(self, cfgs):
        for key in cfgs:
            for value in cfgs[key]:
                self.add_cfg(key, value)

    def generate_random_convergent(self, symbol, arg=None, convergenceFactor=0.5, pCount=None):
        if pCount is None:
            pCount = {}
        sentence = ''
        weights = self.calculate_weights(symbol, pCount, convergenceFactor)
        rand_prod = random.choices(self.cfg_prods[symbol], weights=weights, k=1)[0]
        pCount[rand_prod] = pCount.get(rand_prod, 0) + 1
        for sym in rand_prod:
            if sym in self.cfg_prods:
                new_pCount = pCount.copy()
                sentence += self.generate_random_convergent(sym, arg, convergenceFactor, new_pCount)
            else:
                sentence += generate_terminal(sym, arg)

        return sentence

    def calculate_weights(self, symbol, pCount, cfactor):
        weights = []
        for prod in self.cfg_prods[symbol]:
            freq_factor = cfactor ** pCount.get(prod, 1)
            weights.append(freq_factor)
        return weights

    def random_attack(self, idx, attempt, max_attempts, fdetail, fsuccess, fpath, leaf_entry, clsf, max_steps,
                      greedWeight):
        min_score = 1
        min_score_payload = ''
        origin_output = leaf_entry.get_payload()
        try:
            all_choices = leaf_entry.mutationStrings_and_mutationStrategies
            step = min(max_steps, len(all_choices))
            for stp in range(step):
                if not all_choices:
                    break
                polices = [item for item in list(set(item[2] for item in all_choices)) if item not in greedWeight.path]
                if not polices:
                    break
                policy = random.choice(polices)
                greedWeight.add_path(policy)
                extracted = [item for item in all_choices if item[2] == policy and item[0] not in greedWeight.position]
                if not extracted:
                    break
                idx_tuple = random.choice(extracted)
                random_string = random.choice(idx_tuple[4])
                greedWeight.add_position(idx_tuple[0])
                idx_tuple[4].remove(random_string)
                if len(idx_tuple[4]) == 0:
                    all_choices.remove(idx_tuple)
                self.attack(leaf_entry, idx_tuple, True, random_string)
                output = leaf_entry.get_payload()
                score = clsf.get_score(output)
                add_request_count()
                print("idx:{} attempt:{}/{} step:{}/{}  {} {}".format(idx, attempt,
                                                                      max_attempts, stp + 1, step, score,
                                                                      (output + " ").encode()), file=fdetail,
                      flush=True)
                if score < min_score:
                    greedWeight.update_ranking(policy, True)
                    min_score = score
                    min_score_payload = output
                if score <= clsf.get_thresh():
                    print(idx, '\t', (origin_output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', (output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', greedWeight.path, file=fpath, flush=True)
                    return {'success': True, 'except': None, 'benign': False, 'min_score': min_score,
                            'min_score_payload': min_score_payload, 'success_step': stp + 1, 'max_step': step}
                greedWeight.update_ranking(policy, False)
        except Exception as e:
            print('EXCEPT', e)
            print('EXCEPT', e, file=fdetail, flush=True)
            traceback.print_exc()
            return {'success': False, 'except': 'attack except'}
        return {'success': False, 'except': None, 'benign': False, 'min_score': min_score,
                'min_score_payload': min_score_payload, 'success_step': None, 'max_step': step}

    def greedWeight_attack(self, idx, attempt, max_attempts, fdetail, fsuccess, fpath, leaf_entry, clsf,
                           max_steps, greedWeight):
        min_score = 1
        origin_output = leaf_entry.get_payload()
        min_score_payload = ''
        try:
            all_choices = leaf_entry.mutationStrings_and_mutationStrategies
            step = min(max_steps, len(all_choices))
            for stp in range(step):
                if not all_choices:
                    break
                polices = [item for item in list(set(item[2] for item in all_choices)) if item not in greedWeight.path]
                if not polices:
                    break
                policy = greedWeight.experience_based_guide(polices)
                greedWeight.add_path(policy)
                extracted = [item for item in all_choices if item[2] == policy and item[0] not in greedWeight.position]
                if not extracted:
                    break
                idx_tuple = random.choice(extracted)
                random_string = random.choice(idx_tuple[4])
                idx_tuple[4].remove(random_string)
                greedWeight.add_position(idx_tuple[0])
                if len(idx_tuple[4]) == 0:
                    all_choices.remove(idx_tuple)
                self.attack(leaf_entry, idx_tuple, True, random_string)
                output = leaf_entry.get_payload()
                score = clsf.get_score(output)
                add_request_count()
                print("idx:{} attempt:{}/{} step:{}/{}  {} {}".format(idx, attempt,
                                                                      max_attempts, stp + 1, step, score,
                                                                      (output + " ").encode()), file=fdetail,
                      flush=True)
                if score < min_score:
                    min_score = score
                    min_score_payload = output
                if score <= clsf.get_thresh():
                    greedWeight.update_ranking(policy, True)
                    print(idx, '\t', (origin_output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', (output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', greedWeight.path, file=fpath, flush=True)
                    return {'success': True, 'except': None, 'benign': False, 'min_score': min_score,
                            'min_score_payload': min_score_payload, 'success_step': stp + 1, 'max_step': step}
                greedWeight.update_ranking(policy, False)
        except Exception as e:
            print('EXCEPT', e)
            print('EXCEPT', e, file=fdetail, flush=True)
            traceback.print_exc()
            return {'success': False, 'except': 'attack except'}
        return {'success': False, 'except': None, 'benign': False, 'min_score': min_score,
                'min_score_payload': min_score_payload, 'success_step': None, 'max_step': step}

    def greedWeightAndAllMutation_attack(self, idx, attempt, max_attempts, fdetail, fsuccess, fpath, fdefend,
                                         leaf_entry, clsf, max_steps, greedWeight, defend_test=False):
        min_score = 1
        origin_output = leaf_entry.get_payload()
        min_score_payload = ''
        try:
            all_choices = leaf_entry.mutationStrings_and_mutationStrategies
            step = min(max_steps, len(all_choices))
            for stp in range(step):
                if not all_choices:
                    break
                polices = [item for item in list(set(item[2] for item in all_choices)) if item not in greedWeight.path]
                if not polices:
                    break
                extracted_all_choices = [item for item in all_choices if item[0] not in greedWeight.position]
                extracted_polices = [item for item in list(set(item[2] for item in extracted_all_choices)) if item not in greedWeight.path]
                if not extracted_polices:
                    break
                policy = greedWeight.experience_based_guide(extracted_polices)
                greedWeight.add_path(policy)
                extracted = [item for item in extracted_all_choices if item[2] == policy]
                if not extracted:
                    break
                for idx_tuple in extracted:
                    random_string = random.choice(idx_tuple[4])
                    idx_tuple[4].remove(random_string)
                    greedWeight.add_position(idx_tuple[0])
                    if len(idx_tuple[4]) == 0:
                        all_choices.remove(idx_tuple)
                    self.attack(leaf_entry, idx_tuple, True, random_string)
                output = leaf_entry.get_payload()
                score = clsf.get_score(output)
                add_request_count()
                print("idx:{} attempt:{}/{} step:{}/{}  {} {}".format(idx, attempt,
                                                                      max_attempts, stp + 1, step, score,
                                                                      (output + " ").encode()), file=fdetail,
                      flush=True)
                if score < min_score:
                    min_score = score
                    min_score_payload = output
                if score <= clsf.get_thresh():  # 成功绕过
                    if defend_test:
                        defend_output = defend_process(output)
                        defend_score = clsf.get_score(defend_output)
                        if defend_score > score:
                            add_defend_count()
                            print(idx, '\t', (output + " ").encode(), file=fdefend, flush=True)
                            print(idx, '\t', (defend_output + " ").encode(), file=fdefend, flush=True)
                    greedWeight.update_ranking(policy, True)
                    print(idx, '\t', (origin_output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', (output + " ").encode(), file=fsuccess, flush=True)
                    print(idx, '\t', greedWeight.path, file=fpath, flush=True)
                    return {'success': True, 'except': None, 'benign': False, 'min_score': min_score,
                            'min_score_payload': min_score_payload, 'success_step': stp + 1, 'max_step': step}
                greedWeight.update_ranking(policy, False)
        except Exception as e:
            print('EXCEPT', e)
            print('EXCEPT', e, file=fdetail, flush=True)
            traceback.print_exc()
            return {'success': False, 'except': 'attack except'}
        return {'success': False, 'except': None, 'benign': False, 'min_score': min_score,
                'min_score_payload': min_score_payload, 'success_step': None, 'max_step': step}

    def attack(self, leaf_entry, idx_tuple, just_replace=False, replace_string=''):
        if just_replace:
            replace_location = idx_tuple[0]
        else:
            prod = CFG_CONF_ENTRY[idx_tuple[3]][0]
            string_to_be_replace = idx_tuple[1]
            replace_location = idx_tuple[0]
            replace_string = self.generate_random_convergent(prod, string_to_be_replace)
        leaf_entry.replace_leaf(replace_string=replace_string, replacement=replace_location)

    def gen_before_attack(self, leaf_entry, t=10):
        mutationStrings_and_mutationStrategies = []
        for idx_tuple in leaf_entry.mutationPoints_and_mutationStrategies:
            prod = CFG_CONF_ENTRY[idx_tuple[3]][0]
            string_to_be_replace = idx_tuple[1]
            stmts = []
            for _ in range(t):  # # 生成多组替换字符串
                stmt = self.generate_random_convergent(prod, string_to_be_replace)
                if stmt not in stmts:  # 去重
                    stmts.append(stmt)
            stmts_and_nodes = []
            for stmt in stmts:
                stmts_and_nodes.append(stmt)
            mutationStrings_and_mutationStrategies.append(idx_tuple + (stmts_and_nodes,))
        leaf_entry.mutationStrings_and_mutationStrategies = mutationStrings_and_mutationStrategies
        return mutationStrings_and_mutationStrategies

from global_vars import verify_conditions
from SQLi import *


def syntax_judge(leafs):
    for leaf in leafs:
        for node in leaf:
            if node[2] == 'Token.Literal.String.Single' and ' ' in node[0]:
                return False
    else:
        return True


def closed_symbol_partition(payload):
    left_closure_pattern = r'^[-]?[a-zA-Z0-9]*[%]?[\'"][\)]*'
    left_closure_match = re.search(left_closure_pattern, payload)
    if left_closure_match:
        left_closure_idx = left_closure_match.end()
        return [payload[:left_closure_idx], payload[left_closure_idx:]]
    else:
        return [payload]


def semicolon_division(payload):
    sql_statements = payload.split(';')
    for index, sql_statement in enumerate(sql_statements):
        if index != len(sql_statements) - 1:
            sql_statements[index] = sql_statements[index] + ";"
    return sql_statements


class Leaf:
    def __init__(self):
        self.leaf_lists = []
        self.mutationPoints_and_mutationStrategies = []
        self.mutationStrings_and_mutationStrategies = []

    def parse_leaf(self, tokens):
        leaf_list = []

        if isinstance(tokens, sqlparse.sql.Comparison):
            if verify_conditions("Comparison", tokens):
                return [[tokens.value, str(type(tokens)), str(tokens.ttype)]]
            else:
                for token in tokens:
                    leaf_list.extend(self.parse_leaf(token))
                return leaf_list

        if type(tokens) in LEAF_NODE_TYPE_DICT:
            return [[tokens.value, str(type(tokens)), str(tokens.ttype)]]

        for token in tokens:
            leaf_list.extend(self.parse_leaf(token))

        return leaf_list

    def generate_leaf_list(self, statement):
        token = sqlparse.parse(statement)
        return self.parse_leaf(token)

    def generate_leaf_lists1(self, payload):
        self.leaf_lists = []
        semicolon_count = payload.count(';')
        if semicolon_count == 0:
            sentences = closed_symbol_partition(payload)
            for sentence in sentences:
                self.leaf_lists.append(self.generate_leaf_list(sentence))
        else:
            semicolon_index = payload.find(';')
            part1 = payload[:semicolon_index + 1]
            part2 = payload[semicolon_index + 1:]
            sentences = closed_symbol_partition(part1)
            for sentence in sentences:
                self.leaf_lists.append(self.generate_leaf_list(sentence))
            if len(part2) != 0 and not all(c.isspace() for c in part2):
                tokens = sqlparse.parse(part2)
                for token in tokens:
                    self.leaf_lists.append(self.generate_leaf_list(token.value))

    def generate_leaf_lists(self, payload):
        self.leaf_lists = []
        semicolon_count = payload.count(';')
        if semicolon_count == 0:
            sentences = closed_symbol_partition(payload)
        else:
            sentences = semicolon_division(payload)
            new_sentences = []
            for index, sentence in enumerate(sentences):
                if index == 0:
                    for new_sentence in closed_symbol_partition(sentence):
                        new_sentences.append(new_sentence)
                else:
                    new_sentences.append(sentence)
            sentences = new_sentences
        for sentence in sentences:
            token = sqlparse.parse(sentence)
            if len(token) != 0:
                self.leaf_lists.append(self.parse_leaf(token))

    def get_payload(self):
        payload = ''
        for leaf_list in self.leaf_lists:
            for leaf in leaf_list:
                payload += leaf[0]
        return payload

    def get_leaf_lists(self):
        return self.leaf_lists

    def replace_leaf(self, replacement, replace_string):
        if replace_string in [' ', "\t", "\n", "\r", "\f", "\v"]:
            token = sqlparse.parse('select' + replace_string)[0][1]
        else:
            token = sqlparse.parse(replace_string)[0]
        self.leaf_lists[replacement[0]][replacement[1]][0] = token.value
        self.leaf_lists[replacement[0]][replacement[1]][1] = str(type(token))
        self.leaf_lists[replacement[0]][replacement[1]][2] = str(token.ttype)

    def generate_mutationPoints_and_mutationStrategies(self, entry):
        entry_id = CFG_CONF_ENTRY[entry][2]
        stmt = CFG_CONF_ENTRY[entry][0]
        index = stmt.find('_')
        if index != -1:
            prefix = stmt[:index]
            suffix = stmt[index + 1:]
        else:
            prefix = stmt
            suffix = stmt
        for i, leaf_list in enumerate(self.leaf_lists):
            for j, leaf in enumerate(leaf_list):
                location = (i, j)
                value = leaf[0]
                value_type = leaf[1]
                value_ttype = leaf[2]
                if prefix.startswith('T'):
                    token_name = suffix
                    if TOKEN_TYPE_DICT[token_name][1] is None:
                        if value_type == TOKEN_TYPE_DICT[token_name][0]:
                            self.mutationPoints_and_mutationStrategies.append((location, value, entry_id, entry))
                    else:
                        for _type in TOKEN_TYPE_DICT[token_name][1]:
                            if "Token.Literal.Number.Integer" == _type and (i != 0 or j != 0):
                                continue
                            if (_type in ['Token.Literal.String.Single', 'Token.Literal.String.Symbol']
                                    and self.leaf_lists[i][j - 1][0] != '='):
                                continue
                            if value_ttype == _type:
                                self.mutationPoints_and_mutationStrategies.append((location, value, entry_id, entry))
                elif prefix.startswith('S'):  # Sx_
                    if value == suffix:
                        self.mutationPoints_and_mutationStrategies.append((location, value, entry_id, entry))
                # = 和 #
                elif value == stmt:
                    self.mutationPoints_and_mutationStrategies.append((location, value, entry_id, entry))

    def sum_mutationPoints_and_mutationStrategies(self):
        return len(self.mutationPoints_and_mutationStrategies)


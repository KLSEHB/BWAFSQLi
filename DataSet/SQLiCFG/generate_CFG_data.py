from BWAF.SQLi import *
from BWAF.cfg.cfg_conf import CFG_CONF

attacker = SQLi()
attacker.load_cfgs(CFG_CONF)

BENIGN_PAYLOADS_PATH = '../../text/payload_benign.txt'
MYSQL_FUNCTIONS_PATH = '../../text/mysql_functions.txt'
DATABASE_NAMES_PATH = '../../text/database_names.txt'
TABLE_NAMES_PATH = '../../text/table_names.txt'
COLUMN_NAMES_PATH = '../../text/column_names.txt'


load_benign_payloads(BENIGN_PAYLOADS_PATH)
load_mysql_functions(MYSQL_FUNCTIONS_PATH)
load_database_names(DATABASE_NAMES_PATH)
load_table_names(TABLE_NAMES_PATH)
load_column_names(COLUMN_NAMES_PATH)

# norm_data_set = set()
# while len(norm_data_set) < 10000:
#     stmt = attacker.gen_random_convergent('norm_Payload')
#     norm_data_set.add(stmt)

sqli_data_set = set()
while len(sqli_data_set) < 5:
    stmt = attacker.generate_random_convergent('QuoteContext')
    print(stmt)
    sqli_data_set.add(stmt)
#
#
# with open('norm.txt', 'w') as file:
#     for data in norm_data_set:
#         file.write(data + '\n')

# with open('sqli.txt', 'w') as file:
#     for data in sqli_data_set:
#         file.write(data + '\n')

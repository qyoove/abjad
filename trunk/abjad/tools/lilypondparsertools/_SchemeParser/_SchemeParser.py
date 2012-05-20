import inspect
import logging
import os

from ply import lex
from ply import yacc

from abjad.tools import schemetools
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler


class _SchemeParser(object):

    ### INITIALIZER ###

    def __init__(self, debug=False):
        class_path = inspect.getfile(self.__class__)
        self.output_path = class_path.rpartition(os.path.sep)[0]
        self.pickle_path = os.path.join(self.output_path, '_parsetab.pkl')
        self.logger_path = os.path.join(self.output_path, 'parselog.txt')

        self.debug = bool(debug)

        # setup a logging
        if self.debug:
            logging.basicConfig(
                level = logging.DEBUG,
                filename = self.logger_path,
                filemode = 'w',
                format = '%(filename)10s:%(lineno)8d:%(message)s'
            )
            self.logger = logging.getLogger()
        else:
            self.logger = logging.getLogger()
            self.logger.addHandler(_NullHandler()) # use custom NullHandler for 2.6 compatibility

        # setup PLY objects
        self.lexer = lex.lex(
            debug=True,
            debuglog=self.logger,
            object=self,
        )
        self.parser = yacc.yacc(
            debug=True,
            debuglog=self.logger,
            module=self,
            outputdir=self.output_path,
            picklefile=self.pickle_path,
        )

        self._expression_depth = 0

    ### SPECIAL METHODS ###

    def __call__(self, input_string):
        #self.lexer.input(input_string)
        #for token in self.lexer:
        #    print token
        self.expression_depth = 0

        #if os.path.exists(self.logger_path):
        #    os.remove(self.logger_path)

        if self.debug:
            result = self.parser.parsedebug(
                input_string,
                lexer=self.lexer,
                debug=self.logger)
        else:
            result = self.parser.parse(
                input_string,
                lexer=self.lexer)

        if hasattr(self, 'cleanup'):
            result = self.cleanup(result)
        return result

    ### PUBLIC METHODS ###

    def tokenize(self, input_string):
        self.lexer.input(input_string)
        for token in self.lexer:
            print token

    ### LEX SETUP ###

    N               = r'[0-9]'
    DIGIT           = r'%s' % N
    UNSIGNED        = r'%s+' % N
    INT             = r'(-?%s)' % UNSIGNED
    REAL            = r'((%s\.%s*)|(-?\.%s+))' % (INT, N, N)

    states = (
        ('quote', 'exclusive'),
    )

    tokens = (
        'BOOLEAN',
        'DECIMAL',
        #'ELLIPSIS',
        'HASH',
        'INTEGER',
        'L_PAREN',
        'R_PAREN',
        'STRING',
    )

    literals = (
        '&', # AMPERSAND
        '*', # ASTERISK
        '^', # CARAT
        ':', # COLON
        '$', # DOLLAR
        '=', # EQUALS
        '!', # EXCLAMATION
        '<', # L_CARAT
        '(', # L_PAREN
        '-', # MINUS
        '%', # PERCENT
        '.', # PERIOD
        '+', # PLUS
        '?', # QUESTION
        "'", # QUOTE
        '>', # R_CARAT
        ')', # R_PAREN
        '/', # SLASH
        '~', # TILDE
        '_', # UNDERSCORE
    )

    #t_ELLIPSIS = '\.\.\.'

    t_ignore = ' \t\r'

    ### LEX METHODS ###

    def t_BOOLEAN(self, t):
        r'\#(T|F|t|f)'
        if t.value[-1].lower() == 't':
            t.value = True
        else:
            t.value = False
        return t

    @lex.TOKEN(REAL)
    def t_DECIMAL(self, t):
        t.value = float(t.value)
        return t

    def t_HASH(self, t):
        r'\#'
        return t

    @lex.TOKEN(INT)
    def t_INTEGER(self, t):
        t.value = int(t.value)
        return t

    def t_L_PAREN(self, t):
        r'\('
        self.expression_depth += 1
        return t

    def t_R_PAREN(self, t):
        r'\)'
        self.expression_depth -= 1
        return t

    def t_quote(self, t):
        r'\"'
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    def t_quote_440(self, t):
        r'''\\[nt\\'"]'''
        self.string_accumulator += t.value
        pass

    def t_quote_443(self, t):
        r'[^\\""]+'
        self.string_accumulator += t.value
        pass

    def t_quote_446(self, t):
        r'\"'
        t.lexer.pop_state( )
        t.type = 'STRING'
        t.value = self.string_accumulator
        self.string_accumulator = ''
        return t

    def t_quote_456(self, t):
        r'.'
        self.string_accumulator += t.value
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_quote_error = t_error
    t_quote_ignore = t_ignore

    ### YACC SETUP ###

    precedence = (
        ('left', 'INTEGER'),
    )

    start = 'program'

    ### YACC METHODS ###

    ### program ###

    '''<program> : <form>*'''

    def p_program__forms(self, p):
        '''program : forms'''
        p[0] = p[1]

    def p_forms__EMPTY(self, p):
        '''forms : '''
        p[0] = []

    def p_forms__forms__form(self, p):
        '''forms : forms form'''
        p[0] = p[1] + [p[2]]

    ### form ###

    '''<form> : <definition> | <expression>'''

    def p_form__expression(self, p):
        '''form : expression'''
        p[0] = p[1]
        self.result = p[1]
        raise Exception

    ### definition ###

    '''<definition> : <variable definition>
    |   <syntax definition>
    |   (begin <definition>*)
    |   (let-syntax (<syntax binding>*) <definition>*)
    |   (letrec-syntax (<syntax binding>*) <definition>*)
    |   <derived definition>
    '''

    ### variable definition ###

    '''<variable definition> : (define <variable> <expression>)
    |   (define (<variable> <variable>*) <body>)
    |   (define (<variable> <variable>* . <variable>) <body>)
    '''

    ### variable ###

    '''<variable> : <identifier>'''

    ### body ###

    '''<body> : <definition>* <expression>+'''

    ### syntax definition ###

    '''<syntax definition> : (define-syntax <keyword> <transformer expression>)'''

    ### keyword ###

    '''<keyword> : <identifier>'''

    ### syntax binding ###

    '''<syntax binding> : (<keyword> <transformer expression>)'''

    ### expression ###

    '''<expression> : <constant>
    |   <variable>
    |   (quote <datum>) | ' <datum>
    |   (lambda <formals> <body>)
    |   (if <expression> <expression> <expression>) | (if <expression> <expression>)
    |   (set! <variable> <expression>)
    |   <application>
    |   (let-syntax (<syntax binding>*) <expression>+)
    |   (letrec-syntax (<syntax binding>*) <expression>+)
    |   <derived expression>
    '''

    def p_expression__QUOTE__datum(self, p):
        '''expression : "'" datum'''
        datum = p[2]
        if isinstance(datum, schemetools.Scheme):
            if datum._quoting:
                datum._quoting = "'" + datum._quoting
            else:
                datum._quoting = "'"
            p[0] = datum
        else:
            p[0] = schemetools.Scheme(datum, quoting="'")

    def p_expression__constant(self, p):
        '''expression : constant'''
        p[0] = p[1]

    ### constant ###

    '''<constant> : <boolean> | <number> | <character> | <string>'''

    def p_constant__boolean(self, p):
        '''constant : boolean'''
        p[0] = p[1] 

    def p_constant__number(self, p):
        '''constant : number'''
        p[0] = p[1] 

    def p_constant__string(self, p):
        '''constant : string'''
        p[0] = p[1] 

    ### formals ###

    '''<formals> : <variable> | (<variable>*) | (<variable>+ . <variable>)'''

    ### application ###

    '''<application> : (<expression> <expression>*)'''

    ### identifier ###

    '''<identifier> : <initial> <subsequent>* | + | - | ...'''

    ### initial ###

    '''<initial> : <letter> | ! | $ | % | & | * | / | : | < | = | > | ? | ~ | _ | ^'''

    ### subsequent ###

    '''<subsequent> : <initial> | <digit> | . | + | -'''

    ### letter ###

    '''<letter> : a | b | ... | z'''

    ### digit ###

    '''<digit> : 0 | 1 | ... | 9'''

    ### datum ###

    '''<datum> : <boolean> | <number> | <character> | <string> | <symbol> | <list> | <vector>'''

    def p_datum__constant(self, p):
        '''datum : constant'''
        p[0] = p[1]

    #def p_datum__boolean(self, p):
    #    '''datum : boolean'''
    #    p[0] = p[1]

    #def p_datum__number(self, p):
    #    '''datum : number'''
    #    p[0] = p[1]

    #def p_datum__string(self, p):
    #    '''datum : string'''
    #    p[0] = p[1]

    def p_datum__list(self, p):
        '''datum : list'''
        p[0] = p[1]

    def p_datum__vector(self, p):
        '''datum : vector'''
        p[0] = p[1]

    def p_data__EMPTY(self, p):
        '''data : '''
        p[0] = []

    def p_data__data__datum(self, p):
        '''data : data datum'''
        p[0] = p[1] + [p[2]]

    ### boolean ###

    '''<boolean> : #t | #f'''

    def p_boolean__BOOLEAN(self, p):
        '''boolean : BOOLEAN'''
        p[0] = p[1]

    ### number ###
    
    '''<number> : <num 2> | <num 8> | <num 10> | <num 16>'''

    def p_number__DECIMAL(self, p):
        '''number : DECIMAL'''
        p[0] = p[1]

    def p_number__INTEGER(self, p):
        '''number : INTEGER'''
        p[0] = p[1]

    ### character ###

    '''<character> : #\ <any character> | #\newline | #\space'''

    ### string ###

    '''<string> : " <string character>* "'''

    def p_string__STRING(self, p):
        '''string : STRING'''
        p[0] = p[1]

    ### string character ###

    '''<string character> : \" | \\ | <any character other than " or \>'''

    ### symbol ###

    '''<symbol> : <identifier>'''

    ### vector ###

    '''<vector> : #(<datum>*)'''

    def p_vector__HASH__L_PAREN__data__R_PAREN(self, p):
        '''vector : HASH L_PAREN data R_PAREN'''
        p[0] = p[3]

    ### list ###

    '''<list> : (<datum>*) | (<datum>+ . <datum>) | <abbreviation>'''

    def p_list__L_PAREN__data__R_PAREN(self, p):
        '''list : L_PAREN data R_PAREN'''
        p[0] = p[2]

    def p_list__L_PAREN__data__PERIOD__datum(self, p):
        '''list : L_PAREN data datum "." datum R_PAREN'''
        result = p[2] + [p[3]] + [p[5]]
        if len(result) == 2:
            p[0] = schemetools.SchemePair(*result)
        else:
            p[0] = schemetools.Scheme(*result)

    ### abbreviation ###

    '''<abbreviation> : ' <datum> | ` <datum> | , <datum> | ,@ <datum>'''

    ### error ###

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

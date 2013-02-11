#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.idrules import *
from splparser.cmdparsers.common.keyrules import *
from splparser.cmdparsers.common.typerules import *
from splparser.cmdparsers.common.valuerules import *

from splparser.cmdparsers.lookuplexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_lookup(p):
    """cmdexpr : lookupcmd"""
    p[0] = p[1]

def p_lookup_tablename(p):
    """lookupcmd : LOOKUP table"""
    p[0] = ParseTreeNode('LOOKUP')
    p[0].add_children(p[2])

def p_lookup_options_tablename(p):
    """lookupcmd :  LOOKUP key EQ value table"""
    p[0] = ParseTreeNode('LOOKUP')
    option = ParseTreeNode(p[2].raw.upper())
    boolean = p[4]
    option.add_child(boolean)
    p[0].add_children([option] + p[5])

def p_table_tablename(p):
    """table : field"""
    p[0] = [p[1]]

def p_table_tablename_field(p):
    """table : field field"""
    p[0] = [p[1], p[2]]

def p_table_tablename_field_output(p):
    """table : field field out"""
    p[0] = [p[1], p[2], p[3]]

def p_field_as(p):
    """field : field ASLC field
             | field ASUC field"""
    _as = ParseTreeNode('AS')
    _as.add_child(p[3])
    p[1].add_child(_as)
    p[0] = p[1]

def p_out(p):
    """out : OUTPUT field
           | OUTPUTNEW field"""
    p[0] = ParseTreeNode(p[1])
    p[0].add_child(p[2])

def p_error(p):
    raise SPLSyntaxError("Syntax error in lookup parser input!")

logging.basicConfig(
    level = logging.DEBUG,
    filename = "statsparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="lookup_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)

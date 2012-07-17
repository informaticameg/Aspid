#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2012 Informática MEG <contacto@informaticameg.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import re
from ply import *

keywords = '''
        GROUP COUNT EXCLUDE REGEXP
        ZEROORONE ZEROORMORE ONEORMORE
        OR NOT
        '''
tokens = tuple((keywords + '''
    INDEX_1 INDEX_2
    LPAREN RPAREN
     
    DOT 
    NEWLINE 
    ID
    STRING''').split())


t_LPAREN      = r'\('
t_RPAREN      = r'\)'
#~ t_LBRACKET    = r'\['
#~ t_RBRACKET    = r'\]'
t_DOT         = r'.'
t_GROUP       = r"(\[)([a-zA-Z0-9\\#\\¡\\$:.,¿?+=&%@!-_],?:?)+(\])"
t_INDEX_1     = r'\([0-9]\)'
t_INDEX_2     = r'\([0-9]+:[0-9]*\)'
t_STRING      = r'[\"|\']([^\\\n]|(\\.))*?[\"|\']'

t_ignore      = r' \t'

def t_comment(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1
    
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_ID(t):
    r'[0-9a-zA-Z]+'
    if t.value in keywords:
        t.type = t.value
    return t
    
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(reflags=re.IGNORECASE,debug=0)







       
   
  
            







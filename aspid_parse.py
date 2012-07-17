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

from ply import *
import aspid_lex

tokens = aspid_lex.tokens

def p_program(p):
    '''program : program command 
               | command'''
    if len(p) == 2 and p[1]:
       p[0] = { }
       line,stat = p[1]
       p[0][line] = stat
    elif len(p) ==3:
       p[0] = p[1]
       if not p[0]: p[0] = { }
       if p[2]:
           line,stat = p[2]
           p[0][line] = stat

def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1
        
#### Format of all ASPID statements.
        
def p_command_1(p):
    '''command : GROUP'''
    group = p[1][1:-1]
    p[0] = (p.lineno(1),('GROUP',group))

def p_command_2(p):
    '''command : GROUP DOT COUNT index_stmt'''    
    group = p[1][1:-1]
    p[0] = (p.lineno(1),('GROUP',(group,('COUNT',p[4]))))
    
def p_command_3(p):
    '''command : GROUP DOT EXCLUDE GROUP'''    
    group = p[1][1:-1]
    p[0] = (p.lineno(1),('GROUP',(group,('EXCLUDE',p[4]))))

def p_command_4(p):
    '''command : NOT LPAREN GROUP RPAREN'''
    group = p[3][1:-1]
    p[0] = (p.lineno(1),('NOT',('GROUP',group) ) )
        
def p_command_5(p):
    '''command : OR LPAREN GROUP RPAREN'''
    group = p[3][1:-1]
    p[0] = (p.lineno(1),('OR',('GROUP',group) ) )
    
def p_command_6(p):
    '''command : REGEXP LPAREN STRING RPAREN'''
    regexp = p[3][1:-1]
    p[0] = (p.lineno(1),('REGEXP',regexp))
    
def p_command_nl(p):
    '''command : NEWLINE'''
    p[0] = None
    
def p_index_stmt(p):
    '''index_stmt : INDEX_1
                  | INDEX_2
                  | LPAREN ONEORMORE RPAREN
                  | LPAREN ZEROORONE RPAREN
                  | LPAREN ZEROORMORE RPAREN'''
    if len(p) == 2:        
        p[0] = p[1][1:-1]
    if len(p) == 4:
        p[0] = p[2]
    
    
#### Catastrophic error handler
def p_error(p):
    if not p:
        return "SYNTAX ERROR AT EOF"
    else:
        msj = "AN ERROR HAS OCURRED IN LINE <%s> IN THE VALUE <%s>" % (p.lexpos, p.value)
        return msj
    
aspid_parser = yacc.yacc()

def parse(data,debug=0):
    aspid_parser.error = 0
    p = aspid_parser.parse(data,debug=debug)
    if aspid_parser.error: 
        return aspid_parser.error
    return p




       
   
  
            







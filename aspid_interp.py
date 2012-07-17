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

import sys

class AspidInterpreter:

    # Initialize the interpreter. prog is a dictionary
    # containing (line_number,(statement)) mappings
    def __init__(self,prog):
        print prog
        self.prog = prog
        self.result = r''
        
        self.constants = {           # Built-in constants table
            'PAIR':r'\d*[0|2|4|6|8]$',
            'UNPAIR':r'\d*[1|3|5|7|9]$',
            'LOWER':r'([a-z])',
            'UPPER':r'([A-Z])',
            'ALPHABETIC':r'([a-zA-Z])*',
            'ALPHANUMERIC':'([a-zA-Z0-9])*',
            'NUMERIC':r'\d+'
        }
        # characters to scape
        self.metacharacters = '[ ] ( ) { } < > . + * | $ ^'.split()

    # Run it
    def run(self):
        #~ self.error  = 0              # Indicates program error
        self.stat = list(self.prog)  # Ordered list of all line numbers
        self.stat.sort()
        self.pc = 0                  # Current program counter

        # Processing prior to running

        #self.collect_data()          # Collect all of the data statements
        #self.check_end()
        #self.check_loops()

        #~ if self.error: raise RuntimeError
        for line in self.stat:
            line  = self.stat[self.pc]
            instruction = self.prog[line]
            # Dict with possible cases
            cases = {                
                'GROUP'  : self.analize_group,
                'OR'     : self.analize_or,
                'NOT'    : self.analize_not,
                'REGEXP' : self.analize_regexp
            }
            # Call the method related case
            instruction = list(instruction)
            self.result += cases[instruction[0]](instruction)
            # Increment program counter
            self.pc += 1
        return self.result

    # Utility functions
    def analize_group(self, statement, OR = False):
        #~ print '>'*10,'group ',statement
        result = []
        statement = list(statement)
        st_group = ''
        if statement[0] == 'GROUP':
            
            if type(statement[1]) is str :
                st_group = statement[1]
            elif type(statement[1]) is tuple :
                st_group = statement[1][0]
            
            # en caso de tratarce de un rango, reemplaza el : por -
            if st_group.find(':') != -1:
                st_group = st_group.replace(':','-')
            
            elements = st_group.split(',') # separa los elementos            
            # si es una expresion OR
            if OR :
                result.append('[(%s)]' % '|'.join(elements))
                return ''.join(result)
                
            if len(elements) > 1 :
                # por cada elemento itera y va generando la regexp correspondiente
                result.append('[') # parentesis de inicio del grupo
                for element in elements :
                    if len(element) == 1 :
                        print 'len 1>',element, self.metacharacters 
                        # si el catacter actual es un metacaracter
                        # le antepone la barra invertida 
                        result.append(
                            ('\%s' % element) 
                                if element in self.metacharacters 
                                    else '%s' % element)
                    else:
                        print 'len > 1 -->',element
                        result.append(
                            ('%s' % element)
                                if element.find('-') != -1
                                    else ('(%s)' % element))
                result.append(']') # parentesis de cierre del grupo
            else:
                if len(elements[0]) == 1 :
                    result.append(
                        ('\%s' % elements[0]) 
                            if elements[0] in self.metacharacters
                                else elements[0])
                else:
                    result.append('[%s]' % elements[0])
            
            # en caso de que al grupo se le aplique alguna
            # de las siguientes funciones
            cases = {
                'COUNT'   : self.analize_group_count,
                'EXCLUDE' : self.analize_group_exclude
            }
            if type(statement[1]) is tuple:
                result.append(
                    cases[ statement[1][1][0] ]( statement[1][1] )
                )
                return '(%s)' % ''.join(result)
            return ''.join(result)
            
    def analize_group_count(self, statement):
        quantifiers = {
            'ZEROORMORE':r'*',
            'ZEROORONE':r'?',
            'ONEORMORE':r'+'
        }
        if statement[0] == 'COUNT' :
            # en caso de contener un indice simple
            if (statement[1].find(':') == -1) and \
                (statement[1].find('OR') == -1):
                return '{%s}' % statement[1]
            # en caso de contener un indice tipo rango
            elif (statement[1].find(':') != -1) and \
                (statement[1].find('OR') == -1):
                return '{%s}' % statement[1].replace(':',',')
            # en caso de contener un cuantificador
            elif (statement[1].find(':') == -1) and \
                (statement[1].find('OR') != -1):
                return quantifiers[statement[1]]
                    
    def analize_group_exclude(self, statement):
        pass
        
    def analize_or(self, statement):        
        if statement[0] == 'OR':
            if statement[1][0] == 'GROUP' :
                return self.analize_group(statement[1], OR = True)
                
    def analize_not(self, statement):
        result_not = ''
        if statement[0] == 'NOT':
            if statement[1][0] == 'GROUP' :
                result_not = self.analize_group(statement[1])
        if result_not :
            result_not = result_not[0] + '^' + result_not[1:]
        return result_not
        
    def analize_regexp(self, statement) :
        return statement[1]
        
    # Erase the current program
    def new(self):
         self.prog = {}
 

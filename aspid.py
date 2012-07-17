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
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import aspid_lex
import aspid_parse
import aspid_interp

if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = aspid_parse.parse(data)
    #~ print 'exit prog>',prog
    if not prog: raise SystemExit
    if prog != 1 :
        aspid = aspid_interp.AspidInterpreter(prog)
        try:
            print 'ASPID result> ', aspid.run()
            raise SystemExit
        except RuntimeError:
            pass
#~ 
#~ else:
    #~ aspid = aspid_interp.AspidInterpreter({})
#~ else:
    #~ while 1:
        #~ try:
            #~ line = raw_input("[ASPID] ")    
        #~ except EOFError:
            #~ raise SystemExit
        #~ if not line: continue
        #~ line += "\n"
        #~ prog = aspid_parse.parse(line)
        #~ print prog

def run(data):
    prog = aspid_parse.parse(data)
    if prog != 1 :
        aspid = aspid_interp.AspidInterpreter(prog)
        try:
            return aspid.run()
        except RuntimeError:
            return 1
    return 1


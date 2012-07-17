Aspid
=====

Simple language for create Regular Expressions.

Introduction
------------
When we are facing to the task of writing regular expressions, the traditional wayis very complex and requires extensive previous study.
Aspid arises from the need to create regular expressions in a simple, short and fast way.

The idea is to specify the rules that will have the pattern and, as a result, get a regular expression.

Technical features
------------
Aspid uses `PLY`_ 3.4 (PLY is a pure-Python implementation of the popular compiler construction tools lex and yacc.).
Download `here`_ a last version.

Example to use
------------

Suppose we want generate the regular expression to validate an email. 
The code should be like this: ::

[a:z,0:9,_,.,-].COUNT(ONEORMORE)
[@]
[0:9,a:z,.,-].COUNT(ONEORMORE)
[.]
[a:z,.].COUNT(2:6)

This generate the next regular expression: ::

([a-z0-9_\.-]+)@([0-9a-z\.-]+)\.([a-z\.]{2,6})

To use the example, run it as follows:

   % python aspid.py sample.aspid
   
Documentation
------------
Here a first version of documentation, available in `Spanish`_.

.. _PLY: http://www.dabeaz.com/ply/
.. _here: http://www.dabeaz.com/ply/ply-3.4.tar.gz
.. _Spanish: http://db.tt/oVfWrNp5

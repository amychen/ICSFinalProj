#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:30:18 2017

@author: xijiaqi1997
"""

import string



def cipher(c,offset):
    if c in string.ascii_lowercase:
        if ord(c) + offset <= 122:
            return chr( ord(c) + offset )
        else:
            return chr( ord(c) + offset - 26 )
    elif c in string.ascii_uppercase:
        if ord(c) + offset <= 90:
            return chr( ord(c) + offset )
        else:
            return chr( ord(c) + offset - 26 )
    else:
        return c

def encryption(s,A_private,B_public,p):
    comb = (B_public**A_private)%p
    str_list = []
    l = len(s)
    if l%8 != 0:
        s = s + '0'*((l//8+1)*8-l)
    l = len(s)
    for i in range(0,l-7,8):
        str_list.append(s[i:i+8])
    update = []
    for i in range(len(str_list)):
        try:
            if i+comb < len(str_list) - 1:
                update.append(str_list[i+comb])
            else:
                update.append(str_list[i+comb-(len(str_list))])
        except:
            update = str_list
            break
    for i in range(len(update)):
        temp = ''
        for char in update[i]:
            temp += cipher(char,comb)
        update[i] = temp
    return ''.join(update)

    
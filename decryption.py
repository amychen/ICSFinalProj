#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 22:46:39 2017

@author: xijiaqi1997
"""

import string

def decipher(c,uppset):
    if c in string.ascii_lowercase:
        if ord(c) - uppset >= 97:
            return chr( ord(c) - uppset )
        else:
            return chr( ord(c) - uppset + 26 )
    elif c in string.ascii_uppercase:
        if ord(c) - uppset >= 65:
            return chr( ord(c) - uppset )
        else:
            return chr( ord(c) - uppset + 26 )
    else:
        return c

def decryption(s,B_private,A_public,p):
    comb = (A_public**B_private)%p
    str_list = []
    l = len(s)
    for i in range(0,l-7,8):
        str_list.append(s[i:i+8])
    update = []
    for i in range(len(str_list)):
        if i-comb >= 0:
            update.append(str_list[i-comb])
        elif i-comb+len(str_list) >= 0:
            update.append(str_list[i-comb+(len(str_list))])
        else:
            update = str_list
            break
    for i in range(len(update)):
        temp = ''
        for char in update[i]:
            temp += decipher(char,comb)
        update[i] = temp
    return ''.join(update).strip('0')
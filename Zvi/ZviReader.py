#!/usr/bin/env python
# coding: utf-8

import olefile

class ZviReader(olefile.OleFileIO):

    pass

file = "C:/Users/Anthony/Documents/file.zvi"

if olefile.isOleFile(file):

    reader = ZviReader(file)
    print(reader.listdir())
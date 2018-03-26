# /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

doc_root = os.getcwd()

ignore_files = [
    '^\..*',
    'book.json',
    'GLOSSARY.md',
    'SUMMARY.md',
    'README.md'
]

ignore_dirs = [
    'style',
    'node_modules',
    '^[^a-zA-Z0-9]'
]

SUMMARY = []

class Doc(object):
    def __init__(self, path, level=0):
        self.root = path
        self.children = os.listdir(self.root)
        self.name = self.get_name() if self.get_name() else os.path.basename(self.root)
        self.level = level
        self.files = filter(
            lambda f: f if not len(list(filter(lambda p: p if re.compile(p).match(f) else None, ignore_files))) else None,
            filter(lambda f:f if os.path.isfile(os.path.join(self.root,f)) else None, self.children)
        )
        self.subdirs = []

        self.start()

    def start(self):
        for dir in filter(
            lambda d: d if not len(list(filter(lambda p: p if re.compile(p).match(d) else None, ignore_dirs))) else None,
            filter(lambda d:d if os.path.isdir(os.path.join(self.root,d)) else None, self.children)
        ):
            self.subdirs.append(Doc(os.path.join(self.root,dir), self.level+1))

    def get_name(self):
        readme = os.path.join(self.root, 'README.md')
        if os.path.isfile(readme):
            with open(readme, 'r') as fp:
                first_line = fp.readline()

            p = './*name\s*:\s*(?P<dname>.*).\s*-->*'

            try:
                dname = re.search(p , first_line).groupdict()['dname']
                return dname
            except:
                return None
                pass

    def walk(self):
        if self.level > 0:
            SUMMARY.append((self.level -1 ) * 2 * ' ' + '* ' + '[{}]({})'.format(self.name, os.path.join(self.root.replace(doc_root, '')[1:], 'README.md')))

        for file in self.files:
            if self.level > 0:
                SUMMARY.append((self.level + 1) * 2 * ' ' + '* ' + '[{}]({})'.format(file, os.path.join(self.root.replace(doc_root, '')[1:], file)))
            else:
                SUMMARY.append('* ' + '[{}]({})'.format(file, file))
        for subdir in self.subdirs:
            subdir.walk()

class file(object):
    def __init__(self):
        self.level = 0
        self.name = ''
        self.link = ''


doc = Doc(os.getcwd())
doc.walk()

with open(os.path.join(doc_root, 'SUMMARY.md'), 'w') as fp:
    fp.write('* [Introduction](README.md)\n')
    fp.write('\n'.join(SUMMARY))
    fp.close()
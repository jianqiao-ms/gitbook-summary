# /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

doc_root = os.getcwd()
# doc_root = '/home/jianqiao/Workspace/shangwei.gitlab.shangweiec.com'
os.chdir(doc_root)

ignore_files = [
    '^\..*',
    'book.json',
    'GLOSSARY.md',
    'SUMMARY.md',
    'README.md'
]

ignore_dirs = [
    'etc',
    'style',
    'node_modules',
    '^[^a-zA-Z0-9]'
]

SUMMARY = []

class Doc(object):
    def __init__(self, path, level=0):
        self.root = path
        self.children = os.listdir(self.root)
        self.basename = self.root.replace(doc_root, '')[1:]
        self.name = self.get_name() if self.get_name() else self.basename
        self.link = os.path.join(self.root.replace(doc_root, '')[1:], 'README.md')
        self.level = level
        self.files = []
        self.subdirs = []

        self.start()

    def start(self):
        for file in filter(
            lambda f: f if not len(list(filter(lambda p: p if re.compile(p).match(f) else None, ignore_files))) else None,
            filter(lambda f:f if os.path.isfile(os.path.join(self.root,f)) else None, self.children)
        ):
            self.files.append(File(self.basename, file, self.level))

        for dir in filter(
            lambda d: d if not len(list(filter(lambda p: p if re.compile(p).match(d) else None, ignore_dirs))) else None,
            filter(lambda d:d if os.path.isdir(os.path.join(self.root,d)) else None, self.children)
        ):
            self.subdirs.append(Doc(os.path.join(self.root,dir), self.level+1))



    def get_name(self):
        p = '.*name\s*:\s*(?P<dname>.*)\s*-->*'
        readme = os.path.join(self.root, 'README.md')
        if os.path.isfile(readme):
            with open(readme, 'r') as fp:
                first_line = fp.readline()

            try:
                dname = re.search(p , first_line).groupdict()['dname']
                return dname
            except:
                return None
                pass

    def walk(self):
        SUMMARY.append((self.level-1) * 2 * ' ' + '* ' + '[{}]({})'.format(self.name, self.link, 'README.md'))

        for file in self.files:
            if file.level > 0:
                SUMMARY.append((file.level ) * 2 * ' ' + '* ' + '[{}]({})'.format(file.name, file.link))
            else:
                SUMMARY.append('* ' + '[{}]({})'.format(file.name, file.link))
        for subdir in self.subdirs:
            subdir.walk()

class File(object):
    def __init__(self, path, filename, level):
        self.level = level
        self.link = os.path.join(path, filename)
        self.name = self.get_name() if self.get_name() else filename

    def get_name(self):
        p = '.*name\s*:\s*(?P<fname>.*)\s*-->*'
        with open(self.link, 'r') as fp:
            first_line = fp.readline()

        try:
            fname = re.search(p, first_line).groupdict()['fname']
            return fname
        except:
            return None
            pass


doc = Doc(os.getcwd())
doc.walk()

with open(os.path.join(doc_root, 'SUMMARY.md'), 'w') as fp:
    fp.write('* [Introduction](README.md)\n')
    fp.write('\n'.join(SUMMARY))
    fp.close()
import os
import re

os.chdir('/home/jianqiao/Workspace/shangwei.gitlab.shangweiec.com')
doc_root = os.getcwd()

ignore_files = [
    '^\..*',
    'book.json',
    'SUMMARY.md',
    'README.md'
]

ignore_dirs = [
    'node_modules',
    '^[^a-zA-Z0-9]'
]


class Doc(object):
    def __init__(self, path):
        self.root = path
        self.children = os.listdir(self.root)
        self.name = self.get_name() if self.get_name() else None
        self.level = 0
        self.files = []
        self.subdirs = []

        self.start()

    def start(self):


        self.files = self.get_files()

        for dir in self.get_subdirs():
            self.subdirs.append(Doc(os.path.join(self.root,dir)))

        for dir in self.subdirs:
            dir.start()



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


    def get_files(self):
        def file_filter(file):
            for p in ignore_files:
                if re.compile(p).match(file):
                    return None
            return file

        return list(filter(file_filter, list(filter(lambda x: x if os.path.isfile(os.path.join(self.root, x)) else None, self.children))))

    def get_subdirs(self):
        def dir_filter(dir):
            for p in ignore_dirs:
                if re.compile(p).match(dir):
                    return None
            return dir

        return list(filter(dir_filter, list(filter(lambda x: x if os.path.isdir(os.path.join(self.root, x)) else None, self.children))))

    def walk(self):
        for file in self.files:
            print(file)
        for subdir in self.subdirs:
            subdir.walk()

class file(object):
    def __init__(self):
        self.level = 0
        self.name = ''
        self.link = ''


doc = Doc(os.getcwd())
doc.start()
doc.walk()




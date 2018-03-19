import os
import re

os.chdir('/home/jianqiao/Workspace/test')
doc_root = os.getcwd()


class Doc(object):
    def __init__(self, path):
        self.root = path
        self.children = os.listdir(self.root)
        self.name = os.path.basename(path) if path.replace(doc_root, '') else 'root'
        self.level =  0
        self.files = []
        self.subdirs = []

        self.start()

    def start(self):
        if self.name != 'root':
            self.level += 1

        print('level : ' + str(self.level))
        print(self.root)
        print(self.name)

        self.files = self.get_files()
        subdirs = self.get_subdirs()



        print(self.files)
        print(subdirs)
        print('========================\n\n\n')

        for dir in subdirs:
            self.subdirs.append(Doc(os.path.join(self.root,dir)))


            # print(self.files)
            # print(self.subdirs)
            # print('==================\n\n')

    def get_files(self):
        r = []
        for f in self.children:
            if os.path.isfile(os.path.join(self.root, f)):
                r.append(f)
        # return list(filter(lambda x: x if os.path.isfile(x) else None, os.listdir(self.root)))
        return r

    def get_subdirs(self):
        r = []
        for f in self.children:
            if os.path.isdir(os.path.join(self.root, f)):
                r.append(f)
        # return list(filter(lambda x: x if os.path.isfile(x) else None, os.listdir(self.root)))
        return r

        # return list(filter(lambda x: x if not os.path.isfile(x) else None, os.listdir(self.root)))

    def walk(self):
        for file in self.files:
            print( self.level * '*' + file )
        for subdir in self.subdirs:
            subdir.walk()




doc = Doc(doc_root)
# print(doc.root)
# doc.start()

# for s in doc.subdirs:
#     s.start()
# doc.walk()

# print(doc.files)
# print(doc.subdirs)


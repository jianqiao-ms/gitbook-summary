import os
import re

content = []

ignore_files = [
    'boos.json',
    'SUMMARY.md',
]

ignore_dirs = [
    'node_modules',
    '^[^a-zA-Z0-9]'
]

def list_files(startpath):

    for root, dirs, files in os.walk(startpath):

        basename = root.replace(startpath, '')

        if basename:
            if not re.compile('[a-zA-Z0-9]').match(basename[0]):
                continue

        level = basename.count(os.sep) + 1

        if level != 0 :
            line = (level - 1)*2*' ' + '*' + ' ' + '[' + os.path.basename(root) + ']' + '('+ os.path.basename(root) +'/README.md )'
            content.append(line)

        for f in files:

            if not re.compile('[a-zA-Z0-9]').match(os.path.basename(f)[0]):
                continue

            if f == 'README.md':
                continue

            line = level*2*' ' + '*' + ' ' + '[' + f +']' + '('+basename+'/' + f  +' )'
            content.append(line)




def list_files(startpath):
    for root, dirs, files in os.walk(startpath):

        basename = root.replace(startpath, '')[1:]


        if basename:
            ignore = False
            for r in ignore_dirs:
                if re.compile(r).match(basename):
                    ignore = True
                    break
            if ignore == True:
               continue
            print(basename)

list_files('/home/jianqiao/Workspace/shangwei.gitlab.shangweiec.com')
# list_files('/home/jianqiao/Workspace/test')


# for line in content:
#     print(line)

fp = open(os.path.join('/home/jianqiao/Workspace/shangwei.gitlab.shangweiec.com','SUMMARY.md'), 'w')
for line in content:
    fp.write(line)
    fp.write('\n')
fp.close()

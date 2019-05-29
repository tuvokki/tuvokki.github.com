import os
with os.scandir('_posts') as entries:
    for entry in entries:
        with open(f'_posts/{entry.name}') as file, open(f'content/{entry.name[11:]}', 'w') as writer:
            # print('==========================================================')
            writer.write(f'Title: {entry.name[11:][:-3]}\n')
            writer.write(f'Date: {entry.name[:10]} 0:00\n')
            writer.write('Category: Old\n\n')
            # print('==========================================================')
            # print(file.readline(3))
            # print(file.readlines())
            # print(file.read())
            line = file.readline()
            line = file.readline()
            while line != '---\n':
                line = file.readline()
            for wline in file.readlines():
                writer.write(wline)

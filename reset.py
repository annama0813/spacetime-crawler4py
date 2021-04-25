# Quickly deletes all crawled files

import os

def delete_file(name):
    if os.path.exists(name):
        os.remove(name)
    else:
        print("The file does not exist")

file_names = ['frontier.shelve', 'longestpage.txt', 'content.txt', 'url.txt']
for name in file_names:
    delete_file(name)

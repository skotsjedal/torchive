import os
import rarfile
from archive import *


class Rar:
    def __init__(self, folder):
        self.folder = folder
        self.folder_name = folder[folder.rindex("/")+1:]
        self.archives = []
        self.parse_folder()

    def parse_folder(self):
        print "parsing", self.folder
        for fil in os.listdir(self.folder):
            if fil[-3:] == "rar":
                newarch = Arch(os.path.join(self.folder, fil))
                self.archives.append(newarch)

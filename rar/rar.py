import os
from archive import Arch


class Rar:
    def __init__(self, folder):
        self.folder = folder
        self.folder_name = folder[folder.rindex("/")+1:]
        self.archives = []
        self.parse_folder(self.folder)

    def parse_folder(self, folder):
        print "parsing", folder
        for fil in os.listdir(folder):
            if fil[-3:] == "rar":
                newarch = Arch(os.path.join(self.folder, fil))
                self.archives.append(newarch)
            elif os.path.isdir(fil):
                self.parse_folder(fil)
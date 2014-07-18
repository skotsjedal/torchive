import os
from archive import Arch


class Rar:
    def __init__(self, folder):
        self.folder = folder
        self.folder_name = folder[folder.rindex("/")+1:]
        self.archives = []
        self.parse_folder(self.folder)

    def parse_folder(self, folder):
        print "folderparse", folder
        for fil in os.listdir(folder):
            fullpath = os.path.join(folder, fil)
            if fil[-4:] == ".rar":
                newarch = Arch(fullpath)
                self.archives.append(newarch)
            elif os.path.isdir(fullpath):
                self.parse_folder(fullpath)

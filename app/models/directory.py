from config_local import Config
from os import walk
from os.path import dirname, abspath, realpath


class FileSystemItem(object):
    def __init__(self, display_name: str):
        if not type(display_name) is str:
            raise Exception(f"Expected str, got {type(display_name)}")
        self.display_name = display_name
        self.full_path = display_name
        self.is_directory = None


class DirectoryStub(FileSystemItem):
    def __init__(self, directory: str, parent_directory: str = None):

        if directory is None or directory == '':
            self.directory = realpath(Config.ROOT_DIRECTORY)
        else:
            self.directory = directory

        super().__init__(self.directory)
        if parent_directory is None:
            self.parent_path = dirname(self.directory)
        else:
            self.parent_path = parent_directory

        self.full_path = realpath(self.parent_path + '/' + self.directory)
        self.num_children = 0
        self.is_directory = True

    def __str__(self):
        return f"d:{self.display_name} ({self.num_children})"

    def __repr__(self):
        return f"<DirectoryStub '{self.display_name}'>"


class File(FileSystemItem):
    def __init__(self, filename: str, directory: str):
        self.filename = filename
        super().__init__(self.filename)
        self.is_directory = False
        self.parent_path = directory
        self.full_path = realpath(self.parent_path + '/' + self.filename)
    
    def __str__(self):
        return self.display_name

    def __repr__(self):
        return f"<File '{self.display_name}'>"


class Directory(DirectoryStub):
    def __init__(self, directory: str):
        super().__init__(Config.ROOT_DIRECTORY + directory)
        self.contents = self.__get_contents()
        self.options = self.__get_options()

    def __get_contents(self):
        basedir = Config.ROOT_DIRECTORY
        files = []
        dirs_dict = {}
        depth = 0
        for (dirpath, dirnames, filenames) in walk(realpath(basedir + self.directory)):
            for d in dirnames:
                if d == '.basic-file-browser' or d == '.' or d == '..':
                    continue
                if depth == 0:
                    dirs_dict[realpath(dirpath + '/' + d)] = DirectoryStub(d, dirpath)
                else:
                    dirs_dict[realpath(dirpath)].num_children += 1
            for f in filenames:
                if depth == 0:
                    files.append(File(f, dirpath))
                else:
                    dirs_dict[realpath(dirpath)].num_children += 1
            if depth == 1:
                break
            depth += 1
        directories = sorted(
            (d for (_, d) in dirs_dict.items()),
            key=lambda fs: fs.display_name.lower()
        )
        files = sorted(
            files,
            key=lambda fs: fs.display_name.lower()
        )
        return directories + files

    def __get_options(self):
        pass

    def __repr__(self):
        return f"<Directory '{self.display_name}'>"

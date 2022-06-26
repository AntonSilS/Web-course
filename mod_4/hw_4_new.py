from abc import ABC, abstractmethod
from threading import Thread
import os, re, shutil, sys


class ReturnValueThread(Thread):
    def __init__(self, group=None, target=None, name=None, 
                 args=(), kwargs={}, verbose=None):
        super().__init__(group, target, name, args, kwargs)
        self.value = None

    def run(self):
        if self._target is not None:
            self.value = self._target(*self._args)

    def join (self, *args):
        Thread.join(self,*args)
        return self.value


class Normolizible(ABC):
    def __init__(self):
        self.CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        self.TRANS = {}
        self.TRANSLATION = (
                            "a", "b", "v", "g", "d", "e", "e", "j",
                            "z", "i", "j", "k", "l", "m", "n", "o",
                            "p", "r", "s", "t", "u", "f", "h", "ts",
                            "ch", "sh", "sch", "", "y", "", "e", "yu",
                            "u", "ja", "je", "ji", "g"
                            )


    def name_translateration(self, name):
        clear_name = re.sub(r"\W", "_", name)
        if re.search(r"[а-яА-ЯёЁ]", name):
            for c, l in zip(tuple(self.CYRILLIC_SYMBOLS), self.TRANSLATION):
                self.TRANS[ord(c)] = l
                self.TRANS[ord(c.upper())] = l.upper()
            clear_name = clear_name.translate(self.TRANS)
        return clear_name


class Extension: 
    def __init__(self, name):
        self.name = name
        if name.startswith("."):
            self.name = name.replace('.', '')
        self.dict_extentions =  {
                                'image': ['jpg', 'png', 'jpeg','svg'],
                                'video': ['avi', 'mp4' 'mov', 'mkv'],
                                'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
                                'audio': ['mp3', 'ogg', 'wav', 'amr'],
                                'archive': ['zip', 'gz', 'tar']
                                }
        
        category = [k for k, v in self.dict_extentions.items() if self.name in v]
        if category:
            self.category = category[0]
        else:
            self.category = 'other'

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name


class UserPath:
    def __init__(self, path):
        self._path = None
        self.path = path
        self.empthy_folder_tree = []
    
    def __str__(self):
        return self.path
    
    def __repr__(self):
        return self.path
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        if os.path.exists(path):
            self._path = path
        else:
            raise Exception("Such path doesn't exist!!")
    def remove_path(self):
        os.rmdir(self.path)


class Unzipped:
    def unpzip_archive(self, path, extraction_dir):
        shutil.unpack_archive(path, extraction_dir)


@abstractmethod
class File(Normolizible, Unzipped):
    def __init__(self, path):
        Normolizible().__init__()
        self.path = path
        self.root_dir, self.fullname = os.path.split(str(self.path))
        self.filename, extention = os.path.splitext(self.fullname)
        self.extention = Extension(extention)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return str(self.path)
    
    def name_translateration(self):
        norm_name = Normolizible().name_translateration(self.filename)
        new_full_path = os.path.join(self.root_dir,norm_name+"."+ self.extention.name)
        os.replace(str(self.path), new_full_path)
        self.path.path = new_full_path
        self.__init__(self.path)
    
    def remove(self):
        self.path.remove_path()

    def unpzip_archive(self):
        extraction_dir = os.path.join(self.root_dir, self.filename)
        super().unpzip_archive(str(self.path), extraction_dir)
        unpack_name_file = [x for x in os.listdir(extraction_dir) if x != '__MACOSX']
        new_file_path = os.path.join(extraction_dir, unpack_name_file[0])
        old_path = self.path.path
        self.path.path = new_file_path
        self.__init__(self.path)
        os.remove(old_path)
        
        
class Folder:
    def __init__(self, path):
        self.path = path
        self.root_dir, self.fullname = os.path.split(str(self.path))

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return str(self.path)

    def remove(self):
        self.path.remove_path()


class Catalog:
    def __init__(self, path):
        self.path = path

    def get_tree(self, dir = None):
        tree = []
        if dir == None:
            dir = self.path
        for filename in os.listdir(dir.path):
            filename_path = os.path.join(dir.path, filename)
            if '.DS_Store' in filename_path:
                os.remove(filename_path)
                continue
            if os.path.isdir(filename_path):
                if os.listdir(filename_path):
                    obj_path = UserPath(filename_path)
                    cus_thread = ReturnValueThread(target=self.get_tree, args=(obj_path,))
                    cus_thread.start()
                    tree += cus_thread.join()
                else: 
                    folder_path = UserPath(filename_path)
                    folder = Folder(folder_path)
                    folder.empty = None
                    tree.append(folder)
            else:
                file_path = UserPath(filename_path)
                tree.append(File(file_path))
        return tree
    
    def remove_file(self, obj):
        obj.remove()
        del obj
     
    def remove_empty_folder(self):
        
        while True:
            if list(filter(lambda x: hasattr(x, 'empty'),  self.get_tree())):
                for obj in self.get_tree():
                    if hasattr(obj, 'empty'):
                        self.remove_file(obj)
            else:
                break

    def sorts_files(self):
        list_known_exten = set()
        list_unknown_exten = set()
        tree = self.get_tree(self.path)
        for obj in tree:
            if isinstance(obj, File):
                folder_category = os.path.join(str(self.path), obj.extention.category)
                if not os.path.exists(folder_category):
                   os.mkdir(folder_category)
                obj.name_translateration()
                new_file_path = os.path.join(folder_category, obj.fullname)
                if not os.path.exists(new_file_path):
                    os.replace(str(obj.path), new_file_path)
                    obj.path.path = new_file_path
                    obj.__init__(obj.path)
                if obj.extention.category == 'other':
                    if obj.extention.name:
                        list_unknown_exten.add(obj.extention.name)
                else:
                    list_known_exten.add(obj.extention.name)
                if obj.extention.category == 'archive':
                    obj.unpzip_archive()
                    obj.name_translateration()
  
        print(f'Known extetnion: {list_known_exten}\n')
        print(f'Unknown extetnion: {list_unknown_exten}\n')
  

if __name__ == "__main__":
    try:
        path = sys.argv[1]

    except IndexError:

        path = input("Write please your path: ")

    user_path = UserPath(path)
    catalog = Catalog(user_path)
    catalog.sorts_files()
    catalog.remove_empty_folder()
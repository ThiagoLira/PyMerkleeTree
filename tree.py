import hashlib
from pathlib import Path
from os import listdir
from os.path import isfile, join

BUF_SIZE = 65536

def HASH_FILE(file_path: str):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def HASH_HASH(hash: str):
    return hashlib.sha1(hash.encode()).hexdigest()

class LeafNode:
    def __init__(self, file_path):
        self.children = []
        self.file_path = file_path
        self.hash = None

class DataNode:
    def __init__(self,file_path):
        self.file_path = file_path 
        self.hash = HASH_FILE(file_path) 
        
class MerkleTree:
    def __init__(self, path):
        assert(Path(path).exists())
        self.root = LeafNode(str(path))
        self._add_folder(self.root,path)
        self.root.hash = HASH_HASH(''.join([c.hash for c in self.root.children]))

    def _add_folder(self,node,path):
        for f in listdir(path): 
            full_path = join(path,f)
            is_file = isfile(full_path)
            if (is_file):
                f_node = DataNode(str(full_path))
                node.children.append(f_node)
            else:
                dir_node = LeafNode(str(full_path))
                node.children.append(dir_node)
                self._add_folder(dir_node,full_path)
                # when the first folder gets to this point we know it doesn't have any
                # hashes uncalculated
                dir_node.hash = HASH_HASH(''.join([c.hash for c in dir_node.children]))


    def validate_file(self,file_path: str):
        assert(Path(file_path).exists(),'invalid file')
        hash = HASH_FILE(file_path)
        ## TODO validate file path is inside the tree
        # get position of file in tree
        for f in listdir(self.root.file_path):
            full_path = join(self.root.file_path,f)
            if (full_path == file_path):
                pass

    def print_tree(self):
        print(self.root.file_path,self.root.hash)
        self._print_node(self.root)
        
    def _print_node(self,node):
        for c in node.children:
            if isinstance(c,DataNode):
                print(c.file_path,c.hash)
                break
            else:
                print(c.file_path,c.hash)
                self._print_node(c)
        
if __name__=='__main__':
    t = MerkleTree(Path.cwd())
    t.print_tree()
    t.validate_file(str(Path.cwd() / 'tree.py'))
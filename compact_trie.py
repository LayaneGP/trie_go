import math
class TrieNode:

    #armazena posting list completa e mu, sigma.
    def __init__(self, label=""):
        self.label = label
        self.children = {}
        self.is_word = False
        self.doc_ids = {}
        self.stats = {'mu': 0.0, 'sigma': 0.0}
    def __repr__(self):
        return f"TrieNode(label='{self.label}', word={self.is_word}, docs={len(self.doc_ids)})"

class TrieCompacta:

    def __init__(self):

        self.root = TrieNode()

    def insert(self, word, doc_id, frequency=1):
        node = self.root
        i = 0
        word = word.lower()
        while i < len(word):
            first_char = word[i]
            if first_char in node.children:
                child = node.children[first_char]
                label = child.label
                #encontra prefixo comum
                j = 0
                while j < len(label) and i + j < len(word) and word[i + j] == label[j]:
                    j += 1
                if j == len(label):
                    node = child
                    i += j
                elif j > 0:
                    # dividir no   
                # cria no do prefixo comum
                    split_node = TrieNode(label[:j])
                    split_node.children = {label[j]: child}
                    # atualiza
                    child.label = label[j:]
                    if split_node.is_word:
                        split_node.doc_ids = split_node.doc_ids.copy()

                        split_node.stats = split_node.stats.copy()
                    node.children[first_char] = split_node
                    node = split_node
                    if i + j == len(word):
                        node.is_word = True
                        node.doc_ids[doc_id] = node.doc_ids.get(doc_id, 0) + frequency
                        return        
                    new_suffix = word[i + j:]
                    new_node = TrieNode(new_suffix)
                    new_node.is_word = True
                    new_node.doc_ids[doc_id] = frequency
                    node.children[new_suffix[0]] = new_node
                    return
                else:
                    #se nao tem prefixo em comum
                    i += 1

            else:
                new_node = TrieNode(word[i:])
                new_node.is_word = True
                new_node.doc_ids[doc_id] = frequency
                node.children[first_char] = new_node
                return
        node.is_word = True
        node.doc_ids[doc_id] = node.doc_ids.get(doc_id, 0) + frequency
    def search(self, word):
        node = self.root
        i = 0
        word = word.lower()
        while i < len(word):
            first_char = word[i]
            if first_char not in node.children:
                return None, None

            child = node.children[first_char]
            label = child.label
        
            if word[i:i + len(label)] != label:
                return None, None
    
            node = child
            i += len(label)
            
        if node.is_word:
            return node.doc_ids, node.stats

        return None, None
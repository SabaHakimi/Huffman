from __future__ import annotations
from typing import List, Optional
from os.path import exists

class HuffmanNode:
    def __init__(self, char_ascii: int, freq: int, left: Optional[HuffmanNode] = None, right: Optional[HuffmanNode] = None):
        self.char_ascii = char_ascii    # stored as an integer - the ASCII character code value
        self.freq = freq                # the frequency associated with the node
        self.left = left                # Huffman tree (node) to the left!
        self.right = right              # Huffman tree (node) to the right

    def __lt__(self, other: HuffmanNode) -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    if a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            return True
        return False
    return False

def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""
    if comes_before(a, b):
        temp = HuffmanNode(min(a.char_ascii, b.char_ascii), a.freq + b.freq, a, b)
    else:
        temp = HuffmanNode(min(a.char_ascii, b.char_ascii), a.freq + b. freq, b, a)
    return temp

def cnt_freq(filename: str) -> List:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    freq_list = [0]*256
    t = open(filename)
    text = t.read()
    for c in text:
        freq_list[ord(c)] += 1
    t.close()
    return freq_list

def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    huff_list = []
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            huff_list.append(HuffmanNode(i, char_freq[i]))
    while len(huff_list) > 1:
        insertion_sort(huff_list)
        min1 = huff_list.pop(0)
        min2 = huff_list.pop(0)
        huff_list.append(combine(min1, min2))
    if huff_list == []:
        return None
    return huff_list[0]

def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    code_list = [""] * 256
    huffman_tree_traversal(node, "", code_list)
    return code_list

def huffman_tree_traversal(tnode: HuffmanNode, code: str, arr: list) -> None:
    """Helper function for create_code function; recursively traverses the huffman tree, adding a 0 when traversing
    left and a 1 when traversing right."""
    if tnode.left is not None:
        huffman_tree_traversal(tnode.left, code + "0", arr)
    if tnode.right is not None:
        huffman_tree_traversal(tnode.right, code + "1", arr)
    if arr[tnode.char_ascii] == "":
        arr[tnode.char_ascii] = code

def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header_str = ""
    for i in range(len(freqs)):
        if freqs[i] != 0:
            header_str = header_str + str(i) + " " + str(freqs[i]) + " "
    return header_str[:len(header_str) - 1]

def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    # Check if file exists
    if not exists(in_file):
        raise FileNotFoundError
    freq_list = cnt_freq(in_file)
    huff_tree = create_huff_tree(freq_list)
    # If the file is empty
    if huff_tree is None:
        out_f = open(out_file, 'w', newline="")
        out_f.write("")
        out_f.close()
        return
    # If only one unique character
    if huff_tree.left is None and huff_tree.right is None:
        out_f = open(out_file, 'w', newline="")
        out_f.write(create_header(freq_list))
        out_f.close()
        return
    code_list = create_code(huff_tree)
    in_f = open(in_file)
    text = in_f.read()
    out_f = open(out_file, 'w', newline="")
    out_f.write(create_header(freq_list) + "\n")
    for c in text:
        out_f.write(code_list[ord(c)])
    in_f.close()
    out_f.close()

def huffman_decode(encoded_file: str, decode_file: str) -> None:
    """Takes in an input file and decodes it in an output file by first rebuilding the huffman tree used to encode it,
    then traversing the tree until it reaches a leaf node. Upon reaching a leaf node, it takes the char_ascii value of
    that node as a decoded character. Thue huffman tree is repeatedly traversed until every character is decoded."""
    if not exists(encoded_file):
        raise FileNotFoundError
    in_f = open(encoded_file)
    freq_list = parse_header(in_f.readline().rstrip())
    huff_tree = create_huff_tree(freq_list)
    if huff_tree is None:
        out_f = open(decode_file, 'w', newline="")
        out_f.write("")
        out_f.close()
        in_f.close()
        return
    if huff_tree.left is None and huff_tree.right is None:
        out_f = open(decode_file, 'w', newline="")
        output = [chr(huff_tree.char_ascii)] * freq_list[huff_tree.char_ascii]
        output = ''.join(output)
        out_f.write(output)
        out_f.close()
        in_f.close()
        return
    code = in_f.read()
    out_f = open(decode_file, 'w', newline="")
    i = 0
    while i < len(code):
        dec_str = decode_char(code, huff_tree, i)
        out_f.write(dec_str[0])
        i = int(dec_str[1:])
    in_f.close()
    out_f.close()

def decode_char(coded_string: str, tnode: HuffmanNode, char_index: int) -> str:
    """Helper function for huffman_decode function. Recursively traverses the huffman tree to decode one character."""
    if char_index < len(coded_string):
        if int(coded_string[char_index]) == 0 and tnode.left is not None:
            char_index += 1
            return decode_char(coded_string, tnode.left, char_index)
        elif int(coded_string[char_index]) == 1 and tnode.right is not None:
            char_index += 1
            return decode_char(coded_string, tnode.right, char_index)
    ret_str = chr(tnode.char_ascii) + str(char_index)
    return ret_str

def parse_header(header_str: str) -> List:
    """Parses the header to recreate the list of frequencies required to recreate the huffman tree used for encoding,
    in order to decode."""
    freq_list = [0]*256
    token = ""
    i = 0
    while i < len(header_str):
        if header_str[i] != " ":
            token = token + header_str[i]
            i += 1
        else:
            j = i + 1
            cnt = 0
            freq_val = ""
            while j < len(header_str) and header_str[j] != " ":
                freq_val = freq_val + header_str[j]
                cnt += 1
                j += 1
            freq_list[int(token)] = int(freq_val)
            token = ""
            freq_val = ""
            i += (cnt + 2)
    return freq_list

def insertion_sort(alist: list) -> List:
    """Helper function used to sort the list of huffman nodes used in creating the huffman tree."""
    for i in range(1, len(alist)):
        j = i
        while j > 0:
            if comes_before(alist[j], alist[j - 1]):
                alist[j], alist[j - 1] = alist[j - 1], alist[j]
                j -= 1
            else:
                j = 0
    return alist



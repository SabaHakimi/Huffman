import unittest
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self) -> None:
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

        # Test another simple file
        freqlist2 = cnt_freq("file1.txt")
        anslist2 = [4, 3, 2, 1]
        self.assertEqual(freqlist2[97:101], anslist2)
        self.assertEqual(freqlist2[32], 3)

    def test_comes_before(self) -> None:
        # Basic tests for this function
        a = HuffmanNode(97, 4)
        b = HuffmanNode(44, 4)
        c = HuffmanNode(52, 16)
        d = HuffmanNode(101, 1)
        e = HuffmanNode(215, 7)
        self.assertFalse(comes_before(a, b))
        self.assertTrue(comes_before(b, a))
        self.assertTrue(comes_before(b, c))
        self.assertFalse(comes_before(e, d))
        self.assertTrue(comes_before(d, b))

    def test_combine(self) -> None:
        a = HuffmanNode(65, 1)
        b = HuffmanNode(66, 2)
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii,65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:   # pragma: no cover
            self.fail()

        # Test values with same frequency
        a = HuffmanNode(49, 17)
        b = HuffmanNode(122, 17)
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 49)
            self.assertEqual(c.left.freq, 17)
            self.assertEqual(c.right.char_ascii, 122)
            self.assertEqual(c.right.freq, 17)
            self.assertEqual(c.char_ascii, 49)
            self.assertEqual(c.freq, 34)
        else:  # pragma: no cover
            self.fail()
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 49)
            self.assertEqual(c.left.freq, 17)
            self.assertEqual(c.right.char_ascii, 122)
            self.assertEqual(c.right.freq, 17)
            self.assertEqual(c.char_ascii, 49)
            self.assertEqual(c.freq, 34)
        else:  # pragma: no cover
            self.fail()

    def test_insertion_sort(self):
        a = HuffmanNode(97, 4)
        b = HuffmanNode(41, 5)
        c = HuffmanNode(22, 1)
        d = HuffmanNode(199, 7)
        e = HuffmanNode(30, 5)
        tlist = [a, b, c, d, e]
        self.assertEqual(insertion_sort(tlist), [c, a, e, b, d])
        tlist2 = [b, a]
        self.assertEqual(insertion_sort(tlist2), [a, b])
        tlist3 = [d]
        self.assertEqual(insertion_sort(tlist3), [d])
        tlist4 = []
        self.assertEqual(insertion_sort(tlist4), [])

    def test_create_huff_tree(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        if hufftree is not None:
            self.assertEqual(hufftree.freq, 32)
            self.assertEqual(hufftree.char_ascii, 97)
            left = hufftree.left
            right = hufftree.right
            if (left is not None) and (right is not None):
                self.assertEqual(left.freq, 16)
                self.assertEqual(left.char_ascii, 97)
                self.assertEqual(right.freq, 16)
                self.assertEqual(right.char_ascii, 100)
            else: # pragma: no cover
                self.fail()
        else: # pragma: no cover
            self.fail()
        # Test empty freq list
        freqList2 = [0] * 256
        hufftree2 = create_huff_tree(freqList2)
        self.assertEqual(hufftree2, None)
        # Test one item freq list
        freqList3 = [0] * 256
        freqList3[66] = 4
        hufftree3 = create_huff_tree(freqList3)
        self.assertEqual(hufftree3.freq, 4)
        self.assertEqual(hufftree3.char_ascii, 66)
        self.assertEqual(hufftree3.left, None)
        self.assertEqual(hufftree3.right, None)

    def test_create_header(self) -> None:
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self) -> None:
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1_out.txt", "file1_soln.txt"))
        # Test File 2
        huffman_encode("file2.txt", "file2_out.txt")
        self.assertTrue(compare_files("file2_out.txt", "file2_soln.txt"))
        # Another test
        huffman_encode("testfile2.txt", "testfile2_out.txt")
        self.assertTrue(compare_files("testfile2_out.txt", "testfile2_soln.txt"))
        # Test Multiline File
        huffman_encode("multiline.txt", "multiline_out.txt")
        self.assertTrue(compare_files("multiline_out.txt", "multiline_soln.txt"))
        # Test encoding Declaration of Independence
        huffman_encode("declaration.txt", "declaration_out.txt")
        self.assertTrue(compare_files("declaration_out.txt", "declaration_soln.txt"))
        # Test only one unique character
        huffman_encode("testfile1.txt", "testfile1_out.txt")
        self.assertTrue(compare_files("testfile1_out.txt", "testfile1_soln.txt"))
        # Test empty file
        huffman_encode("testempty.txt", "testempty_out.txt")
        self.assertTrue(compare_files("testempty.txt", "testempty_out.txt"))
        # Test no input file
        with self.assertRaises(FileNotFoundError):
            huffman_encode("test404.txt", "test404_out.txt")

    def test_parse_header(self):
        # Simple Test
        file1 = open("file1_soln.txt")
        header = file1.readline().rstrip()
        self.assertEqual(cnt_freq("file1.txt"), parse_header(header))
        file1.close()
        # Thorough Test
        filedec = open("declaration_soln.txt")
        header_dec = filedec.readline().rstrip()
        self.assertEqual(cnt_freq("declaration.txt"), parse_header(header_dec))
        filedec.close()

    def test_huffman_decode(self):
        """Tests both the overarching huffman_decode function and decode_char helper function; decode_char is difficult
        to test outside the context of huffman_decode."""
        # Test file 1
        huffman_decode("file1_soln.txt", "file1_decoded.txt")
        self.assertTrue(compare_files("file1.txt", "file1_decoded.txt"))
        # Test file 2
        huffman_decode("file2_soln.txt", "file2_decoded.txt")
        self.assertTrue(compare_files("file2.txt", "file2_decoded.txt"))
        # Test multiline
        huffman_decode("multiline_soln.txt", "multiline_decoded.txt")
        self.assertTrue(compare_files("multiline.txt", "multiline_decoded.txt"))
        # Test DOI
        huffman_decode("declaration_soln.txt", "declaration_decoded.txt")
        self.assertTrue(compare_files("declaration.txt", "declaration_decoded.txt"))
        # Test Essay
        huffman_encode("test_essay.txt", "test_essay_out.txt")
        huffman_decode("test_essay_out.txt", "test_essay_decoded.txt")
        self.assertTrue(compare_files("test_essay.txt", "test_essay_decoded.txt"))
        # Test one unique char
        huffman_decode("testfile1_soln.txt", "testfile1decoded.txt")
        self.assertTrue(compare_files("testfile1.txt", "testfile1decoded.txt"))
        # Test empty file
        huffman_decode("testempty.txt", "testempty_decoded.txt")
        self.assertTrue(compare_files("testempty.txt", "testempty_decoded.txt"))
        # Test no input file
        with self.assertRaises(FileNotFoundError):
            huffman_decode("test404.txt", "test404_decoded.txt")

# Compare files - takes care of CR/LF, LF issues
def compare_files(file1: str, file2: str) -> bool: # pragma: no cover
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match


if __name__ == '__main__':
    unittest.main()

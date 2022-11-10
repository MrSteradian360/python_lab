import unittest
from ac_DUMA import build, search


class AcTest(unittest.TestCase):
    def test1(self):
        trie = build('abcdef', 'abc', 'def')
        self.assertEqual(sorted(search(trie, "abcdef")),
                         [0, 0, 3])

    def test2(self):
        trie = build('abc', 'aab', 'cba')
        self.assertEqual(sorted(search(trie, "aaabc")),
                         [1, 2])

    def test3(self):
        trie = build('a', 'aaa')
        self.assertEqual(sorted(search(trie, "aaabc")),
                         [0, 0, 1, 2])

    def test4(self):
        trie = build('abcd', 'bc')
        self.assertEqual(sorted(search(trie, "abcd")),
                         [0, 1])

    def test5(self):
        trie = build('ad', 'yt')
        self.assertEqual(sorted(search(trie, "cdftytaddp")),
                         [4, 6])

    def test6(self):
        trie = build('abcd', 'bc')
        self.assertEqual(sorted(search(trie, "abcx")),
                         [1])


if __name__ == '__main__':
    unittest.main()

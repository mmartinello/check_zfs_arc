"""
Unittest for the Icinga Plugin: check_zfs_arc

authors:
    Mattia Martinello - mattia@mattiamartinello.com
"""

import os
import unittest
import check_zfs_arc as checker


class ParserTest(unittest.TestCase):
    def test_get_ram_total_128gb(self):
        check = checker.Checker()
        input_file = 'examples/meminfo_128gb.txt'
        file = open(input_file, mode='r')
        content = file.read()
        file.close()

        ram_total = check._get_ram_total(input_text=content)
        self.assertEqual(ram_total, 134981455872)

    def test_get_ram_total_8gb(self):
        check = checker.Checker()
        input_file = 'examples/meminfo_8gb.txt'
        file = open(input_file, mode='r')
        content = file.read()
        file.close()

        ram_total = check._get_ram_total(input_text=content)
        self.assertEqual(ram_total, 8366292992)

    def test_get_ram_total_32gb(self):
        check = checker.Checker()
        input_file = 'examples/meminfo_32gb.txt'
        file = open(input_file, mode='r')
        content = file.read()
        file.close()

        ram_total = check._get_ram_total(input_text=content)
        self.assertEqual(ram_total, 33672822784)

    def test_get_ram_total_missing(self):
        check = checker.Checker()
        input_file = 'examples/meminfo_missing.txt'
        file = open(input_file, mode='r')
        content = file.read()
        file.close()

        ram_total = check._get_ram_total(input_text=content)
        self.assertIsNone(ram_total)

def test_get_ram_total_missing(self):
        check = checker.Checker()
        input_file = 'examples/meminfo_wrong.txt'
        file = open(input_file, mode='r')
        content = file.read()
        file.close()

        ram_total = check._get_ram_total(input_text=content)
        self.assertIsNone(ram_total)

if __name__ == "__main__":
    unittest.main()

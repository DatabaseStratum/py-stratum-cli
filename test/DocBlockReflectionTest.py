"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import unittest

from pystratum.DocBlockReflection import DocBlockReflection


class DocBlockReflectionTest(unittest.TestCase):
    """
    Unit test for class DocBlockReflection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Test empty DocBlock.
        """
        doc_block = []
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('', description)

        params = reflection.get_tags('param')
        self.assertEqual([], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Test DocBlock with description only and minimal whitespace.
        """
        doc_block = ['/** Hello World */']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual([], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        Test DocBlock with description only and proper whitespace.
        """
        doc_block = ['/**',
                     '  * Hello World',
                     '  */']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual([], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test04(self):
        """
        Test DocBlock with description only and not proper whitespace.
        """
        doc_block = ['  /**',
                     ' * Hello World',
                     '  */  ']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual([], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test10(self):
        """
        Test DocBlock with description and parameters and proper whitespace.
        """
        doc_block = ['/**',
                     ' * Hello World',
                     ' *',
                     ' * @param p1 This is param1.',
                     ' * @param p2 This is param2.',
                     ' */']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual(['@param p1 This is param1.', '@param p2 This is param2.'], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test11(self):
        """
        Test DocBlock with description and parameters and not proper whitespace.
        """
        doc_block = [' /**',
                     ' * Hello World',
                     '',
                     ' ',
                     '   * @param p1  ',
                     '* @param p2 This is param2. ',
                     ' */ ']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual(['@param p1', '@param p2 This is param2.'], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test12(self):
        """
        Test DocBlock with description and parameters and not proper whitespace.
        """
        doc_block = [' /**',
                     ' * Hello World',
                     '   * @param p1  ',
                     '* @param p2 This is param2. ',
                     ' */ ']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World', description)

        params = reflection.get_tags('param')
        self.assertEqual(['@param p1', '@param p2 This is param2.'], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test20(self):
        """
        Test DocBlock without description and parameters with proper whitespace.
        """
        doc_block = ['/**',
                     ' * @param p1 This is param1.',
                     ' * @param p2 This is param2.',
                     ' */']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('', description)

        params = reflection.get_tags('param')
        self.assertEqual(['@param p1 This is param1.', '@param p2 This is param2.'], params)

    # ------------------------------------------------------------------------------------------------------------------
    def test30(self):
        """
        Test DocBlock without description and parameters with proper whitespace.
        """
        doc_block = ['/**',
                     ' * Hello World.',
                     ' * ',
                     ' * @param p1 This is param1.',
                     ' * @param p2 This is param2.',
                     ' *           This is more about param2',
                     ' */']
        reflection = DocBlockReflection(doc_block)

        description = reflection.get_description()
        self.assertEqual('Hello World.', description)

        params = reflection.get_tags('param')
        self.assertEqual(['@param p1 This is param1.', '@param p2 This is param2.\nThis is more about param2'], params)

# ----------------------------------------------------------------------------------------------------------------------

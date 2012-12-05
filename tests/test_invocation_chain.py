import unittest

from vake.invocation_chain import InvocationChain, EMPTY

class TestInvocationChain(unittest.TestCase):
    def setUp(self):
        self.empty = EMPTY
        self.first_member = "A"
        self.second_member = "B"
        self.one = self.empty.append(self.first_member)
        self.two = self.one.append(self.second_member)

    def test_append(self):
        chain = self.empty.append("A")

        self.assertEqual("TOP => A", str(chain))

    def test_chain_repr(self):
        self.assertEqual("TOP", str(self.empty))
        self.assertEqual("TOP => A", str(self.one))
        self.assertEqual("TOP => A => B", str(self.two))

    def test_chain_contains_one(self):
        self.assertTrue(self.first_member in self.one)

    def test_chain_contains_two(self):
        self.assertTrue(self.second_member in self.two)
        self.assertTrue(self.first_member in self.two)

    def test_append_one_circular(self):
        with self.assertRaises(RuntimeError) as context:
            self.one.append(self.first_member);
        ex = context.exception
        self.assertRegex(ex.args[0], r'^Circular dependency detected');
        self.assertRegex(ex.args[0], r'A.*=>.*A');

    def test_append_two_circular(self):
        with self.assertRaises(RuntimeError) as context:
            self.two.append(self.first_member);
        ex = context.exception
        self.assertRegex(ex.args[0], r'A.*=>.*B.*=>.*A')


import unittest
from ...classes import *


class TestAutomat(unittest.TestCase):
    def setUp(self):
        fill_transition_sieve()

    def test_add_transition(self):
        # Test the method add_transition
        a = Automat()
        a.add_transition(0, 1, 'a')
        self.assertTrue(a.state_map[0][1]['a'])

    def test_merge(self):
        # Test the method merge
        a = Automat(1)
        a.add_transition(1, -1, 'a')
        a.capture_groups[1] = set()
        a.capture_groups[1].add((1, -1))
        b = Automat(2)
        b.add_transition(2, -2, 'b')
        b.capture_groups[1] = set()
        b.capture_groups[1].add((2, -2))
        a._merge(b)
        self.assertTrue(a.state_map[1][-1]["a"])
        self.assertTrue(a.state_map[2][-2]["b"])
        self.assertEqual(a.start, 1)
        self.assertEqual(a.end, -1)
        self.assertEqual(a.allowed_set, {-1})
        self.assertEqual(a.capture_groups[1], {(1, -1), (2, -2)})

    def test_repeat_automat(self):
        # Test the method repeat_automat
        a = Automat(1)
        a.add_transition(1, -1, 'a')
        self.assertEqual(a.start, 1)
        self.assertEqual(a.end, -1)
        op = Operator("*")
        a.repeat_automat(op)
        self.assertTrue(a.state_map[-1][1][''])
        self.assertTrue(a.state_map[2][1][''])
        self.assertTrue(a.state_map[-1][0][''])
        self.assertTrue(a.state_map[2][0][''])
        self.assertEqual(a.start, 2)
        self.assertEqual(a.end, 0)
        self.assertEqual(a.allowed_set, {0, 2, -1})
        self.assertEqual(a.id, 2)

        a = Automat(1)
        a.add_transition(1, -1, 'a')
        op = Operator("+")
        a.repeat_automat(op)
        self.assertTrue(a.state_map[-1][1][''])

    def test_alter_automat(self):
        # Test the method cat_automat
        a = Automat(1)
        a.add_transition(1, -1, 'a')
        b = Automat(2)
        b.add_transition(2, -2, 'b')
        a.alter_automat(b)
        self.assertTrue(a.state_map[3][2][''])
        self.assertTrue(a.state_map[3][1][''])
        self.assertTrue(a.state_map[-2][-3][''])
        self.assertTrue(a.state_map[-1][-3][''])
        self.assertEqual(a.start, 3)
        self.assertEqual(a.end, -3)
        self.assertEqual(a.allowed_set, {-1, -2, -3})

    def test_cat_automat(self):
        # Test the method cat_automat
        a = Automat(1)
        a.add_transition(1, -1, 'a')
        b = Automat(2)
        b.add_transition(2, -2, 'b')
        a.cat_automat(b)
        self.assertTrue(a.state_map[3][1][''])
        self.assertTrue(a.state_map[-1][2][''])
        self.assertTrue(a.state_map[-2][-3][''])
        self.assertEqual(a.start, 3)
        self.assertEqual(a.end, -3)
        self.assertEqual(a.allowed_set, {-2, -3})


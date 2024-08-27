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


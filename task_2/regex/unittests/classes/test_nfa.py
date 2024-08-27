import unittest
from ...classes import *


class TestNFA(unittest.TestCase):
    def setUp(self):
        fill_transition_sieve()

    def test_build_nfa(self):
        ast: AST = build_ast("a|bc")
        nfa: Automat = build_nfa(ast, 1)
        self.assertTrue(nfa.state_map[11][9][''])
        self.assertTrue(nfa.state_map[11][2][''])
        self.assertTrue(nfa.state_map[2][-2]['a'])
        self.assertTrue(nfa.state_map[-2][-11][''])
        self.assertTrue(nfa.state_map[9][4][''])
        self.assertTrue(nfa.state_map[4][-4]['b'])
        self.assertTrue(nfa.state_map[-4][5][''])
        self.assertTrue(nfa.state_map[5][-5]['c'])
        self.assertTrue(nfa.state_map[-5][-9][''])
        self.assertTrue(nfa.state_map[-2][-11][''])
        self.assertEqual(nfa.allowed_set, {-11, -2, -9})



import unittest
from ...classes import *

class TestOperator(unittest.TestCase):
    def setUp(self):
        return
    def test_plus(self):
        operator = Operator("+")
        self.assertEqual(operator.type, Operator.Type.REPEAT)
        self.assertEqual(operator.min_repetitions, 1)
        self.assertEqual(operator.max_repetitions, None)

    def test_star(self):
        operator = Operator("*")
        self.assertEqual(operator.type, Operator.Type.REPEAT)
        self.assertEqual(operator.min_repetitions, 0)
        self.assertEqual(operator.max_repetitions, None)

    def test_range(self):
        operator = Operator("{1,3}")
        self.assertEqual(operator.type, Operator.Type.REPEAT)
        self.assertEqual(operator.min_repetitions, 1)
        self.assertEqual(operator.max_repetitions, 3)
        operator = Operator("{5}")
        self.assertEqual(operator.type, Operator.Type.REPEAT)
        self.assertEqual(operator.min_repetitions, 5)
        self.assertEqual(operator.max_repetitions, 5)

    def test_alter(self):
        operator = Operator("|")
        self.assertEqual(operator.type, Operator.Type.ALTER)

    def test_concat(self):
        operator = Operator("")
        self.assertEqual(operator.type, Operator.Type.CONCAT)

    def test_predictive(self):
        operator = Operator("/")
        self.assertEqual(operator.type, Operator.Type.PREDICTIVE)

    def test_set_range(self):
        operator = Operator("[a-z]")
        self.assertEqual(operator.type, Operator.Type.SET_RANGE)
        self.assertEqual(operator.set_range, set("abcdefghijklmnopqrstuvwxyz"))

    def test_check_operator(self):
        self.assertTrue(Operator.check_operator("+"))
        self.assertTrue(Operator.check_operator("*"))
        self.assertTrue(Operator.check_operator("{1,3}"))
        self.assertTrue(Operator.check_operator("{5}"))
        self.assertTrue(Operator.check_operator("|"))
        self.assertTrue(Operator.check_operator(""))
        self.assertTrue(Operator.check_operator("/"))
        self.assertTrue(Operator.check_operator("[a-z]"))
        self.assertFalse(Operator.check_operator("a-z"))
        self.assertFalse(Operator.check_operator("a"))
        self.assertFalse(Operator.check_operator("z"))


class TestNodeAST(unittest.TestCase):
    def setUp(self):
        return

    def test_init(self):
        node = AST.Node("a")
        self.assertEqual(node.name, "a")
        self.assertIsNone(node.operand)
        self.assertIsNone(node.capture_group)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

        node = AST.Node("a", True)
        self.assertEqual(node.name, "a")
        self.assertIsNone(node.operand)
        self.assertIsNone(node.capture_group)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

        node = AST.Node("+")
        self.assertIsNone(node.name)
        self.assertIsNotNone(node.operand)
        self.assertIsNone(node.capture_group)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

        node = AST.Node("+", True)
        self.assertEqual(node.name, "+")
        self.assertIsNone(node.operand)
        self.assertIsNone(node.capture_group)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_check_op(self):
        node = AST.Node("+")
        self.assertTrue(node.check_op(Operator.Type.REPEAT))
        self.assertFalse(node.check_op(Operator.Type.CONCAT))

        node = AST.Node("a")
        self.assertFalse(node.check_op(Operator.Type.REPEAT))
        self.assertFalse(node.check_op(Operator.Type.CONCAT))
        self.assertFalse(node.check_op(Operator.Type.ALTER))


class TestAST(unittest.TestCase):
    def setUp(self):
        return

    def test_ast_left(self):
        ast = AST(AST.Node("A"))
        ast.ast_left(AST.Node("B"))
        self.assertEqual(ast.root.left.name, "A")
        self.assertIsNone(ast.root.right)
        self.assertEqual(ast.root.name, "B")

    def test_ast_right(self):
        ast = AST(AST.Node("A"))
        ast.ast_right(AST.Node("B"), AST.Node("C"))
        self.assertEqual(ast.root.name, "B")
        self.assertIsNotNone(ast.root.left)
        self.assertIsNotNone(ast.root.right)
        self.assertEqual(ast.root.left.name, "A")
        self.assertEqual(ast.root.right.name, "C")

    def test_set_left(self):
        ast = AST(AST.Node("A"))
        ast.set_left(AST.Node("B"))
        self.assertEqual(ast.root.left.name, "B")
        self.assertIsNone(ast.root.right)
        self.assertEqual(ast.root.name, "A")

    def test_right(self):
        ast = AST(AST.Node("A"))
        ast.set_right(AST.Node("B"))
        self.assertEqual(ast.root.right.name, "B")
        self.assertIsNone(ast.root.left)
        self.assertEqual(ast.root.name, "A")


class TestBuildAst(unittest.TestCase):
    def setUp(self):
        return

    def test_bracket_concat_ast(self):
        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("B")), AST(AST.Node(")"))]
        brackets = [0, 3]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.CONCAT)
        self.assertEqual(asts[1].root.left.name, "A")
        self.assertEqual(asts[1].root.right.name, "B")

        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("B")), AST(AST.Node("C")), AST(AST.Node(")"))]
        brackets = [0, 4]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.CONCAT)
        self.assertIsNone(asts[1].root.left.name)
        self.assertEqual(asts[1].root.left.operand.type, Operator.Type.CONCAT)
        self.assertEqual(asts[1].root.left.left.name, "A")
        self.assertEqual(asts[1].root.left.right.name, "B")
        self.assertEqual(asts[1].root.right.name, "C")


    def test_bracket_plus_ast(self):
        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("+")), AST(AST.Node(")"))]
        brackets = [0, 3]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.REPEAT)
        self.assertEqual(asts[1].root.operand.min_repetitions, 1)
        self.assertEqual(asts[1].root.operand.max_repetitions, None)
        self.assertEqual(asts[1].root.left.name, "A")
        self.assertIsNone(asts[1].root.right)

    def test_bracket_star_ast(self):
        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("*")), AST(AST.Node(")"))]
        brackets = [0, 3]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.REPEAT)
        self.assertEqual(asts[1].root.operand.min_repetitions, 0)
        self.assertEqual(asts[1].root.operand.max_repetitions, None)
        self.assertEqual(asts[1].root.left.name, "A")
        self.assertIsNone(asts[1].root.right)

    def test_bracket_range_ast(self):
        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("{1,3}")), AST(AST.Node(")"))]
        brackets = [0, 3]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.REPEAT)
        self.assertEqual(asts[1].root.operand.min_repetitions, 1)
        self.assertEqual(asts[1].root.operand.max_repetitions, 3)
        self.assertEqual(asts[1].root.left.name, "A")
        self.assertIsNone(asts[1].root.right)

    def test_bracket_alt_ast(self):
        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("|")), AST(AST.Node("B")), AST(AST.Node(")"))]
        brackets = [0, 4]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.ALTER)
        self.assertEqual(asts[1].root.left.name, "A")
        self.assertEqual(asts[1].root.right.name, "B")

        asts = [AST(AST.Node("(")), AST(AST.Node("A")), AST(AST.Node("|")), AST(AST.Node("B")), AST(AST.Node("|")), AST(AST.Node("C")), AST(AST.Node(")"))]
        brackets = [0, 6]
        ast_builder.bracket_pair_to_ast(asts, brackets)
        self.assertEqual(len(asts), 3)
        self.assertIsNone(asts[1].root.name)
        self.assertEqual(asts[1].root.operand.type, Operator.Type.ALTER)
        self.assertIsNone(asts[1].root.left.name)
        self.assertEqual(asts[1].root.left.operand.type, Operator.Type.ALTER)
        self.assertEqual(asts[1].root.left.left.name, "A")
        self.assertEqual(asts[1].root.left.right.name, "B")
        self.assertEqual(asts[1].root.right.name, "C")

    def test_tokenize(self):
        def _compare_tokens(_tokens, _test_tokens):
            for i in range(len(_tokens)):
                self.assertEqual(_tokens[i].root.name, _test_tokens[i].root.name)
                if _tokens[i].root.operand:
                    self.assertEqual(_tokens[i].root.operand.type, _test_tokens[i].root.operand.type)
                    self.assertEqual(_tokens[i].root.operand.min_repetitions,
                                     _test_tokens[i].root.operand.min_repetitions)
                    self.assertEqual(_tokens[i].root.operand.max_repetitions,
                                     _test_tokens[i].root.operand.max_repetitions)

        tokens, start_elements = ast_builder.tokenize("a|b")
        test_tokens = [AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b"))]
        _compare_tokens(tokens, test_tokens)

        tokens, start_elements = ast_builder.tokenize("a|b|c")
        test_tokens = [AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node("|")), AST(AST.Node("c"))]
        _compare_tokens(tokens, test_tokens)

        # test for brackets and figure brackets
        tokens, start_elements = ast_builder.tokenize("(a|b)")
        test_tokens = [AST(AST.Node("(")), AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node(")"))]
        _compare_tokens(tokens, test_tokens)

        tokens, start_elements = ast_builder.tokenize("{1, 2}")
        test_tokens = [AST(AST.Node("{1, 2}"))]
        _compare_tokens(tokens, test_tokens)

        tokens, start_elements = ast_builder.tokenize("[a-z]")
        test_tokens = [AST(AST.Node("[a-z]"))]
        _compare_tokens(tokens, test_tokens)

        # test for special symbols
        tokens, start_elements = ast_builder.tokenize("a|b|c*")
        test_tokens = [AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node("|")), AST(AST.Node("c")), AST(AST.Node("*"))]
        _compare_tokens(tokens, test_tokens)

        tokens, start_elements = ast_builder.tokenize("a|$")
        test_tokens = [AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("", non_operand=True))]
        _compare_tokens(tokens, test_tokens)

        # test for start element count
        tokens, start_elements = ast_builder.tokenize("(ab)(cd)(ef)")
        self.assertEqual(start_elements, 3)

        # test for ! in brackets
        tokens, start_elements = ast_builder.tokenize("(!abc)")
        test_tokens = [AST(AST.Node("(!")), AST(AST.Node("a")), AST(AST.Node("b")), AST(AST.Node("c")), AST(AST.Node(")"))]
        _compare_tokens(tokens, test_tokens)

    def test_capture_groups(self):
        tokens = [AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node("|")), AST(AST.Node("c"))]
        ast_builder.set_capture_groups(tokens)
        self.assertEqual(tokens[0].root.capture_group, [])
        self.assertEqual(tokens[1].root.capture_group, [])
        self.assertEqual(tokens[2].root.capture_group, [])
        self.assertEqual(tokens[3].root.capture_group, [])
        self.assertEqual(tokens[4].root.capture_group, [])

        tokens = [AST(AST.Node("(")), AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node(")"))]
        ast_builder.set_capture_groups(tokens)
        self.assertEqual(tokens[0].root.capture_group, [1])
        self.assertEqual(tokens[1].root.capture_group, [1])
        self.assertEqual(tokens[2].root.capture_group, [1])
        self.assertEqual(tokens[3].root.capture_group, [1])
        self.assertEqual(tokens[4].root.capture_group, [1])

        tokens = [AST(AST.Node("(")), AST(AST.Node("a")), AST(AST.Node("|")), AST(AST.Node("b")), AST(AST.Node(")")), AST(AST.Node("|"), non_operand=True), AST(AST.Node("c"))]
        ast_builder.set_capture_groups(tokens)
        self.assertEqual(tokens[0].root.capture_group, [1])
        self.assertEqual(tokens[1].root.capture_group, [1])
        self.assertEqual(tokens[2].root.capture_group, [1])
        self.assertEqual(tokens[3].root.capture_group, [1])
        self.assertEqual(tokens[4].root.capture_group, [1])
        self.assertEqual(tokens[5].root.capture_group, [])
        self.assertEqual(tokens[6].root.capture_group, [])

    def test_remove_shielding_symbols(self):
        ast = AST(AST.Node("%a"))
        ast_builder.remove_shielding_symbols(ast)
        self.assertEqual(ast.root.name, "a")

        ast = AST(AST.Node("%a"))
        ast.root.left = AST.Node("%b")
        ast_builder.remove_shielding_symbols(ast)
        self.assertEqual(ast.root.name, "a")
        self.assertEqual(ast.root.left.name, "b")

        ast = AST(AST.Node("%a"))
        ast.root.left = AST.Node("%b")
        ast.root.left.left = AST.Node("%c")
        ast_builder.remove_shielding_symbols(ast)
        self.assertEqual(ast.root.name, "a")
        self.assertEqual(ast.root.left.name, "b")
        self.assertEqual(ast.root.left.left.name, "c")

    def test_build_ast(self):
        ast = ast_builder.build_ast("a|b")
        self.assertEqual(ast.root.operand.type, Operator.Type.ALTER)
        self.assertEqual(ast.root.left.name, "a")
        self.assertEqual(ast.root.right.name, "b")

        ast = ast_builder.build_ast("abc")
        self.assertEqual(ast.root.operand.type, Operator.Type.CONCAT)
        self.assertEqual(ast.root.left.left.name, "a")
        self.assertEqual(ast.root.left.operand.type, Operator.Type.CONCAT)
        self.assertEqual(ast.root.left.right.name, "b")
        self.assertEqual(ast.root.right.name, "c")

        ast = ast_builder.build_ast("a|b|c")
        self.assertEqual(ast.root.operand.type, Operator.Type.ALTER)
        self.assertEqual(ast.root.left.left.name, "a")
        self.assertEqual(ast.root.left.operand.type, Operator.Type.ALTER)
        self.assertEqual(ast.root.left.right.name, "b")
        self.assertEqual(ast.root.right.name, "c")

        ast = ast_builder.build_ast("(a|b)")
        self.assertEqual(ast.root.operand.type, Operator.Type.ALTER)
        self.assertEqual(ast.root.left.name, "a")
        self.assertEqual(ast.root.right.name, "b")
        self.assertEqual(ast.root.capture_group, [1])
        self.assertEqual(ast.root.left.capture_group, [1])
        self.assertEqual(ast.root.right.capture_group, [1])

        ast = ast_builder.build_ast("(!abc)")
        self.assertEqual(ast.root.operand.type, Operator.Type.CONCAT)
        self.assertEqual(ast.root.left.left.name, "a")
        self.assertEqual(ast.root.left.operand.type, Operator.Type.CONCAT)
        self.assertEqual(ast.root.left.right.name, "b")
        self.assertEqual(ast.root.right.name, "c")
        self.assertEqual(ast.root.capture_group, [])
        self.assertEqual(ast.root.left.capture_group, [])
        self.assertEqual(ast.root.right.capture_group, [])

        ast = ast_builder.build_ast("ac*")
        self.assertEqual(ast.root.operand.type, Operator.Type.CONCAT)
        self.assertEqual(ast.root.left.name, "a")
        self.assertEqual(ast.root.right.operand.type, Operator.Type.REPEAT)
        self.assertEqual(ast.root.right.left.name, "c")
        self.assertEqual(ast.root.right.right, None)




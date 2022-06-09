import pytest
from myfilter.tree_node import TreeNode


def test_prune_tree():
    print()
    path_list = ['/A/A/A/A/A/hello.txt', '/A/A/A/abc.doc', '/A/B/', '/A/C/xyz.py']
    expected_path_list = ['/A/A/A/hello.txt', '/A/A/abc.doc', '/A/B', '/A/C/xyz.py']

    root = TreeNode()  # root name is ''
    leaf_node_list = [root.add_child(path) for path in path_list]
    root.dump()

    #  |- A
    #      |- A
    #          |- A
    #              |- A
    #                  |- A
    #                      |- hello.txt
    #              |- abc.doc
    #      |- B
    #      |- C
    #          |- xyz.py

    root.prune_tree_from_top_to_down()
    root.dump()

    #  |- A
    #      |- A
    #          |- A
    #              |- hello.txt
    #          |- abc.doc
    #      |- B
    #      |- C
    #          |- xyz.py

    output_path_list = [leaf_node.path for leaf_node in leaf_node_list]

    assert output_path_list == expected_path_list


def test_prune_tree_real_world():
    print()
    path_list = ['/Lab03-JUnit for Unit Test/L201926630102-DENNISERTANDY/Lab3_L201926630102/hello.java']
    expected_path_list = ['/Lab03-JUnit for Unit Test/L201926630102-DENNISERTANDY/hello.java']

    root = TreeNode()  # root name is ''

    leaf_node_list = [root.add_child(path) for path in path_list]
    root.dump()

    root.prune_tree_from_top_to_down()
    root.dump()

    output_path_list = [leaf_node.path for leaf_node in leaf_node_list]

    assert output_path_list == expected_path_list


@pytest.mark.parametrize('path_list, expected_path_list', [
    (['/A/A/A/A/A/hello.txt', '/A/A/A/abc.doc', '/A/B/', '/A/C/xyz.py'],
     ['/A/A/A/hello.txt', '/A/A/abc.doc', '/A/B', '/A/C/xyz.py']),

    (['/Lab03-JUnit for Unit Test/L201926630102-DENNISERTANDY/Lab3_L201926630102/hello.java'],
     ['/Lab03-JUnit for Unit Test/L201926630102-DENNISERTANDY/hello.java']),
])
def test_prune_tree_parametrize(path_list, expected_path_list):
    """
    Does pytest exercise all test cases?
    To see this, we can revise the expected result of test case 01.
    We'll find both test cases are exercised, but test case 01 fails.
    """
    print()

    root = TreeNode()  # root name is ''

    leaf_node_list = [root.add_child(path) for path in path_list]
    root.dump()

    root.prune_tree_from_top_to_down()
    root.dump()

    output_path_list = [leaf_node.path for leaf_node in leaf_node_list]

    assert output_path_list == expected_path_list

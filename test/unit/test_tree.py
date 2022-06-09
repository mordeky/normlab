from myfilter.tree_node import TreeNode


# TODO: Can we traverse the tree node by node?
# def test_traverse():
#     root = TreeNode('')
#     root.add_child('/A/A/A/X')
#     root.add_child('/A/B')
#     root.add_child('/A/C')
#     node = root.traverse_depth_first()
#     a = next(node)
#     while a:
#         print(a.name)
#         a = next(node)
#     pass

def test_produce_structure():
    # directory = [
    #     '/A/A/A/Hello.py',
    #     '/A/A/Hello.class',  # binary file
    #     '/A/B/B/.idea/vcs.xml',  # `.idea` folder
    #     '/A/C/C',  # empty folder
    #     '/A/C/Hello.txt',
    #     '/A/D/D.zip/D/D/Hello.py',
    #     '/A/D/D.zip/D/Hello.txt',
    # ]
    directory = [
        '/A/A/Hello.py',
        '/A/C/Hello.txt',
        '/A/D/D/Hello.py',
        '/A/D/Hello.txt',
    ]
    root = TreeNode('')
    for path in directory:
        root.add_child(path)

    root.dump()
    pass


def test_tree_node():
    # local test
    print()
    print('test add_child()')
    root = TreeNode('')  # root name is ''
    a1 = root.add_child('a1')
    a1.add_child('b1')
    a1.add_child('b2')
    a2 = root.add_child('a2')
    b3 = a2.add_child('b3')
    b3.add_child('c1')
    root.dump()
    # (root)
    #  |- a1
    #      |- b1
    #      |- b2
    #  |- a2
    #      |- b3
    #          |- c1

    print('\ntest items()')
    for name, obj in a1.items():
        print(name, obj)
    # b1 TreeNode(b1)
    # b2 TreeNode(b2)

    print('\ntest operator "in"')
    print("b2 is a1's child = %s" % ('b2' in a1))
    # b2 is a1's child = True

    print('\ntest del_child()')
    a1.del_child('b2')
    root.dump()
    print("b2 is a1's child = %s" % ('b2' in a1))
    # (root)
    #  |- a1
    #      |- b1
    #  |- a2
    #      |- b3
    #          |- c1
    # b2 is a1's child = False

    print('\ntest find_child()')
    obj = root.find_child('/a2/b3/c1')
    print(obj)
    # TreeNode(c1)

    print('\ntest find_child() with create')
    obj = root.find_child('/a1/b1/c2/b1/e1/f1', create=True)
    print(obj)
    root.dump()
    # TreeNode(f1)
    # (root)
    # |- a1
    #     |- b1
    #         |- c2
    #             |- b1
    #                 |- e1
    #                     |- f1
    # |- a2
    #     |- b3
    #         |- c1

    print('test attr path')
    print(obj.path)
    # a1 b1 c2 b1 e1 f1

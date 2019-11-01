# from .node import RootNode, Node, CDATAText
# from . import node
from .node import RootNode, Node, CDATAText



def dict2xml(dict_object):
    return _dict2xml(dict_object, is_sub_node=False)


def _dict2xml(dict_object, is_sub_node=True):
    # dict_object目标字典
    # 断言 不符合条件的话会报错
    # 目标字典必须是字典类型，长度必须为1
    assert isinstance(dict_object, dict)
    assert len(dict_object) == 1
    # 判断该结点是否是根结点
    if is_sub_node:
        NodeObject = Node
    else:
        NodeObject = RootNode
    # 获取字典的键值对
    # 为何要转换为列表再取值？因为可能有很多值，这里只取一个判断即可
    key, value = list(dict_object.items())[0]
    # 如果值是字典类型
    if isinstance(value, dict):
        text = None
        attrs = {}
        sub_node_lst = []
        for sub_key, sub_value in value.items():
            if sub_key == '#text':
                text = sub_value
            elif sub_key.startswith('@'):
                attrs[sub_key[1:]] = sub_value
            else:
                sub_node_result = _dict2xml({sub_key: sub_value})
                if isinstance(sub_node_result, list):
                    for sub_node in sub_node_result:
                        sub_node_lst.append(sub_node)
                else:
                    sub_node_lst.append(sub_node_result)
        node = NodeObject(key, attrs=attrs)
        if sub_node_lst:
            node.add_children(sub_node_lst)
        if text:
            node.text = CDATAText(text)
        return node
    # 如果值是列表类型
    elif isinstance(value, list):
        assert is_sub_node is True
        sub_node_lst = []
        for sub_value in value:
            try:
                assert isinstance(sub_value, dict)
            except AssertionError:
                print('%s\'s value is list, item should be dict, but get %s' %(key, type(sub_value)))
                raise
            sub_node = _dict2xml({key: sub_value})
            sub_node_lst.append(sub_node)
        return sub_node_lst
    # 如果以上两个都不是，说明就是字符串了，也就是到最后一层了
    else:
        node = NodeObject(key, text=CDATAText(value))
        return node

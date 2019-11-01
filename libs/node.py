from lxml import etree

class BaseNodeException(Exception):
    pass


class NodeTypeError(BaseNodeException):
    pass


class NodeError(BaseNodeException):
    pass

# xml标签的文本属性
class BaseTextAttr(object):
    '''xml标签的文本属性
    '''
    def __init__(self, text):
        self.text = self._check_and_clean_text(text)

    def _check_and_clean_text(self, text):
        if isinstance(text, int):
            return str(text)
        elif isinstance(text, str):
            return text
        else:
            raise NodeTypeError(
                'text of a tag shoud be a str, but get: %s' % type(text)
            )

    def to_xml(self):
        raise NotImplementedError()


class PureText(BaseTextAttr):
    def to_xml(self):
        return self.text

# 返回CDATA类型字符串
class CDATAText(BaseTextAttr):
    def to_xml(self):
        # 将字符串转换为<!CDATA[str]>形式
        return etree.CDATA(self.text)

# xml的标签
class BaseNode(object):
    '''xml的标签
    '''
    # 创建一个标签基类
    # 在初始化的时候判断标签的各个属性是否符合标准
    def __init__(self, name, text=None, attrs=None, child_lst=None):
        self.name = self._check_and_clean_name(name)
        self._text = self._check_and_clean_text(text)
        self.attrs = self._check_and_clean_attrs(attrs)
        self.child_lst = self._check_and_clean_child_lst(child_lst)

    # Python内置的@property装饰器就是负责把一个方法变成属性调用的
    # 这里相当于一个get函数，BaseNode.text直接返回text
    @property
    def text(self):
        return self._text

    # 这里相当于一个set函数，BaseNode.text = aaa 直接赋值text为aaa
    @text.setter
    def text(self, text):
        self._text = self._check_and_clean_text(text)

    # 检查文本属性是否为BaseTextAttr
    def _check_and_clean_text(self, text):
        if text is None:
            return None
        elif not isinstance(text, BaseTextAttr):
            raise NodeTypeError('text of a xml tag should be an isinstance of BaseTextAttr, get: %s' % (type(text)))
        else:
            return text

    # 检查标签名字是否为str
    def _check_and_clean_name(self, name):
        if isinstance(name, int):
            return str(name)
        elif isinstance(name, str):
            return name
        else:
            raise NodeTypeError(
                'name of a tag shoud be a str, but get: %s' % type(name)
            )

    # 检查子标签是否为list
    def _check_and_clean_child_lst(self, child_lst):
        if child_lst is None:
            return list()
        elif not isinstance(child_lst, list):
            raise NodeTypeError(
                'child_lst shoud be a list object, '
                'but get: %s' % type(child_lst)
            )
        else:
            for child in child_lst:
                if not isinstance(child, BaseNode):
                    raise NodeTypeError(
                        'child of a node shoud be a '
                        'BaseNode isinstance, but '
                        'get: %s' % type(child)
                    )
            return child_lst

    # 检查数据类型
    # 如果符合标准，返回，如果不符合，转换类型再返回
    def _check_and_clean_attrs(self, attrs):
        if attrs is None:
            return dict()
        elif isinstance(attrs, dict):
            for key, value in attrs.items():
                if not isinstance(key, str):
                    raise NodeTypeError('key of tag attrs should be str, get: %s' % type(key))
                if not isinstance(value, str):
                    if isinstance(value, int):
                        value = str(value)
                    else:
                        raise NodeTypeError('values of %s<tag attrs> should be str, get: %s' % (key, type(value)))
                attrs[key] = value
            return attrs
        else:
            raise NodeTypeError('attrs should be a dict object')

    def add_child(self, child_node):
        if self == child_node:
            raise NodeError('cannot add self to child_lst')
        if not isinstance(child_node, BaseNode):
            raise NodeError(
                'child of a node should be an instance '\
                'of BaseNode, but get: %s' % (type(child_node))
            )
        self.child_lst.append(child_node)

    def add_children(self, child_node_lst):
        if not isinstance(child_node_lst, list):
            raise NodeError('need list instance, but get %s' % (type(child_node_lst)))
        for child_node in child_node_lst:
            self.add_child(child_node)


    def to_xml(self):
        raise NotImplementedError()


class Node(BaseNode):
    def to_xml(self):
        tag_name = self.name
        tag_attr_dict = self.attrs
        xml = etree.Element(tag_name, **tag_attr_dict)
        for child in self.child_lst:
            xml.append(child.to_xml())
        if self.text is not None:
            xml.text = self.text.to_xml()
        return xml


class RootNode(Node):
    def to_xml(self):
        # 调用父类的一个方法
        xml = super().to_xml()
        tree = etree.ElementTree(xml)
        return tree

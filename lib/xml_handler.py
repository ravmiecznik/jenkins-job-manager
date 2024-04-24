import xmltodict
from pprint import pformat


class XmlElement(dict):
    """
    Defines mechanism to access and modify dict keys as an object attribute
    """
    def __init__(self, value, parent=None):
        """

        @param value: input value
        @param parent: parent to keep track of attribute calls
        """
        self._dict_parent = parent

        # Element can be a dictionary or a plain value like string or int, super-class constructor can run only for dict objects
        if issubclass(type(value), dict):
            dict.__init__(self, value)

    def __getitem__(self, item):
        data = dict.__getitem__(self, item)
        if isinstance(data, dict):
            # Return new XmlElement if an element is another dictionary
            return XmlElement(data, parent=data)
        else:
            # Return plain data
            return data

    def __getattr__(self, item):
        """
        Allows to access dictionary elements by key just like an attribute
        """
        return self.__getitem__(item)

    def __setattr__(self, key: str, value):
        """
        Allows to assign new value for dictionary key with setattr method
        """
        if key.startswith("_"):
            object.__setattr__(self, key, value)
        else:
            self[key] = value

    def __setitem__(self, key, value):
        """
        Sets value into parent's key. Keeping the context of parent is substantial to access chained attributes
        @param key: key
        @param value: value to set
        @return:
        """
        self._dict_parent[key] = value


class XmlHandler:
    """
    Handle XML document like an OOP object
    """
    def __init__(self, xml_data: str):
        self._data = xmltodict.parse(xml_data)

        # XML can have only one root
        root = list(self._data.keys())[0]
        self._root = XmlElement(self._data[root], parent=self._data)
    
    @property
    def root(self) -> XmlElement:
        """

        @return: XmlElement of root
        """
        return self._root

    def unparse(self) -> str:
        """

        @return: xml as string
        """
        return xmltodict.unparse(self._data, pretty=True)
    
    def __repr__(self):
        return pformat(self._data)
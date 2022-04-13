class Type:
    """
    This class is used to represent PDDL types.

    Attributes
    ----------
    name : String
        Name of the type
    extend : Type
        Type that the current type extends
    """

    def __init__(self, name, extend):
        self.name = name
        self.extend = extend

    def __str__(self):
        return 'Type: ' + self.name + \
        ' extends: ' + str(self.extend)

    def __eq__(self, other): 
        if self.name == other:
            return True
        return False

    def __repr__(self):
        return "Type: %s" % (self.name)
    
    def get_list_extensions(self):
        """
        This method is used to get the list of the extensions of the type.

        Returns
        -------
        List
            List of the extensions of the type
        """
        extensions = []
        extensions.append(self.name)
        if self.name != 'object':
            list_ext = self.extend.get_list_extensions()
            for item in list_ext:
                extensions.append(item)
        return extensions
    
    def to_PDDL(self):
        """
        This method is used to transform the type to PDDL.

        Returns
        -------
        String
            PDDL representation of the type
        """
        return '%s' % (self.name)

    
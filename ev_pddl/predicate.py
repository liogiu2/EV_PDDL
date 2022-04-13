class Predicate:
    """
    A class that is used to represent a PDDL predicate.

    Attributes:
    ------------
    name: str
        The name of the predicate.
    arguments: list of Argument
        The arguments of the predicate.
    """
    
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments             

    def __str__(self):
        string = ' '+ self.name  +'('
        i = 1
        for item in self.arguments:
            string += item.name +','
            i += 1
        string = string[:-1]
        string += ')'
        return string


    def __eq__(self, other): 
        return (
            self.__class__ == other.__class__ and 
            self.name == other.name 
            # and all(map(lambda x, y: x == y, self.arguments, other.arguments))
        )

    def __repr__(self):
        string= "Predicate: %s " % (self.name)
        for item in self.arguments:
            string += '%s '%(item)
    
    def find_argument_with_type(self, type): #TODO: check all chain of extends, probably need to to it in the domain
        for item in self.arguments:
            if item.name == type:
                return item
        return None
    
    def to_PDDL(self):
        """
        Method that is used to convert a predicate to a PDDL string.

        Returns:
        --------
        string: str
            The PDDL string of the predicate.
        """
        string = "(" 
        string += self.name
        list_types = []
        n = 1
        for item in self.arguments:
            pddl = item.to_PDDL()
            if item.name in list_types:
                string += " ?" + pddl[:1] + str(n)+ " - "
                n += 1
            else:
                string += " ?" + pddl[:1] + " - "
                list_types.append(item.name)
            string += pddl
        string += ")"
        return string

    def to_PDDL_for_action_proposition(self):
        """
        Method that is used to convert a predicate to a PDDL string.

        Returns:
        --------
        string: str
            The PDDL string of the predicate.
        """
        string = "(" 
        string += self.name
        for item in self.arguments:
            string += " " + item.name
        string += ")"
        return string
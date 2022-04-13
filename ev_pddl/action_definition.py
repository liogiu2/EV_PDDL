class ActionDefinition:

    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        string = 'action: ' + self.name 
        string +='\n\t  parameters: '
        for item in self.parameters:
            string += str(item)
        string +='\n\t  preconditions: ' + str(self.preconditions)
        string +='\n\t  effects: ' + str(self.effects) + '\n'
        return string

    def __eq__(self, other): 
        return (
            self.__class__ == other.__class__ and 
            self.name == other.name and 
            all(map(lambda x, y: x == y, self.parameters, other.parameters)) and 
            self.preconditions == other.preconditions and 
            self.effects == other.effects
        )
    
    def get_dict_parameters(self):
        return_dict = {}
        for item in self.parameters:
            return_dict[item.name] = item.type
        return return_dict
    
    def to_PDDL(self):
        """
        This method is used to create the PDDL representation of the Action
        """
        string = '\t(:action ' + self.name + '\n'
        string += '\t\t:parameters ('
        for item in self.parameters:
            string += item.to_PDDL() + " "
        string += ')\n'
        string += '\t\t:precondition ' + self.preconditions.to_PDDL() + '\n'
        string += '\t\t:effect ' + self.effects.to_PDDL() + '\n'
        string += '\t)\n'
        return string



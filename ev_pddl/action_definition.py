class ActionDefinition:

    def __init__(self, name, parameters, preconditions, effects, available = True):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects
        self.available = available

    def __str__(self):
        string = 'action: ' + self.name 
        string +='\n      parameters: '
        for item in self.parameters:
            string += str(item)
        string +='\n      preconditions: ' + str(self.preconditions)
        string +='\n      effects: ' + str(self.effects) + '\n'
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
        if self.available == False:
            return ''
            
        string = '    (:action ' + self.name + '\n'
        string += '        :parameters ('
        for item in self.parameters:
            string += item.to_PDDL() + " "
        string += ')\n'
        string += '        :precondition ' + self.preconditions.to_PDDL() + '\n'
        string += '        :effect ' + self.effects.to_PDDL() + '\n'
        string += '    )\n'
        return string



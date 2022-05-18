from ev_pddl.action_definition import ActionDefinition
from ev_pddl.action_proposition import ActionProposition
from ev_pddl.predicate import Predicate
from ev_pddl.relation import Relation, RelationValue

class Action:
    """
    A Class used to represent an Action. An action differs from an action_definition because is made of Relations
    
    Attributes
    ----------
    parameters : dict
        dict of parameters (Entity) that need to be sobstituted when transforming from action_definition to Action
    name : String
        Name of the action
    precondition : ActionProposition, read-only
        ActionProposition with the preconditions
    effects : ActionProposition, read-only
        ActionProposition with the effects

    """

    def __init__(self, action_definition, parameters):
        self._action_definition = action_definition
        self.name = action_definition.name
        self.__parameters = {}
        self.__preconditions = None
        self.__effects = None
        self.__available = True
        self.create_action(self._action_definition, parameters)
    
    #-----------------------------------
    #       Parameters methods
    #-----------------------------------
    @property
    def parameters(self):
        """
        Getter for the parameters of the action
        """
        return self.__parameters
    
    @parameters.setter
    def parameters(self, parameters):
        """
        Setter for the parameters of the action. If you change the parameters the action will be rebuilt
        """
        self.create_action(self._action_definition, parameters)
    
    #-----------------------------------
    #       preconditions methods
    #-----------------------------------
    @property
    def preconditions(self):
        """
        Getter for the preconditions of the action
        """
        return self.__preconditions
    
    #-----------------------------------
    #       effects methods
    #-----------------------------------
    @property
    def effects(self):
        """
        Getter for the preconditions of the action
        """
        return self.__effects

    #-----------------------------------
    #       available methods
    #-----------------------------------
    @property
    def available(self):
        """
        Getter for the preconditions of the action
        """
        return self.__available
    
    @available.setter
    def available(self, value : bool):
        """
        Setter for the available attribute
        """
        self.__available = value
    
    #-----------------------------------
    #       Other methods
    #-----------------------------------

    def create_action(self, action_definition: ActionDefinition, parameters):
        """A method that is used to create an action from an action definition
        
        Parameters
        ----------
        action_definition : ActionDefinition
            the model of the action
        parameters : dict
            the parameters that need to be sobstituted from the action_definition
        """
        #Cheking action_definition parameters with dict of parameters passed in the method to be sobstitute in the action
        for param in action_definition.parameters:
            if param.name in parameters.keys():
                self.__parameters[param.name] = parameters[param.name]
            else:
                raise KeyError("Parameter %s in action %s not found"%(param.name, action_definition.name))
        #Transforming preconditions from predicate to relations
        self.__preconditions = self._transform_action_proposition_recursive(action_definition.preconditions)
        #Transforming effects from predicate to relations
        self.__effects = self._transform_action_proposition_recursive(action_definition.effects)
        
    def _transform_action_proposition_recursive(self, action_prop: ActionProposition):
        """A method that is used to recursively navigate an actionProposition and transform the predicates to relations
        
        Parameters
        ----------
        action_prop : ActionProposition
            actionProposition to navigate and transform to relations
        """
        if action_prop.name in ['and', "or", "not"]:
            if action_prop.name == 'not' and len(action_prop.parameters) == 1:
                relation = self._from_predicate_to_relation(action_prop.parameters[0], True)
                return relation
            return_action_prop = ActionProposition(action_prop.name, [])
            for item in action_prop.parameters:
                if type(item) == Predicate:
                    relation = self._from_predicate_to_relation(item)
                    return_action_prop.add_parameter(relation)
                elif type(item) == ActionProposition:
                    return_action_prop.add_parameter(self._transform_action_proposition_recursive(item))
            return return_action_prop
        elif action_prop.name == 'forall':
            #TODO: transformation for forall
            pass   

    def _from_predicate_to_relation(self, predicate, not_value = False) -> Relation:
        """A method that is used to transform a predicate to a relation
        
        Parameters
        ----------
        predicate : Predicate
            predicate that needs to be transformed
        not_value : bool, optional
            needs to be True only in case we want a False relation
        """
        list_entity = []
        list_type = []
        for arg in predicate.arguments:
            if arg.name not in self.__parameters.keys():
                raise ValueError("%s not found in list of parameters"%(arg.name))
            list_entity.append(self.__parameters[arg.name])
            list_type.append(arg.type)
        if not_value:
            return Relation(predicate, list_entity, RelationValue.FALSE)
        else:
            return Relation(predicate, list_entity, RelationValue.TRUE)
    
    def to_PDDL(self):
        """A method that is used to transform the action to a PDDL action

        Returns
        -------
        String
            PDDL representation of the action
        """
        #':action openfurniture\n
        # :parameters (bob alchemyshop.Chest alchemyshop.Chest )\n
        # :precondition (and (alive bob = TRUE)
        # (at bob alchemyshop.Chest = TRUE)
        # (is_open alchemyshop.Chest = FALSE)
        # (can_open alchemyshop.Chest = TRUE))\n
        # :effect (and (is_open alchemyshop.Chest = TRUE))\n'
        if self.__available == False:
            return ""

        return_string = ":action %s\n"%(self.name)
        return_string += "        :parameters ("
        for item in self.__parameters.keys():
            return_string += "%s "%(self.__parameters[item].to_PDDL())
        return_string += ")\n"
        return_string += "        :precondition %s\n"%(self.__preconditions.to_PDDL())
        return_string += "        :effect %s\n"%(self.__effects.to_PDDL())
        return return_string

    def find_parameters_with_type(self, type):
        """
        This method is used to find with entity of the parameters has a specific type

        Parameters
        ----------
        type : String
            Type of the entity

        Returns
        -------
        List
            List of the entity that has the type
        """
        return_list = [self.__parameters[item] for item in self.__parameters.keys() if type in self.__parameters[item].type.get_list_extensions()]
        return return_list     

    def get_string_execution(self) -> str:
        """
        This method is used to get the string representation of the action that can be send to the environment to be executed

        Returns
        -------
        str:
            String representation of the action
        """  
        return_string = "%s("%(self.name)
        for item in self.__parameters.keys():
            return_string += "%s, "%(self.__parameters[item].name)
        return_string = return_string[:-2] + ")"
        return return_string
    
from ev_pddl.domain import Domain


class Problem:
    """
    
    """
    
    def __init__(self, name, domain, objects = [], initial_state = []):
        self.problem_name = name
        if type(domain) is not Domain:
            raise Exception("Domain in problem was expecting type Domain got %s"%(type(domain)))
        self.domain = domain
        self.__objects = objects
        self.__initial_state = initial_state

    @property
    def objects(self):
        """
        Getter for objects
        """
        return self.__objects
    
    @objects.setter
    def objects(self, objects):
        """
        Setter for objects
        """
        self.__objects = objects
    
    def add_object(self, obj, check_duplicates = True):
        """
        Method that adds an entity to the problem. It checks if the entity is already in the problem and if it is not it adds it.

        Parameters
        ----------
        obj : Entity
            The entity to add
        check_duplicates : bool, optional
            If true it checks if the entity is already in the problem, by default True
        """
        if check_duplicates and self.find_objects(obj.name) is not None:
            raise AttributeError('Object %s in the problem already exists'%(obj.name))
        self.__objects.append(obj)
    
    def find_objects(self, obj_name : str):
        """
        Finds all objects with a given name in the problem

        Parameters
        ----------
        obj_name : str
            The name of the object to search for
        """
        for item in self.__objects:
            if item.name.lower() == obj_name.lower():
                return item
        return None
    
    @property
    def initial_state(self):
        """
        Getter for initial_state
        """
        return self.__initial_state
    
    @initial_state.setter
    def initial_state(self, initial_state):
        """
        Setter for initial_state
        """
        self.__initial_state = initial_state
    
    def add_relation_to_initial_state(self, relation):
        """A method that is used to add a relation to the initial state
        
        Parameters
        ----------
        relation : Relation
        """
        if relation in self.__initial_state:
            raise AttributeError('Relation already exists in current problem.')
        self.initial_state.append(relation)
    
    def __str__(self) -> str:
        string = "Problem name: %s "%(self.problem_name)
        string += "Associated Domain name: %s\n"%(self.domain.domain_name)
        string += "Objects: \n    "
        for item in self.objects:
            string += "%s, "%(str(item))
        string += "\nInitial State: \n"
        for item in self.initial_state:
            string += "    %s\n "%(str(item))
        return string
    
    def find_objects_with_type(self, type_e, exclude_types = []):
        """
        A method that is used to find all objects of a given type in the problem. It checks also in the extesions list of the type.

        Parameters
        ----------
        type_e : Type
            The type to search for
        exclude_types : list, optional
            A list of types to exclude, by default []
        """
        return_list = []
        for item in self.objects:
            if type_e in item.type.get_list_extensions():
                if item.type not in exclude_types:
                    return_list.append(item)
        return return_list
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
            self.problem_name == other.problem_name and 
            all(map(lambda x, y: x == y, self.__objects, other.objects)) and 
            all(map(lambda x, y: x == y, self.__initial_state, other.initial_state)) and 
            self.domain == other.domain
            )

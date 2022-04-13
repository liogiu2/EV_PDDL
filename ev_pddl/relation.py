from ev_pddl.problem import Problem
from ev_pddl.domain import Domain
from ev_pddl.predicate import Predicate
from ev_pddl.relation_value import RelationValue

class Relation:
    """
    A class that is used to represent a relation between entities.

    Attributes:
    ------------
    predicate: Predicate
        The predicate of the relation.
    entities: list of Entity
        The list of entities that compose the relation.
    value: RelationValue
        The value of the relation.
    """

    def __init__(self, predicate, entities, value, domain = None, problem = None):
        if type(value) is not RelationValue:
            raise Exception('Value must be enum RelationValue')
        if type(predicate) is not Predicate:
            raise Exception('predicate must be class Predicate')
        if domain is not None and problem is not None:
            if type(domain) is not Domain:
                raise Exception('Domain must be class Domain')
            if type(problem) is not Problem:
                raise Exception('Problem must be class Problem')
            if not self.is_valid_relation(predicate, entities, domain, problem):
                raise Exception('Relation is not valid')
            self.domain = domain
            self.problem = problem
        self.predicate = predicate
        self.entities = entities
        self.value = value
        

    def is_valid_relation(self, predicate, entities, domain, problem) -> bool:
        """
        Method that is used to check if a relation is valid.

        Parameters:
        ------------
        predicate: Predicate
            The predicate of the relation.
        entities: list of Entity 
            The list of entities that compose the relation.
        domain: Domain
            The domain of the problem.
        problem: Problem
            The problem of the domain.
        """
        #check if entities exist
        for item in entities:
            if problem.find_objects(item.name) is None:
                raise Exception('Object %s not found in the list of Objects in the Problem'%(item.name))
        #check if predicate exist
        if domain.find_predicate(predicate.name) is None:
            raise Exception('Cannot find predicate %s in domain %s'%(predicate.name, domain.domain_name))
        #check that type of entities and predicate fit
        check_entity = entities.copy()
        for item in predicate.arguments:
            entity_found = self.find_entity_with_type(check_entity, item.name)
            if entity_found is None:
                raise Exception('Entity %s in relation not found'%(item.name))
            check_entity.remove(entity_found)
        if len(check_entity) > 0:
            raise Exception('More objects written with relation %s'%(predicate.name))
        return True

    
    def find_entity_with_type(self, entities = None, entity_type = None):
        if entities is None:
            entities = self.entities
        if entity_type is None:
            raise Exception('find_entity_with_type: Type must be specified')
        for item in entities:
            extension = item.type.get_list_extensions()
            if entity_type in extension:
                return item
        return None

    def modify_value(self, value: RelationValue):
        if self.value != value: 
            self.value = value
    
    def __str__(self) -> str:
        string = self.predicate.name + '('
        for item in self.entities:
            string += item.name + ', '
        string = string[:-2] +'):'
        string += str(self.value)
        return string
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.value == other.value and 
            self.predicate == other.predicate and 
            all(map(lambda x, y: x == y, self.entities, other.entities))
        )

    def equals_exclude_value(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.predicate == other.predicate and 
            all(map(lambda x, y: x == y, self.entities, other.entities))
        )
    
    def to_PDDL(self):
        """
        Method that is used to convert a relation to a PDDL string.

        Returns:
        --------
        string: str
            The PDDL string of the relation.
        """
        string = "(" 
        if self.value == RelationValue.FALSE:
            string += "not "
        string += self.predicate.name + " "
        for item in self.entities:
            string += item.to_PDDL_for_relation() + " "
        string = string[:-1] + ")"
        # string += "= "
        # if self.value == RelationValue.TRUE:
        #     string += "TRUE"
        # elif self.value == RelationValue.FALSE:
        #     string += "FALSE"
        # elif self.value == RelationValue.PENDING_TRUE:
        #     string += "PENDING_TRUE"
        # elif self.value == RelationValue.PENDING_FALSE:
        #     string += "PENDING_FALSE"
        return string



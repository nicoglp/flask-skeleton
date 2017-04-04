from abc import abstractmethod
from app import service
from app.base.exception import ServiceException

class WorkflowException(ServiceException):

    def __init__(self, message, errors=None):
        super(WorkflowException, self).__init__(message)
        self.errors = errors

class Action:
    """
    Represents the actions through the workflow
    """

    @abstractmethod
    def execute(self, **kwargs):
        """
        This method execute the actions between two states
        and if anything happens it must raise a WorkflowException
        :return:
        """
        pass


class State:
    """
    Represents the state of a process.
    """

    name = None
    description=None
    transitions = []

    def __init__(self, name, description, transitions):
        self.name = name
        self.description = description
        self.transitions = transitions

    def get_transition_for_state(self, state_name):
        for t in self.transitions:
            if t.next_state.name.lower() == state_name.lower():
                return t
        return None

    def get_next_available_states(self):
        next_states = []
        for t in self.transitions:
            next_states.append(t.next_state.name)
        return next_states

class Transition:
    """
    Represents the transition between two states
    """

    name = None
    next_state = None
    actions = []

    def __init__(self, name, next_state, actions):
        self.name = name
        self.next_state = next_state
        self.actions = actions


class Workflow:
    """
    Represents the business workflow
    """
    def __init__(self, actual_state):
        self.actual_state = actual_state

    def transition(self, next_state_name, **kwargs):
        '''
        This method transitioning the actual state to the state in the parameter
        :param kwargs: represent the context of the transition, you can add everything that the Actions needs to be executed as well
        :param next_state_name:
        :return: the next state in the workflow
        '''
        t = self.actual_state.get_transition_for_state(next_state_name)
        if t:
            service.logger.info('Transitioning workflow from %s to %s' % (self.actual_state.name, t.next_state.name))
            try:
                for action in t.actions:
                    action.execute(**kwargs)
                self.actual_state = t.next_state
                return self.actual_state
            except WorkflowException as e:
                service.logger.warn('An error has occurred in an action while a transition '
                                    'from state %s to state %s was happening %s',
                                    self.actual_state.name, next_state_name, e.message)
                raise e
        else:
            message = 'The next state %s is no applicable for the actual ' \
                                              'state %s' % (next_state_name, self.actual_state.name)
            raise WorkflowException(message, errors=None)

    def get_next_available_states(self):
        return self.actual_state.get_next_available_states()

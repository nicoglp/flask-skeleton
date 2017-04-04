
class HealthResult():

    def __init__(self, active=True, warnings=[]):
        self.active = active
        self.warnings = warnings


class HealthChecker():

    description = "Description field has not been updated. Please specify your the health check description"

    def check(self, **kwargs):
        """
        This method return a HealthResult before checking the health of the service and seta list of warnings if there is any
        :param kwargs:
        :return: True or False, Warnings in case that the service failed and the description field
        """
        return [HealthResult(True, [])]


class CheckersWrapper:
    """
    This class represents the wrapper for all the helthchekers elements
    """

    def __init__(self, hc_list):
        self.hc_list = hc_list

    def add_check(self, checker):
        self.hc_list.append(checker)

    def check(self, **kwargs):
        results = []
        for cheker in self.hc_list:
            results.extend(cheker.check())
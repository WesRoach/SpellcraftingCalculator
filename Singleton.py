# HEADER PLACEHOLDER


class Singleton:
    __instance = None

    @staticmethod
    def getInstance():
        if Singleton.__instance:
            return Singleton.__instance
        else:
            raise Exception('ERROR: Class has not been instatiated.')

    def __init__(self):
        if not Singleton.__instance:
            Singleton.__instance = self
        else:
            raise Exception('ERROR: Class is already instantiated.')

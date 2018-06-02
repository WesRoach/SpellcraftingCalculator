# HEADER PLACEHOLDER


class Singleton:
    __single = None

    @staticmethod
    def instance():
        return Singleton.__single

    def __init__(self):
        if Singleton.__single:
            raise TypeError("Singleton is already instantiated")
        Singleton.__single = self

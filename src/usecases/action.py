from src.usecases.info import Information


class ActionInsert:

    def insert_uploaded(self, information: Information):
        pass

    def insert_removed(self, information: Information):
        pass


class ActionWrite:

    def export(self):
        pass


class Action(ActionInsert, ActionWrite):
    pass

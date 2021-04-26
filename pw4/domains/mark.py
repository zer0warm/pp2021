class MarkManager:
    class Mark:
        def __init__(self, value, r_obj=None, e_obj=None):
            self.__value = value
            self.__manager = r_obj
            self.__managee = e_obj

        def get_value(self):
            return self.__value

        def get_object(self, _type):
            if isinstance(self.__manager, _type):
                return self.__manager
            return self.__managee

    def __init__(self):
        self._marks = []

    def add_mark(self, value, obj=None):
        mark = MarkManager.Mark(value, e_obj=obj)
        self._marks.append(mark)

    def get_mark(self, obj=None):
        for mark in self._marks:
            if mark.get_object(obj.__class__) == obj:
                return mark
        return False

    def has_marks(self):
        return bool(self._marks)

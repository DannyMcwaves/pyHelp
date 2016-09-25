"""
so this is just a simple interactive help tool for a class
that creates and then returns a dictionary with all the names of the methods
as keys and the doc strings as values of those keys.

so to access the doc on any method, just pass the name of the method as you
you would for a getitem in dict. and then you get the doc.

If you need it for the main class, then pass main as the key.
"""
from notes import Notes
from pprint import pprint


class ihelp:
    """
    this is nothing but an interactive help module for a class.
    """
    __dict = {}

    def __init__(self, _class):
        self.__object = _class
        self.__run()

    @property
    def __func_type(self):
        """
        :return: the str representation type of a function for comparison
        """

        def test():
            """this is just a test function"""
            pass

        return type(test)

    def __test_type(self, other):
        """
        to check for the matching type. class will match a class and then function will match a function
        """
        object_type = None
        try:
            issubclass(other, object)
            object_type = "Class"
        except KeyError:
            object_type = "Undefined"
        except TypeError:
            if type(other) == self.__func_type:
                object_type = "Function"
            else:
                object_type = "Variable"
        finally:
            return object_type

    def function(self, function):
        """
        this is going to get the doc string on a function and then
        if none exists, the it return doc not available
        """
        return function.__doc__.strip() if function.__doc__ is not None else "No documentation for this method"

    def __run(self):
        """
        this is supposed to run and then get all the docs on a particular function if they exist, if not
        return not doc for this method. Just like I did with the notes thingy.
        """

        def inner(_class: object, container) -> object:
            """
            this one should recursively search the class for any methods or classes that are available.
            and then get all the docs on them.
            """
            mapping = _class.__dict__

            if mapping["__doc__"] is None:
                mapping["__doc__"] = "No documentation for this class.\n"

            container["__main__"] = mapping['__doc__']

            for k in mapping:
                if type(mapping[k]) == self.__func_type:
                    container[k] = self.function(mapping[k])

                elif self.__test_type(mapping[k]) == "Class":
                    new = self.__dict[k] = {}
                    print()
                    inner(mapping[k], new)

        inner(self.__object, self.__dict)

    def docs(self):
        return self.__dict

    def __getitem__(self, item):
        return self.__dict[item]

    def __iter__(self):
        return iter(self.__dict)


if __name__ == '__main__':
    n = ihelp(Notes)
    for i in n:
        pprint(i)
        pprint(n[i])
        print()

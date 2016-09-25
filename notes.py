#! /usr/bin/env python3.5
"""
this is just a simple introduction to the notes package.
the notes module, is just a simple package that is supposed to relieve people of the
stress of creating README *.md *.txt or getting help on a specific module by utilising
the doc strings provided in any module. the docstrings could be the main docstrings on the
start of a document in a class or a function.

**  DOCSTRINGS START AND END WITH THREE COMMA'S AS SO.
    \"""
       any help on a particular object you are trying hard to write
       should be in this enclosed string. every pythonista knows how
       to write docs.
    \"""

USAGE fo Notes:
    from notes import Notes

    NB: the module you are going to use is supposed to expose a set of api's
        (functions and classes in the all variable)
        ie. __all__ = ["class", "anotherClass", "function1", "function2"]
        the order in which you display them is the order in which the docstrings will be generated.

    these are the two constants you need to pass to the Notes Object. You don't have to pass anything else.
    but make sure all is defined so as to create help for it.

    *** notes = Notes(globals(), __all__)

    *** docs = notes()
    -- call notes to get the docs on all the passed api's. (1)

    *** print(docs)
    -- docs is the full docs on the modules you passed (2)

    *** notes(print)
    -- Is the same as the lines (1) and (2)
    -- You can pass and callback function that will operate on the docs.

    *** notes += "any other thing you are willing to add to the docstring before you operate on it".
    --you can edit the docs on the go and then add more to it

    *** notes.save(name)
    -- This is the one that save the docs to a file. if no, name is provided,
    -- It uses README.txt
"""

from pprint import pprint
__all__ = ["Notes", "pprint"]


class Notes:
    """
        so this is the main class that implements all the methods of the notes thingy.
        this is supposed to be rather simple, succinct and concise.
    """

    def __init__(self, _ty, api=None):
        self.__globals = _ty
        self.__apis = api
        self.__fulldoc__ = "MAIN:"+self.__globals["__doc__"] + "\n\n"
        self.__run()

    @property
    def __apis__(self):
        """
        all of the methods in the all thing.
        the _all parameter should include all the set of the APIs in a particular module that you are
        trying expose and those APIs should have a __doc__ string in them. Because we are going to use that
        to construct the readme file for you.
        :return:
        """
        if self.__apis is None:
            __all = ["__doc__"]
        else:
            __all = [x for x in self.__apis if x in self.__globals]
            __all.append("__doc__")
        return __all

    def file(self):
        """
        this should return a file rep for the whole module.
        every single line in the code.
        :return:
        """
        _file = self.__globals["__file__"]
        _content = ""
        with open(_file) as fp:
            for line in fp.readlines():
                _content += line
        return _content

    def __eval__(self, api):
        """
        this is to check if the api is available in this current module
        :param api: the api to check for
        :return: return the mem rep for the api from globals
        """
        return self.__globals[api]

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
        :param other: an object.
        :return: True or False
        """
        object_type = None
        try:
            if type(other) == str:
                other = self.__eval__(other)
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

    def __func_exec(self, function):
        """
        this will return the name and the docstring of the function as a single string.
        :param function: the name of the function
        :return: name + docstring of the function as a single string.
        """
        try:
            if type(function) == str:
                function = self.__eval__(function)
        except NameError:
            return NotImplemented

        if function.__doc__ is None:
            function.__doc__ = "No documentation for the this {type}"

        return "{type}: \t" + function.__name__ + "\n{fmt}__doc__: " + function.__doc__ + "\n\n"

    def __class_exec(self, _class):
        """
        this will return the name of the function and all other methods it contains and the docstrings
        of the functions and the class itself including any other other classes contained within this
        class.
        :param _class: the class to be passed around and extracted from.
        :return:
        """

        main = ""
        _classEval = _class

        try:
            if type(_class) == str:
                _classEval = self.__eval__(_class)
        except NameError:
            return NotImplemented

        def inner(_class, fmt="", _fmt=""):
            nonlocal main, _classEval
            index = dir(_classEval).index("__dict__")
            mapping = eval(_class + "." + dir(_classEval)[index])
            count = _class.count(".")
            if count > 0:
                _fmt *= count
                fmt *= count

            if mapping["__doc__"] is None:
                mapping["__doc__"] = "No documentation for this class."

            main += _fmt + "CLASS : " + _class + "" + mapping["__doc__"] + "\n"

            for k in mapping:
                if type(mapping[k]) == self.__func_type:
                    if k == "__init__":
                        main += fmt + "\t" + self.__func_exec(mapping[k]).format(type="METHOD", fmt=fmt+"\t")

            for k in mapping:
                if type(mapping[k]) == self.__func_type:
                    if k != "__init__":
                        main += fmt + "\t" + self.__func_exec(mapping[k]).format(type="METHOD", fmt=fmt+"\t")

            for k in mapping:
                if self.__test_type(mapping[k]) == "Class":
                    inner(_class + "." + k, fmt="\t", _fmt="\t")

        inner(_class)
        self.__fulldoc__ += main

    def __run(self):
        """
        so this run for all the objects in the api's list argument provided.
        :return: None
        """

        for i in self.__apis__:
            if i is not "__doc__":
                kind = self.__test_type(i)

                if kind == "Class":
                    self.__class_exec(i)
                elif kind == "Function":
                    self.__fulldoc__ += self.__func_exec(i).format(type="FUNCTION ", fmt="")

    def __call__(self, callback=None):
        """
        I am not saying that this is asynchronous programming, but callback should definitely be passed
        for use with the docs.
        :callback: a callback function to be executed
        :return:
        """
        try:
            if callback is not None:
                callback(self.__fulldoc__)
        except Exception as ee:
            print("CALLBACK FAILED WITH MESSAGE: " + ee.args[0])
        finally:
            return self.__fulldoc__

    def __iadd__(self, other):
        self.__fulldoc__ += other
        return self

    def save(self, name="TRIAL.txt"):
        """
        if you want to save the content of the docs to a file
        :param name: then pass the name as the parameter of the file you wanna save else I am using readme.txt
        :return:
        """
        with open(name, "w") as fp:
            fp.write(self.__fulldoc__)

    class Danny:
        """
        who is going to stop me now
        """
        def __init__(self):
            """
            oooooooooooh my God.
            """

        class Me:
            """
            Is this the fault of the squabble in the code
            """
            def __init__(self):
                """
                another small crazy trial
                """
                self.__name = "Danny Mcwaves"

            def __str__(self):
                """
                an str rep of the name of the user.
                :return:
                """
                return self.__name


if __name__ == '__main__':
    notes = Notes(globals(), __all__)
    notes += "Owner: Danny Mcwaves"
    docs = notes(print)
    notes.save("try")

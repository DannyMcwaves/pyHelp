this is just a simple introduction to the notes package.
the notes module, is just a simple package that is supposed to relieve people of the
stress of creating README *.md *.txt or getting help on a specific module by utilising
the doc strings provided in any module. the docstrings could be the main docstrings on the
start of a document in a class or a function.

**  DOCSTRINGS START AND END WITH THREE COMMA'S AS SO.
    """
       any help on a particular object you are trying hard to write
       should be in this enclosed string. every pythonista knows how
       to write docs.
    """

first of all there are two modules.
    -Notes
    -iHelp

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
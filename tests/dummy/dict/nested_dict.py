# Right
foo = {
    'a': {'x': 'hello', 'y': 'world'},
    'b': {
        'x': 'hello',
        'y': 'world',
    },
}


# Dict has child with a child dict
# Wrong: PL101
foo = {'a': {'one': 'hello'}, 'b': {'two': 'world'},
       'c': {'three': 'hello'}, 'd': {'four': 'world'},
}


# Wrong: PL101, PL102
foo = {
    'a': {'x': 'hello', 'y': 'world'},
    'b': {'x': 'hello',
          'y': 'world'},
}


# Wrong: PL110
foo = {
    'a': {'x': 'hello', 'y': 'world'},
    'b': {'x': 'hello', 'y': 'world'},
      }

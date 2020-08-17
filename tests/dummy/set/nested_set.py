# Right
foo = {
    {'hello', 'world'},
    {
        'hello',
        'world',
    },
}


# Wrong: JS101, PL102
foo = {
    {'hello', 'world'},
    {'hello',
     'world'},
}


# Wrong: JS102
foo = {
    {'hello', 'world'},
    {'hello', 'world'},
      }

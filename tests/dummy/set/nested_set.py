# Right
foo = {
    {'hello', 'world'},
    {
        'hello',
        'world',
    },
}


# Wrong: PL101, PL102
foo = {
    {'hello', 'world'},
    {'hello',
     'world'},
}


# Wrong: PL110
foo = {
    {'hello', 'world'},
    {'hello', 'world'},
      }

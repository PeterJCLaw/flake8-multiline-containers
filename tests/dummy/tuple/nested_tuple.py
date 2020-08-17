# Right
foo = (('hello', 'world'), ('sun', 'moon'))

# Right
foo = (
    ('hello', 'world'),
    (
        'hello',
        'world',
    ),
)


# tuple has child list that ends on same line as opening
# Wrong: PL101
foo = (('earth', 'mars'),
       ('sun', 'moon'),
)


# tuple has child with a child tuple that ends on same line as opening
# Wrong: PL101
foo = ({'a': 'hello', 'b': ('earth', 'mars')},
       {'c': 'good night', 'd': 'moon'},
)


# Nested tuple contains a container that doesn't break on the opening
# Wrong: PL101, PL102
foo = (
    ('hello', 'world'),
    ('hello',
     'world'),
)


# Nested tuple closes on wrong column
# Wrong: PL110
foo = (
    ('hello', 'world'),
    ('hello', 'world'),
      )

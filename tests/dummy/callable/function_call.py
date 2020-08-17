# Wrong: PL101, PL102
bizbat ( "Hello",
         "World")

# Wrong: PL101, PL102
bizbat        ( "Hello",
         "World")

# Right
# Function call containing parens around a long string
func(
    (
        "long string such that we use parens"
    ),
)

# Right: triple quoted string hugging is allowed
bizbat(bazbin("""
"""))


# Wrong: PL101, PL102
bizbat(bazbin('a',
'b'))


# Right: Opens and closes on same line
foo = bizbat('hello', 'world')

# Right: Line break after parenthesis, closes on same column
foo = bizbat(
    'hello',
    'world',
)


# Right: Line break after parenthesis, closes on same column
foo = bizbat(
    'hello', 'world',
)


# Wrong: PL101
foo = bizbat('hello',
       'world',
)

# Wrong: PL102
foo = bizbat(
    'hello', 'world')


# Wrong: PL101, PL102
foo = bizbat('hello',
       'world')


# Wrong: PL101, PL110
foo = bizbat('hello',
       'world',
      )


# Right
# Function call with tuple inside
foo = bizbat(
    (
        'hello',
        'world',
    )
)


# Wrong (TODO): Should also error about the double trailer
# Function call with tuple inside
foo = bizbat((
    'hello',
    'world',
)
)

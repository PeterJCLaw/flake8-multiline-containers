# Right: Opens and closes on same line
foo = {'hello', 'world'}


# Right: Line break after parenthesis, closes on same column
foo = {
    'hello',
    'world',
}


# Right: Line break after parenthesis, closes on same column
foo = {
    'hello', 'world',
}


# Wrong: PL101
foo = {'hello',
       'world',
}

# Wrong: PL102
foo = {
    'hello', 'world'}


# Wrong: PL101, PL102
foo = {'hello',
       'world'}


# Wrong: PL101, PL110
foo = {'hello',
       'world',
      }

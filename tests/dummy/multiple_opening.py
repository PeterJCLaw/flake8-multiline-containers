# Right
foo = {'a': {
    'b': 1
}}

# Wrong (TODO): Should also error about the double trailer
foo = {'a': {
    'b': 1
}
}

# Wrong: PL101, PL110
foo = {'a': {'b':
        1
    }
}

# Wrong: PL101
foo = {'a':
    {
        'b': 1
    }
}

# Wrong: PL102
foo = {'a': {
    'b': 1}
}

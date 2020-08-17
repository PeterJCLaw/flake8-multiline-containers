# Wrong: PL101
def foo (a,
         b,
         c,
): pass

# Wrong: PL101
def foo     (a,
         b,
         c,
): pass

# Right: Function without any arguments.
def foo():
    pass


# Right: Function with arguments, ends on opening line.
def bar(a, b, c):
    pass


# Function with keyword argument that is a tuple.
# Right
def barb(a, b, c=('Hello', 'World')):
    pass


# Function with keyword argument that is a tuple.
# Wrong(TODO): closing paren should hug
def baro(a, b, c=(
    'Hello', 'World',
),
):
    pass


# Right: Function with arguments, break after lunula
def biz(
    a,
    b,
    c,
):
    pass


# Wrong: PL101, PL110
# Function with arguments, break after first argument
def baz(a,
        b,
        c,
        ):
    pass


# Wrong: PL101, PL102
#Function with arguments, break after first argument,
# closing bracket after last argument
def bal(a,
        b,
        c):
    pass

if True:
    {
        1: 'test',
        2: 'promo',
    }[1]  # JS102 on col 1 of this line

bad = ('foo',
       'bar')

bad = (
    'foo',
    'bar')

bad = ('foo',
       'bar',
)

good = [('foo')]
good = [(
    'foo',
)]

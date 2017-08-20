Solve a substitution cipher. Tested in Python 2 and 3.

Sample run:

    $ python cryptopuzzle.py
    Enter the encrypted puzzle, followed by a line with only a period ('.') to mark the end:
    rg'p bpvkvpp gx ghc gx exky pxiv uvxukv gx owcgerwa gevc poc ferkv gevc'hv
    ioykc rw kxlv, yhbwz, xh hbwwrwa txh xttrqv.
    .

      '                                                                    '
    -- - ------- -- --- -- ---- ---- ------ -- -------- ---- --- ----- ---- --
    rg'p bpvkvpp gx ghc gx exky pxiv uvxukv gx owcgerwa gevc poc ferkv gevc'hv

                 ,      ,                      .
    ----- -- ----  -----  -- ------- --- ------
    ioykc rw kxlv, yhbwz, xh hbwwrwa txh xttrqv.

    Free: abcdefghijklmnopqrstuvwxyz

    Enter a substitution like 'crypt/plain': rg'p/it's

    it's  s   ss t  t   t       s           t     t i   t    s     i   t   '
    -- - ------- -- --- -- ---- ---- ------ -- -------- ---- --- ----- ---- --
    rg'p bpvkvpp gx ghc gx exky pxiv uvxukv gx owcgerwa gevc poc ferkv gevc'hv

          i      ,      ,        i          i  .
    ----- -- ----  -----  -- ------- --- ------
    ioykc rw kxlv, yhbwz, xh hbwwrwa txh xttrqv.

    Free: abcdefgh jklmnopqr  uvwxyz

    ... more playing snipped ...

    Free:  b       j     pq      x z

    Enter a substitution like 'crypt/plain': u/p

    it's useless to try to hold some people to anything they say while they're
    -- - ------- -- --- -- ---- ---- ------ -- -------- ---- --- ----- ---- --
    rg'p bpvkvpp gx ghc gx exky pxiv uvxukv gx owcgerwa gevc poc ferkv gevc'hv

    madly in love, drunk, or running for office.
    ----- -- ----  -----  -- ------- --- ------
    ioykc rw kxlv, yhbwz, xh hbwwrwa txh xttrqv.

    Free:  b       j      q      x z

    Enter a substitution like 'crypt/plain':
    Do you want to quit? ('y' for yes) y

The example cryptogram was created by running `make_cryptogram.py` on
a computer with `fortune` installed. (But `make_cryptogram.py` only
runs in Python 2; it depends on the `commands` module.)

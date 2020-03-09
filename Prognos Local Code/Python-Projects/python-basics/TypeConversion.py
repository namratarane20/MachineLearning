class Conversion:
    s='Python'
    intNum = 20
    tup = (('a', 1), ('f', 2), ('g', 3))

    converted1 =tuple(s)
    print('string converted to tuple',converted1)
    # o/p=== string converted to tuple ('P', 'y', 't', 'h', 'o', 'n')

    converted2 = list(s)
    print('string converted to list',converted2)
    # o/p=== string converted to list ('P', 'y', 't', 'h', 'o', 'n')

    converted3 = set(s)
    print('string converted to set',converted3)
    # o/p == string converted to set ('P', 'y', 't', 'h', 'o', 'n')

    converted4 = complex(intNum)
    print('integer to converted in to complex=',complex(intNum))
    # o/p ==integer to converted in to complex= (20+0j)

    converted5 = dict(tup)
    print('tuple converted in to Dict',converted5)
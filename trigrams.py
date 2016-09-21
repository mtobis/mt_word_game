defdictpath = "./Dictionaries/"
defdict = "TLW06.txt"

Verbose = True
def trigrams(words):
    """
    gets all initial trigrams from a series of sorted lines, with start and end indices

    array must be sorted prior to call

    >>> data = "abc bcd bcde bcdf bcdfg ghi jkl jklz zzz".split()

    >>> res = trigrams(data)

    >>> for item in sorted(res.keys()): print item, res[item]
    abc (0, 1)
    bcd (1, 5)
    ghi (5, 6)
    jkl (6, 8)
    zzz (8, 9)
    
    """

    oldtrigram = None
    trigram = None
    #result = []
    result = {}
    oldcount = 0
    count = 0
    oldword = "   "            
    for word in words:
        assert word > oldword, "input data is not sorted!"
        oldword = word
        trigram = word[:3]
        if trigram != oldtrigram and len(trigram) == 3:
            if oldtrigram:
                #result.append((oldtrigram,oldcount,count))
                result[oldtrigram] = (oldcount,count)
                oldtrigram,oldcount = trigram, count
            oldtrigram,oldcount = trigram, count
        count += 1
    if trigram:
        #result.append((trigram,oldcount,count)) # get the last one; condition handles empty file
        result[trigram] = (oldcount,count)
    return result

if __name__ == "__main__":
    import optparse # see http://www.alexonlinux.com/pythons-optparse-for-human-beings
    from os.path import isfile

    parser = optparse.OptionParser() 
    parser.add_option('-d', '--wordlist',
                      dest = 'wordlist',
                      help = 'file with list of valid words ["wordlist"]',
                      action = 'store',
                      default = "wordlist")
    parser.add_option('-p', '--wordpath',
                      dest = 'wordpath',
                      help = 'path to file with list of valid words [./]',
                      action = 'store',
                      default = "./")
    parser.add_option('-v', '--.verbose',
                      dest = 'verbose',
                      help = 'print result on exit',
                      action = 'store_true',
                      default = False)
    
    opts,args = parser.parse_args()

    fnam = opts.wordpath+opts.wordlist
    assert isfile(fnam),"word list not found: %s" % fnam

    words = [word.strip().lower() for word in open(fnam).readlines()]
            
    res = trigrams(words)
    if opts.verbose:
        for item in res: print item
    

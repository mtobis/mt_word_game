from string import ascii_lowercase as lcalphas

helptext = """You are looking for dictionary words in this grid, connected horizontally, vertically or diagonally, without reusing a position.
There are %d words in this grid. The longest word has %d letters.

enter your words, one per line
enter _x on a new line when you are done
enter _r to reprint the puzzle grid
enter ? or _h to reprint these instructions
"""



class WordList:
    def __init__(self,wordfile=None):
        """
        create a wordlist

        >>> w = WordList("Dicts/words.txt")

        >>> print w.words[-5:]
        ['zymurgies', 'zymurgy', 'zyzzyva', 'zyzzyvas', 'zzz']

        >>> print w.words[:5]
        ['aa', 'aah', 'aahed', 'aahing', 'aahs']

        # fix these tests
                
        # >>> print [trigram[0] for trigram in w.trigrams[:5]]
        # ['aah', 'aal', 'aar', 'aas', 'aba']
        
        # >>> print [trigram[0] for trigram in w.trigrams[-5:]]
        # ['zyd', 'zyg', 'zym', 'zyz', 'zzz']
        
        >>> w = WordList()

        >>> w = WordList("wordlist")

        >>> w = WordList("no_such_file")
        Traceback (most recent call last):
        IOError: [Errno 2] No such file or directory: 'no_such_file'

        >>> w = WordList(["bar", "foo"])

        >>> print w.words
        ['bar', 'foo']

        """
        if type(wordfile) is list:
            words = wordfile
        else:
            if wordfile is None:
                wordlist = file("wordlist")
            elif type(wordfile) is str:
                wordlist = file(wordfile)
            elif type(wordfile) is file:
                wordlist = wordfile
            else:
                raise ValueError,"invalid word file"
            words = wordlist.readlines()
        
        self.words = [word.strip().lower() for word in words]
        from trigrams import trigrams
        
        self.trigrams = trigrams(self.words)
        self.validTriples = [trigram for trigram in self.trigrams]
        pass
        

class Boggle:
    def __init__(self,data="",x=4,y=4,wordfile=None,scrabble=None):
        """
        creates a Boggle; can pass in file or filename for word list

        >>> print Boggle()
        None
        
        >>> print Boggle("abcdefghijklmnop")
        a b c d 
        e f g h 
        i j k l 
        m n o p 
        <BLANKLINE>

        >>> print Boggle("abcdef~hijklmnop")
        Traceback (most recent call last):
        AssertionError: invalid data
        
        >>> print Boggle("foo")
        Traceback (most recent call last):
        AssertionError: data too short

        >>> print Boggle("_foo")
        Traceback (most recent call last):
        NotImplementedError: unknown distribution

        >>> print Boggle("abcdefg",3,2)
        a b c 
        d e f 
        <BLANKLINE>

        >>> print Boggle(12)
        Traceback (most recent call last):
        TypeError: unrecognized initialization

        >>> b = Boggle("_random")
                
        >>> print Boggle("_randomized")
        d g r z 
        u b o t 
        a e a s 
        e l n e 
        <BLANKLINE>

        >>> b = Boggle("_randomized")

        >>> for item in b.triplets[12:18]: print item
        (0, 5, 8)
        (0, 5, 9)
        (0, 5, 10)
        (1, 0, 4)
        (1, 0, 5)
        (1, 2, 3)

        >>> b = Boggle("_randomized",wordfile="Dicts/words.txt")
        
        >>> for item in b.triplets[12:18]: print item
        (0, 5, 8)
        (0, 5, 9)
        (0, 5, 10)
        (1, 0, 4)
        (1, 0, 5)
        (1, 2, 3)

        # >>> print b.wordlist.trigrams[-2:]
        # [('zyz', 178688, 178690), ('zzz', 178690, 178691)]

        >>> for k in sorted(b.wordlist.trigrams.keys())[-2:]:
        ...     print k, b.wordlist.trigrams[k]
        zyz (178688, 178690)
        zzz (178690, 178691)

        >>> for k in sorted(b.wordlist.trigrams.keys())[:2]:
        ...     print k, b.wordlist.trigrams[k]
        aah (1, 5)
        aal (5, 9)

        # >>> print b.wordlist.trigrams[:2]
        # [('aah', 1, 5), ('aal', 5, 9)]

        >>> print sorted(b.candidates.keys())[:5]
        ['aba', 'abd', 'abe', 'abo', 'abr']

        # ['aba', 'aba', 'abd', 'abd', 'abe']

        >>> print b.candidates["abd"]
        [(8, 5, 0), (10, 5, 0)]
        
        >>> print b.solutions
        []

        # working on this
        
        """
        from string import lowercase
        from adjacency import adjacency, triplets, newseqs

        # 36
        vowels="aaeeeeiiooou"
        if scrabble is None:
            scrabble = ("aaaa" +
                    "bb" +
                    "cc" +
                    "ddddd" +
                    "eeeeeeeee" +
                    "ff" +
                    "ggg" +
                    "hh" +
                    "iiiiii" +
                    "j" +
                    "k" +
                    "llll" +
                    "mm" +
                    "nnnnnn" +
                    "oooooo" +
                    "ppp" +
                    "rrrrrr" +
                    "ssssss" +
                    "tttttt" +
                    "uuu" +
                    "v" +
                    "ww" +
                    "x" +
                    "yy" +
                    "z"
                    )
                
        self.x = x 
        self.y = y
        self.dim = dim = x * y
        self.adjacent = adjacency(x,y)
        #import pdb; pdb.set_trace()

        
        self.triplets = triplets(self.adjacent)
        self.solutions = []
        #self.mat = [[0 for i in range(dim)] for j in range(dim)]
        
        if not data:
            self.data = None
        else:
            try:
                if data[0] in lowercase:
                    assert len(data) >= x * y,"data too short"
                    for index in range(dim):
                        assert data[index] in lowercase,"invalid data"
                    self.data = data[:dim]
                elif data[0] == "_":
                    if data.startswith("_random"):
                        from random import seed, choice
                        if len(data) == len("_random"): #true random if data == "_random"
                            seed(None)
                        else:
                            rseed = data[len("_random"):] # seed is whatever follows "_random"
                            seed(rseed)
                        data = []
                        for i in range(dim):
                            data.append(choice(scrabble))
                        self.data = "".join(data)
                    else:
                        raise NotImplementedError,"unknown distribution"
                else:
                    raise ValueError,"unrecognized initialization"
            except TypeError:
                raise TypeError,"unrecognized initialization"

        self.wordlist = WordList(wordfile)
        self.candidates = self.validtriplets()
        #self.solve()

    def __str__(self):
        repr = []
        index = 0
        if self.data is None:
            return str(None)
        if self.data.startswith("_"):
            return self.data[1:]
        for row in range(self.y):
            for col in range(self.x):
                repr += [self.data[index]," "]
                index += 1
            repr += "\n"
        return "".join(repr)

    def validtriplets(self,wordlist=None):
        "checks which triplets have matches in the wordlist"
        
        if wordlist is None: wordlist = self.wordlist
        mytrigram = {}
        myranges = {}
        for triplet in self.triplets:
            a,b,c = triplet
            data = self.data
            if data:
                testTriple = "" + data[a] + data[b] + data[c]
                if testTriple in wordlist.validTriples:
                    mytrigram.setdefault(testTriple,[]).append(triplet)
        return mytrigram

         
    def solve(self, wordlist = None, Verbose=False):
        """
        find all valid words in the boggle
        
        """
        from time import clock

        t1 = clock()

        def iteration(candidate,sequence,wordsublist):
            """
            for a candidate sequence, add it if it's a word

            recursive call looking for each character in the wordlist
            """

            from adjacency import newseqs
                        
            result = []
            if candidate in wordsublist:
                result.append(candidate)
            newseqlist = newseqs(self.adjacent,sequence)
            
            for newseq in newseqlist:
                newcand = candidate + self.data[newseq[-1]]
                newsublist = [word for word in wordsublist if word.startswith(newcand)]
                if newsublist: 
                    r = iteration(newcand,newseq,wordsublist)
                    if r:
                        result += r
            return result

        words = self.wordlist.words
        trigrams = self.wordlist.trigrams
        
        redundantSolutions = []
        
        c = self.candidates
                 
        for triplet in sorted(c.keys()):
            r1,r2 = trigrams[triplet]
            for sequence in c[triplet]:
                redundantSolutions += iteration(triplet,sequence,words[r1:r2])

        self.solutions = sorted([item for item in set(redundantSolutions)])
        t2 = clock()
        if Verbose: print t2 - t1

def printlist(mylist):
    count = 0
    for item in mylist:
        count += 1
        Item = item
        if len(item) > 6:
            Item = item.upper()
            print Item,"\t",
        else:
            print item,"\t\t",
        if not count % 5: print
    print
                    
if __name__ == "__main__":

        from sys import argv


        
        
        """
        if not len(argv) > 1:
            
        seed = "_random"
        """
        
        
        if len(argv) < 2:
            seed = "_random"
        else:
            seed = argv[-1]
        b=Boggle(seed,wordfile="Dicts/words.txt")
        print "\n",
        
        ######
        ######

        if len(argv) == 1:
            fnam = ".bogglerc"
        else:
            fnam = argv[1]

        with file(fnam) as runparams:
            #import pdb; pdb.set_trace()
            text = runparams.read()
            px = eval(text)
            print px
        b = Boggle(px["data"],px["x"],px["y"],px["wordfile"])

        
        ######
        ######

                
        print b
        b.solve()
        
        maxlen = max([len(item) for item in b.solutions])
        print helptext % (len(b.solutions),maxlen)
        
        a = ""
        myanswers = []
        while True:
            if a.startswith("_x"):
                break
            if(a):
                if a.startswith("_r"):
                    print b
                elif a.startswith("?") or a.startswith("_h"):
                    print b
                    print helptext % (len(b.solutions),maxlen)
                else:
                    a = a.strip().lower()
                    if a.isalpha():
                        if a in myanswers:
                            print "duplicate entry, ignored"
                        else:
                            myanswers.append(a)
                    else:
                        badchars = ''.join([ch for ch in a if ch not in lcalphas])
                        print "bad character(s) '%s' in string '%s', entry ignored" % (badchars,a)
            a = raw_input("> ")
  
        count = 0
        got = [answer for answer in myanswers if answer in b.solutions]

        print "\n",b
        print "\n You found:"
        printlist(got)
        missed = [answer for answer in b.solutions if answer not in myanswers]

        print "\n You missed:"
        printlist(missed)

        print "\n You found %s out of %s solutions." %(len(got),len(b.solutions))

        # might be better to separate out the non-words and the invalid paths on the fly
        # but would add complexity
        
        # note that b is clobbered here, assuming no further use of it

        dubious = [answer for answer in myanswers if answer not in b.solutions]
        if dubious:            
            b.wordlist = WordList(sorted(dubious)) #looking for the unfound entries in the grid
            b.candidates = b.validtriplets() 
            b.solve()
            disputed = b.solutions # this yields a list of sequences that don't match the wordlist but are valid paths in the matrix 
            if disputed:
                print "\n Disputed:"
                printlist(disputed)
            bogus = [item for item in dubious if not item in disputed] # the residual just aren't real sequences
            if bogus:
                print "\n Not valid in this grid:"
                printlist(bogus)

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
    def __init__(self,data="",x=4,y=4,wordfile=None):
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

        vowels="aaeeeeiiooou"
        scrabble = ("aaaa" +
                    "bb" +
                    "cc" +
                    "ddddd" +
                    "eeeeeeeee" +
                    "ff" +
                    "ggg" +
                    "hh" +
                    "iiii" +
                    "j" +
                    "k" +
                    "llll" +
                    "mm" +
                    "nnnnnn" +
                    "oooo" +
                    "ppp" +
                    "rrrrrr" +
                    "ssssss" +
                    "tttttt" +
                    "uu" +
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

        #print self.adjacency
        
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
                        if len(data) == len("_random"): #true random
                            seed(None)
                        else:
                            rseed = data[len("_random"):]
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
        if wordlist is None: wordlist = self.wordlist
        Verbose = False
        mytrigram = {}
        import collections
        #mytrigram = collections.defaultdict(list)
        myranges = {}
        for triplet in self.triplets:
            a,b,c = triplet
            data = self.data
            if data:
                testTriple = "" + data[a] + data[b] + data[c]
                #print testTriple
                #import pdb; pdb.set_trace()
                if testTriple in wordlist.validTriples:
                    #mytrigram[triplet] = testTriple
                    #mytrigram[testTriple] = triplet
                    mytrigram.setdefault(testTriple,[]).append(triplet)
                    
                    if Verbose: print triplet, testTriple
                else:
                    if Verbose: print "NOT " + testTriple
        if Verbose:
            print type(mytrigram)
        return mytrigram


    """
    def isvalid(self,sequence):
        pass
    """
         
    def solve(self, wordlist = None, Verbose=False):
        """
        find all valid words in the boggle
        
        """
        from time import clock

        t1 = clock()

        def iteration(candidate,sequence,wordsublist):
            """
            for a candidate sequence, add it if it's a word, and
            """
            
            result = []
            if candidate in wordsublist:
                #print "FOUND!!!" + candidate   #, sequence
                result.append(candidate)
            #else:
            #    print "NOT " + candidate
            from adjacency import newseqs
            newseqlist = newseqs(self.adjacent,sequence)
            #import pdb;pdb.set_trace()
            
            for newseq in newseqlist:
                newcand = candidate + self.data[newseq[-1]]
                #print newcand
                newsublist = [word for word in wordsublist if word.startswith(newcand)]
                if newsublist: 
                    r = iteration(newcand,newseq,wordsublist)
                    if r:
                        result += r
            return result

        if wordlist is None:
            wordlist = self.wordlist
        
        words = self.wordlist.words
        trigrams = self.wordlist.trigrams
        
        #self.solutions = []

        redundantSolutions = []
        
        c = self.candidates
                 
        for triplet in sorted(c.keys()):
            r1,r2 = trigrams[triplet]
            for sequence in c[triplet]:
                #import pdb; pdb.set_trace()
                redundantSolutions += iteration(triplet,sequence,words[r1:r2])

        self.solutions = sorted([item for item in set(redundantSolutions)])
        t2 = clock()
        if Verbose: print t2 - t1

'''def solveSequence(self,sequence,data,adjacency,wordlist,range):
    """ recursively finds all valid sequences """

    # results = [] (or a set)

    # if sequence in wordlist and sequence not in results add sequence to set

    # get extensions to sequence

    # if valid extension, solveSequence on it
'''

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
    Debug = False
    if Debug:
        b = Boggle("_randomized",wordfile="Dicts/words.txt")
        print b
        b.solve(1)

        print "\n%d solutions found\n" % len(b.solutions)
        #count = 0
        for item in b.solutions:
            count += 1
            Item = item
            if len(item) > 6: Item = item.upper()
            print Item,"\t",

            if not count % 5: print
        print
    else:
        from sys import argv
        #print len(argv)
        if len(argv) < 2:
            seed = "_random"
        else:
            seed = argv[-1]
        b=Boggle(seed,wordfile="Dicts/words.txt")
        print 5 * "\n"
        print b
        b.solve()
        print "there are", len(b.solutions), "words in this Boggle"
        print "enter your words, one per line"
        print "enter _x on a new line when you are done"
        
        a = ""
        myanswers = []
        while not a.startswith("_x"):
            if(a): myanswers.append(a)
            a = raw_input("> ")
  
        count = 0
        solutions = b.solutions
        got = [answer for answer in myanswers if answer in solutions]
        print "\n You found:"
        printlist(got)
        missed = [answer for answer in solutions if answer not in myanswers]
        #import pdb; pdb.set_trace()
        print "\n You missed:"
        printlist(missed)
        dubious = [answer for answer in myanswers if answer not in solutions]
        if dubious:
            # print "\n Disputed or bogus:"
            # printlist(dubious)

            # set up tests

            # avoid clobbering b here (?) YAGNI (?)
            
            b.wordlist = WordList(sorted(dubious)) #looking for words in this dictionay
            b.candidates = b.validtriplets() #looking for valid initial sequences
            b.solve()
            disputed = b.solutions
            if disputed:
                print "\n Disputed:"
                printlist(disputed)
            bogus = [item for item in dubious if not item in disputed]
            if bogus:
                print "\n Bogus:"
                printlist(bogus)

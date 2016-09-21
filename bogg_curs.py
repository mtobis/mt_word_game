import curses

#global debugstr
debugstr = "fare thee well\n"

def draw1(screen,boggle=None):
    global debugstr
    from string import ascii_letters as alphas

    results = []
    
    maxcount = 20
    count = 0
    
    curses.start_color() 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW) 

    screen.bkgd(curses.color_pair(1))
    curses.curs_set(1)
    screen.addstr(1,12,"enter your words here:")
    screen.refresh() 

    win = curses.newwin(6, 9, 2, 2) 
    win.bkgd(curses.color_pair(2)) 
    win.box()
    if boggle is None:
        win.addstr(1, 1, "T O B I")
        win.addstr(2, 1, "S S B O")
        win.addstr(3, 1, "G G L E")
        win.addstr(4, 1, "G A M E")
    else:
        for i in range(4):
            win.addstr(i+1,1," ".join(boggle.upper()[4*i:4*i+4]))
    win.noutrefresh() 

# ************************
    
    inwin = 6 * [None]

    for index in range(5):
        inwin[index] = curses.newwin(20, 10, 2, 12 + 12 * index)
        win2 = inwin[index]
        #win2 = curses.newwin(20, 10, 2, 20)
        inwin[index].idlok(1)
        inwin[index].scrollok(1)
        inwin[index].bkgd(curses.color_pair(3)) 
        #win2.box() 
        #win2.addstr(0, 0, "\n")
        inwin[index].refresh()

    #screen.move(10,5)

    this = 0
    count = 0
    
    win2 = inwin[this]

    screen.refresh()

    lineno = 0
    win2.move(lineno,1)
    win2.refresh()

    curses.echo()
    done = False
    
    while not done:
        line = win2.getstr()
        y,x = win2.getyx()

        #error recovery broken if length > window width
        
        if (len(line.strip())):
            done = ord(line[0]) == 27
            word = line.strip()
            try:
                for ch in word:
                    assert ch in alphas
                count += 1
                if word not in results:
                    results.append(word.lower())
                win2.move(y,x+1)
            except AssertionError:
                win2.addstr(y-1,x+1,"            ")
                win2.move(y-1,x+1)
        else:
            win2.move(y-1,x+1)
        win2.refresh()

    report = ""
    linelen = 0
    linemax = 53
    for result in sorted(results):
        if linelen + len(result) < linemax:
            report += result + " "
            linelen += len(result) + 1
        else:
            linelen = len(result) + 2
            report += "\n " + result + " "
    report += "\n\n HIT RETURN KEY TO SEE YOUR RESULTS"


    

# ***********************
    """
    #screen.addstr(1,12,"enter your words here:")
    screen.addstr(1,12,"you entered:          ")
    screen.refresh()

    win3 = curses.newwin(20, 55, 2, 12)
    win3.bkgd(curses.color_pair(3))
    win3.addstr(1,1,report)
    win3.refresh()
    line = win3.getstr()
    debugstr += "\n"
    """
    return results
    
#def draw2(screen,report,boggle=None):
def draw2(screen,boggle=None):
    global debugstr
    from string import ascii_letters as alphas

    results = []
    
    maxcount = 20
    count = 0
    
    curses.start_color() 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW) 

    screen.bkgd(curses.color_pair(1))
    curses.curs_set(1)
    screen.addstr(1,12,"enter your words here:")
    screen.refresh() 

    win = curses.newwin(6, 9, 2, 2) 
    win.bkgd(curses.color_pair(2)) 
    win.box()
    if boggle is None:
        win.addstr(1, 1, "T O B I")
        win.addstr(2, 1, "S S B O")
        win.addstr(3, 1, "G G L E")
        win.addstr(4, 1, "G A M E")
    else:
        raise NotImplementedError,"working on this"
    win.noutrefresh() 

    """    
    inwin = 6 * [None]

    for index in range(5):
        inwin[index] = curses.newwin(20, 10, 2, 12 + 12 * index)
        win2 = inwin[index]
        #win2 = curses.newwin(20, 10, 2, 20)
        inwin[index].idlok(1)
        inwin[index].scrollok(1)
        inwin[index].bkgd(curses.color_pair(3)) 
        #win2.box() 
        #win2.addstr(0, 0, "\n")
        inwin[index].refresh()

    #screen.move(10,5)

    this = 0
    count = 0
    
    win2 = inwin[this]

    screen.refresh()

    lineno = 0
    win2.move(lineno,1)
    win2.refresh()

    curses.echo()
    done = False
    
    while not done:
        line = win2.getstr()
        y,x = win2.getyx()

        #error recovery broken if length > window width
        
        if (len(line.strip())):
            done = ord(line[0]) == 27
            word = line.strip()
            try:
                for ch in word:
                    assert ch in alphas
                count += 1
                if word not in results:
                    results.append(word.lower())
                win2.move(y,x+1)
            except AssertionError:
                win2.addstr(y-1,x+1,"            ")
                win2.move(y-1,x+1)
        else:
            win2.move(y-1,x+1)
        win2.refresh()

    report = ""
    linelen = 0
    linemax = 53
    for result in sorted(results):
        if linelen + len(result) < linemax:
            report += result + " "
            linelen += len(result) + 1
        else:
            linelen = len(result) + 2
            report += "\n " + result + " "
    report += "\n\n HIT RETURN KEY TO SEE YOUR RESULTS"
    """

    formreport = "\n".join(report) #placeholder for formattin

    screen.addstr(1,12,"you entered:          ")
    screen.refresh()

    win3 = curses.newwin(20, 55, 2, 12)
    win3.bkgd(curses.color_pair(3))
    win3.addstr(1,1,formreport)
    win3.refresh()
    line = win3.getstr()
    debugstr += "\n"    
    
def main(screen):
    draw1(screen)

if __name__ == "__main__":
    try: 
        report = curses.wrapper(draw1,"SOMEBODYELSESFIX")
        print debugstr
        a = raw_input("> ")
        curses.wrapper(draw2,report)
    except KeyboardInterrupt: 
        print "Got KeyboardInterrupt exception. Exiting..." 
        exit() 

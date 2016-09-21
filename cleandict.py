inwords = file("Dicts/words").readlines()
outwords = [word for word in inwords if word.islower() and len(word.strip()) > 2]
outfile = file("Dicts/words.txt","w")
outdata = "".join(outwords)
outfile.write(outdata)

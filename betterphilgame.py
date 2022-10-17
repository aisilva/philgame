#A program that plays the Wikipedia Philosophy game given a URL
from urllib2 import *
from re import *
titles = []

def f():
	baseurl = 'http://en.wikipedia.org/wiki/'
	c = raw_input(baseurl)
	return baseurl + c
	#For this to work, call philgame(f())

def counter(part, whole):
	counter = 0
	t = 0
	if len(part) == 1:
		for x in whole:
			if x == part:
				counter += 1
	elif len(part) > 1:
		while t + len(part) <= len(whole):
			if whole[t:len(part)+t] == part:
				counter += 1
			t += 1
	return counter

def philgame(c):
	global titles
	if c[0:29] != 'http://en.wikipedia.org/wiki/':
		print 'That\'s not a valid Wikipedia URL. Try http:// instead of https://.'
	else:
		if '#' in c:
			c = c[0:c.index('#')]
		x = urlopen(c)
		for line in x:
                        #print page title
			if "<title>" in line:
				template = ur"\<title\>\s?(.*?)\s?\</title\>"
				title = findall(template, line)
				title = ' '.join(title)
				#title = title[0:(len(title)-35)] #Gets rid of the part saying 'Wikipedia - the free encyclopedia'
				print title
				if title in titles:
					x.close()
					return 'LOOPED'
				elif title == 'Philosophy' and len(titles) == 0:
					titles = []
					print 'What? It\'s PHILOSOPHY?!'
					return None
				else:
					titles.append(title)
					break
		for line in x:
                        #search all lines for a next link. Next link needs to be in normal text and outside parentheses
			if '<p>' in line and '<a href=' in line and 'font-size:' not in line:

                                #temp = ur"(?<!\() \<a href=\"(.+?)\""#first part makes sure there's no open paren right before
				#second part takes all between <a href=" and "
				temp = ur"\<a href=\"(.+?)\""
				links = findall(temp, line)
                                
                                delims_list = [ ('(', ')'), ('<i>', '</i>'), ('<b>', '</b>'), ('<small', '</small'), ('[', ']') ]
				for link in links:
                                        #for delims in delims_list:
                                        if False not in [counter(delims[0], line[0:line.index(link)]) == counter(delims[1], line[0:line.index(link)]) for delims in delims_list]:
                                                #pass
                                                


                                        
                                        #if counter('(', line[0:line.index(link)]) == counter(')', line[0:line.index(link)]) and counter('<i>', line[0:line.index(link)]) == counter('</i>', line[0:line.index(link)]) and counter('<small', line[0:line.index(link)]) == counter('</small', line[0:line.index(link)]) and counter('<b>', line[0:line.index(link)]) == counter('</b>', line[0:line.index(link)]):


                                        
                                                nexturl = 'http://en.wikipedia.org' + link
                                                
						if '#' in nexturl:
							if link[0] == '#':
                                                                #invalid link, I believe
								continue
							else:
								nexturl=nexturl[0:nexturl.index('#')]
                                                                
						if link[0:16].lower() != '/wiki/philosophy':
							if 'redlink=1' in nexturl or 'wikimedia' in nexturl or link[6:11] == 'Help:' or nexturl == c:
                                                                #very ad hoc
								continue
                                                        
							else:
                                                                x.close()
								return philgame(nexturl)
						else:
							print 'Philosophy'
							x.close()
							if len(titles) != 1:
								print 'It took %d steps to get to Philosophy.' % (len(titles))
							else:
								print 'It took 1 step to get to Philosophy.'
							titles = []
							return None
philgame(f())

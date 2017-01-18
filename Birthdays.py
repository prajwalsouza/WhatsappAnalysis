import re
import operator


#opening the file

from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()  #Tkinter dialog box helps select the file

filename = askopenfilename() 

infile = open(filename, 'r')

print(" File Selected : %s" % filename) 

msglist=[]		#this list will contain dictionary of each message

badwords=[
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* was added$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* were added$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* added .*$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* left$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* was removed$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* changed to \+.*'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* created group .*'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d \w\w .* Messages you send to this chat and calls are now secured with end-to-end encryption.')
]

msgnumber = 0

for aline in infile.readlines():
	if any(badword.match(aline) for badword in badwords): #this will skip unwanted messages
		continue
	msg={}
	isNewMsg=re.search(r'^(\d?\d)/(\d?\d)/(\d\d), (\d?\d:\d?\d \w\w) - (.*?): (.*)',aline) #regex matching a new message line
	if isNewMsg:
		#add everything to a dictionary
		msgnumber = msgnumber + 1
		msg['index'] = msgnumber
		msg['month'] = isNewMsg.group(1)
		msg['date'] = isNewMsg.group(2)
		msg['year'] = isNewMsg.group(3)
		msg['time'] = isNewMsg.group(4)
		msg['sender'] = isNewMsg.group(5)
		msg['message'] = isNewMsg.group(6)
		msglist.append(msg)
	else:		#if it is not a new message line then it is part of the previous message so append to that
		msg=msglist.pop()
		msg['message']+=aline
		msglist.append(msg)

print(" Number of messages in this conversation: "+str(len(msglist)))
print("")

#Find a Phrase 

findword = ["Happy Birthday"]

wordcount = 0

wordlist = []

for msg in msglist:
	for phrase in findword:
		nphrases=re.findall(phrase,msg['message'],re.IGNORECASE)


	if(nphrases):
		wordcount+=len(nphrases)
		nwords = re.search(phrase + r'\W(\w+)',msg['message'],re.IGNORECASE)
		if nwords:
			word = {}
			word['index'] = msg['index']
			word['date'] = msg['date']
			word['month'] = msg['month']
			word['year'] = msg['year']
			word['time'] = msg['time']
			word['sender'] = msg['sender']
			word['associated word'] = nwords.group(1)
			wordlist.append(word)

    
print(" Number of phrases : %d." % wordcount)


# Removing Duplicates using difflib
import difflib

wishthreshold = 2 #The minimum number of wishes that confirm a birthday.

wordfilter = ['to','bro','dude','boss','babe','bebe','dear','maam','maams','both']



import itertools
awordfreq={}

#We find the frequency with which each word repeats
for worditem in wordlist:
	if worditem['associated word'] in awordfreq:
		awordfreq[worditem['associated word']]+=1
	else:
		awordfreq[worditem['associated word']]=1

adatefreq={}
#We find the frequency with which each word with a given date repeats
for worditem in wordlist:
	if worditem['associated word']+worditem['date']+worditem['month'] in adatefreq:
		adatefreq[worditem['associated word']+worditem['date']+worditem['month']]+=1
	else:
		adatefreq[worditem['associated word']+worditem['date']+worditem['month']]=1


#Finds possible duplicates and deletes them.
for worditem1,worditem2 in itertools.combinations(wordlist, 2):
	if(worditem1 != worditem2):
		associatedword1 = worditem1['associated word']
		associatedword2 = worditem2['associated word']
		date1 = worditem1['date']
		month1 = worditem1['month']
		date2 = worditem2['date']
		month2 = worditem2['month']	
		if(date1 == date2 and month1 == month2  and difflib.SequenceMatcher(None,associatedword1.lower(),associatedword2.lower()).ratio() > 0.3 and awordfreq[associatedword1] <= 1 and awordfreq[associatedword2] <= 1):
			if(awordfreq[associatedword1] >= awordfreq[associatedword2]):
				if worditem2 in wordlist:
					wordlist.remove(worditem2)
					print("Deleted 1 %s" % associatedword2)
					if(associatedword1 != associatedword2):
						awordfreq[associatedword1] = awordfreq[associatedword1] + awordfreq[associatedword2] 
			if(awordfreq[associatedword1] < awordfreq[associatedword2]):
				if worditem1 in wordlist:
					wordlist.remove(worditem1)
					print("Deleted 2 %s" % associatedword1)
					if(associatedword1 != associatedword2):
						awordfreq[associatedword2] = awordfreq[associatedword1] + awordfreq[associatedword2] 
		if(difflib.SequenceMatcher(None,associatedword1.lower(),associatedword2.lower()).ratio() > 0.6):
			if(adatefreq[associatedword1+date1+month1] >= adatefreq[associatedword2+date2+month2]):
				if worditem2 in wordlist:
					wordlist.remove(worditem2)
					print("Deleted 3 %s" % associatedword2)
			if(adatefreq[associatedword1+date1+month1] < adatefreq[associatedword2+date2+month2]):
				if worditem1 in wordlist:
					wordlist.remove(worditem1)
					print("Deleted  4 %s" % associatedword2)
	if associatedword2.lower() in wordfilter:
		if worditem2 in wordlist:
				wordlist.remove(worditem2)
				print("Deleted 5 %s" % associatedword2)
	if associatedword1.lower() in wordfilter:
		if worditem1 in wordlist:
				wordlist.remove(worditem1)
				print("Deleted 6 %s" % associatedword1)
	if len(associatedword2) <= 1:
		if worditem2 in wordlist:
				wordlist.remove(worditem2)
				print("Deleted 7 %s" % associatedword2)
	if len(associatedword1) <= 1:
		if worditem1 in wordlist:
				wordlist.remove(worditem1)
				print("Deleted 8 %s" % associatedword1)
	if  awordfreq[associatedword2] < wishthreshold:
		if worditem2 in wordlist:
				wordlist.remove(worditem2)
				print("Deleted 9 %s" % associatedword2)
	if  awordfreq[associatedword1] < wishthreshold:
		if worditem1 in wordlist:
				wordlist.remove(worditem1)
				print("Deleted 10 %s" % associatedword1)
    

# We print the data we acquired

from datetime import date

print("")
print(" Based on the Analysis : ")
for worditem in wordlist:
	worddate = worditem['date']
	wordmonth = worditem['month']
	associatedword = worditem['associated word']
	forstringassociatedword = associatedword[:1] .upper() + associatedword[1:].lower()
	stringdate = date(day=int(worddate), month=int(wordmonth), year=2016).strftime('%d %B')

	for word in findword:
		print(" %s celebrates birthday on %s and got atleast %d wishes." % (forstringassociatedword,stringdate,awordfreq[associatedword]))

print("")
print(" Number of Birthdays found : %d." % len(wordlist))

import feedparser
import time
import datetime
from pytz import timezone
import requests
import smtplib
import json



start = time.time()
toAddress = ['abcd@zohomail.com']
emailId = 'abcd@gmail.com'
emailIdPassword = 'password'
fromAddress = emailId
topicOfInterest = ['']
feedURL = 'http://feeds.abcd.com/abcd'

parsedFeed = feedparser.parse(feedURL)

#getting UTC time and calculating Pacific daylight time and reformatting it to feeds time format
getUTCTime = datetime.datetime.now(timezone('UTC'))
getPDT = getUTCTime-datetime.timedelta(hours=7,minutes=0) #get your desired timezone by subtracting or adding to UTC time here
PDT= getPDT.strftime('%a, %d %b %Y %H:%M:%S')
realPDT = datetime.datetime.strptime(PDT,'%a, %d %b %Y %H:%M:%S')

#the time range used to iterate only feeds that were upated last 15 minutes and aws lambda time trigger set to every 15 minutes
thresholdTime = getPDT-datetime.timedelta(minutes=15) #set your time range here, here it is 15 minutes
stringThreshold = thresholdTime.strftime('%a, %d %b %Y %H:%M:%S')
timeRange = datetime.datetime.strptime(stringThreshold,'%a, %d %b %Y %H:%M:%S')

#smtplib server initiation (Gmail)
ser=smtplib.SMTP_SSL('smtp.gmail.com',465)
ser.ehlo()
ser.login(emailId,emailIdPassword)

#iterating through feeds and mail the topicOfInterest (relevant feeds) to toAddress
i=0
while i<len(parsedFeed.entries):
    EntryDate = datetime.datetime.strptime(parsedFeed.entries[i].published[0:25],'%a, %d %b %Y %H:%M:%S')
    if timeRange<EntryDate:
        for s in topicOfInterest:
            print(parsedFeed.entries[i].title)
            if s in parsedFeed.entries[i].title:
                print('got item\n')
                ex1 = parsedFeed.entries[i].summary.index('<')
                body1 = parsedFeed.entries[i].summary[:ex1]
                body2 = parsedFeed.entries[i].link
                sub = parsedFeed.entries[i].title
                msg = 'Subject: {}\n{}\n\n{}'.format(sub,body1,body2)
                ser.sendmail(fromAddress,toAddress,msg)
                print('mail sent\n')
    i=i+1
ser.quit()
end = time.time()
print(end-start)

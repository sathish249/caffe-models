#!/usr/bin/python
import sys
from datetime import datetime
from datetime import timedelta

if len(sys.argv) < 2:
   print "Usage: ", sys.argv[0], " caffe_log_file"
   exit()

log_file = sys.argv[1]
start_time=""
iter_count=""
iter_accuracy=""
iter_time=""
prev_time=""
add_days=0

with open(log_file) as fp:
   for line in fp:
       if "Starting Optimization" in line:
         #parse the line.
         words = line.split()
         #print words
         start_time=datetime.strptime(words[1], '%H:%M:%S.%f')
         print "start_time=", start_time
         prev_time=start_time
       elif "Test" in line and "net" in line and '(#0)' in line:
         # there can be 2 types..
#I0617 01:53:21.819911  7709 solver.cpp:337] Iteration 24000, Testing net (#0)
#I0617 01:56:16.498755  7709 solver.cpp:404]     Test net output #0: loss1/loss1 = 3.95918 (* 0.3 = 1.18775 loss)
#I0617 01:56:16.498867  7709 solver.cpp:404]     Test net output #1: loss1/top-1 = 0.20236
#I0617 01:56:16.498880  7709 solver.cpp:404]     Test net output #2: loss1/top-5 = 0.43328
           words = line.split()
           #print words[4], words[8]
           if words[4] == "Iteration":
               #print words[5]
               iter_count = words[5]
               iter_accuracy = ""
               iter_time = ""
       elif "accuracy" in line and "net" in line and '#0' in line:
           words2 = line.split()
           #print words2[8]
           if words2[8] == "accuracy@1":
               iter_accuracy = words2[10]
           iter_time=datetime.strptime(words[1], '%H:%M:%S.%f')
           if prev_time > iter_time:
               add_days=add_days+1
               # debug print "days added=", add_days
           iter_time=iter_time + timedelta(days=add_days)
           # print "Time=", iter_time-start_time, ",Count=", iter_count, ", accuracy=", iter_accuracy
           x = iter_time-start_time
           hours = x.days * 24 + x.seconds // 3600
           minutes =  (x.seconds % 3600) // 60
           # print  iter_time-start_time, ",",  iter_accuracy, ",", iter_count
           # print  hours, ":", minutes,  iter_time-start_time, ",",  iter_accuracy, ",", iter_count
           print  "%02d:%02d, %s, %s" % (hours, minutes,  iter_accuracy, iter_count)
           prev_time=datetime.strptime(words[1], '%H:%M:%S.%f')
        


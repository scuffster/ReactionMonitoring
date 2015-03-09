#!/usr/bin/env python
# sample code to take reading from ADC and post to Grovestrem dashboard
# DScuffell, March 2015
#
import time
import datetime
import httplib
import random
import urllib
 
 
if __name__ == '__main__':
   
    #GroveStreams Settings
    api_key = "ds5152bfd3-0af3-3951-b93a-d9e137ecfc6b"    #Change This to the api key on your grovestreams account!!!
   
    component_id = "Godrick RPI" #change this to your component (device) name
    base_url = '/api/feed?'
   
    conn = httplib.HTTPConnection('www.grovestreams.com')
   
    while True:
       
        sensor1_val = random.randrange(-10, 40) #replace this with the reading from the thermocouple 
        sensor2_val = random.randrange(0, 100) # replace this with reading from another sensor
       
        #Upload the feed
        try:    
            #Let the GS servers set the sample times. Encode parameters
            url = base_url + urllib.urlencode({'compId' : component_id,
                                               'temperature' : sensor1_val,
                                               'sensor2' : sensor2_val})
           
           
            #The api_key token passed as  a cookie in the html header
            headers = {"Connection" : "close", "Content-type": "application/json",
                       "Cookie" : "api_key="+api_key}
           
            print('Uploading feed to: ' + url)
           
            conn.request("PUT", url, "", headers)
           
            #Check for errors
            response = conn.getresponse()
            status = response.status
           
            if status != 200 and status != 201:
                try:
                    if (response.reason != None):
                        print('HTTP Failure Reason: ' + response.reason + ' body: ' + response.read())
                    else:
                        print('HTTP Failure Body: ' + response.read())
                except Exception:
                    print('HTTP Failure Status: %d' % (status) )
       
        except Exception as e:
            print('HTTP Failure: ' + str(e))
       
        finally:
            if conn != None:
                conn.close()
       
        #Pause for 12 seconds -Grovesteams limits readings to 10 seconds apart when using this url posting approach 
        time.sleep(12)
 
    # quit
    exit(0)

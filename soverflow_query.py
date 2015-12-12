''' This file has parameters to query stack overflow and produce summaries.
    Given a list of user IDs and a timeframe, it produces a summary of:
    1. reputation change during that time (per user)
    2. The number of questions asked
    3. The number of questions answered.
'''
import json
import urllib2,urllib
import time
import zlib
import pprint
import argparse

base_url = 'http://api.stackexchange.com/2.2'

def requestStackOverflowData(url):
    req = urllib2.Request(url,headers={'Accept-Encoding': 'gzip,identity'})
    resp = urllib2.urlopen(req)
    text =  resp.read()
    gzip =("gzip" == resp.headers.getheader('Content-Encoding'))
    #print gzip
    if gzip:
        text = zlib.decompress(text,15+32)
    return json.loads(text)

def requestUsersData(uids,site):
    users = "%s/users/%s?order=desc&sort=reputation&site=%s"%(base_url,uids,site)
    return requestStackOverflowData(users)
    

def requestPostData(uids,site,from_dt,to_dt):
    post_data = "%s/users/%s/posts?fromdate=%s&todate=%s&order=desc&sort=activity&site=%s"%(base_url,uids,from_dt,to_dt,site)
    return requestStackOverflowData(post_data)


def requestAllReputationPages(uids,from_dt,to_dt,site,page_size):
    more = True
    page=0
    items = {"items":[]}
    while (more):
        page=page+1
        reputation="%s/users/%s/reputation-history?fromdate=%s&todate=%s&site=%s&pagesize=%s&page=%s"%(base_url,uids,from_dt,to_dt,site,page_size,page)
        #print reputation
        jRep = requestStackOverflowData(reputation)
        more = jRep["has_more"]
        items["items"].extend(jRep["items"])
    #print "Number of pages:",page
    return items
        
    

def summary(uids,from_dt,to_dt,site="stackoverflow",page_size="100"):
    jRep = requestAllReputationPages(uids,from_dt,to_dt,site,page_size)
    jUsers = requestUsersData(uids,site)
    jActivity = requestPostData(uids,site,from_dt,to_dt)
    return addUsers(summarize(jActivity,summarize(jRep)),jUsers)
    
 
def summarize(aResp,summ={}):
    items = aResp["items"]
    #pprint.pprint(aResp)
    for item in items:
        if item.has_key("reputation_change"):
            user_id = item["user_id"]
            reputation_change = item["reputation_change"]
            post_type = item["reputation_history_type"]
            if summ.has_key(user_id):
                summ[user_id]["reputation_change"] = summ[user_id]["reputation_change"]+int(reputation_change)
                summ[user_id][post_type] = summ[user_id].get(post_type,0)+1
            else:
                summ[user_id]={"reputation_change":reputation_change,post_type:1}
        elif item.has_key("post_type"):
            user_id = item["owner"]["user_id"]
            post_type = item["post_type"]
            if summ.has_key(user_id):
                summ[user_id][post_type] =   summ[user_id].get(post_type,0)+1
            else:
                summ[user_id]={"reputation_change":0,post_type:1}
    return summ

def addUsers(jRepSum,jUsers):
    #pprint.pprint(jRepSum)
    for user in jUsers["items"]:
        #print user["user_id"],user["display_name"]
        if jRepSum.has_key(user["user_id"]):
            jRepSum[user["user_id"]]["display_name"]=user["display_name"]
        else:
            jRepSum[user["user_id"]]={"display_name":user["display_name"],"reputation_change":0}
    return jRepSum
    
 
def date2epoch(dt,dt_format="%m.%d.%Y %H:%M:%S"):
    return int(time.mktime(time.strptime(dt,dt_format)))


def summary2Csv(jSummary,sep=","):
    result = "user_id,display_name,asker_accepts_answer,asker_unaccept_answer,post_downvoted,post_undownvoted,post_upvoted,post_unupvoted,reputation_change,questions,answers\n"
    result = result.replace(",",sep)
    #print jSummary
    for uid,stats in jSummary.iteritems():
        result += str(uid)+sep+stats["display_name"]+sep
        result += getStrField(stats,"asker_accepts_answer")+sep+getStrField(stats,"asker_unaccept_answer")+sep
        result += getStrField(stats,"post_downvoted")+sep+getStrField(stats,"post_undownvoted")+sep
        result += getStrField(stats,"post_upvoted")+sep+getStrField(stats,"post_unupvoted")+sep
        result += getStrField(stats,"reputation_change")+sep+getStrField(stats,"question")+sep+getStrField(stats,"answer")+"\n"
    return result
        
 
def getStrField(aDic,key):
    return str(aDic.get(key,0))
    

parser = argparse.ArgumentParser()
parser.add_argument("uids",help="Type all the relevant user ids within quotes and separated by semicolon")
parser.add_argument("from_dt",help="Type the from-date in the format DD.MM.YYYY hh:mm:ss within quotes")
parser.add_argument("to_dt",help="Type the to-date in the format DD.MM.YYYY hh:mm:ss within quotes")
parser.add_argument("-s","--site",help="The name of the stackexchange site. Default:stackoverflow")
args = parser.parse_args()

if __name__=='__main__':
    #from_t=date2epoch("07.01.2013 00:00:00")
    #to_t = date2epoch("08.01.2013 00:00:00")
    from_t = date2epoch(args.from_dt)
    to_t = date2epoch(args.to_dt)
    ids = args.uids
    site = "stackoverflow"
    if args.site:
        site = args.site
    print (summary2Csv(summary(ids,from_t,to_t,site)))
    #print "CS347-S2014"
    #pprint.pprint( summary("1634666;1956256;1955944;3192092;2229847;3191522;3191650;2727084;3187763;2403309;3192094;1900408;2403302;3188062;3171412",from_t,to_t))

    # Sample run.
    # python soverflow_query.py "1634666;1956256;1955944;3192092;3558133" "12.01.2015 00:00:00" "12.05.2015 00:00:00"
   
    
   
   

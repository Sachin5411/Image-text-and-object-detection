'''
This script checks whether a post is spam or not.
It goes to cache in local system and extracts all the url and prints the number of times the user has posted the url and contact details which is encountered most of times in past 7 days.
It also dumps all the user link and '''
from pymemcache.client import base
import re,json
from collections import Counter
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-u', '--user_id',type=int,required=True,
    help='user id (int )')
args = vars(ap.parse_args())



def check_spam(user_id):
    client=base.Client(('localhost',11211))
    json_data=client.get(str(user_id))
    #print(json_data)
    str_data="".join( chr(x) for x in bytearray(json_data))
    str_data='['+str_data.replace('\n',',').replace('null','"nothing"')+']'
    str_data=str_data.replace(',]',']')
    j_obj=json.loads(str_data)
    #print(j_obj[0])
    link_list=list()
    phone_list=list()
    for i in range(len(j_obj)):
        link_list.append(re.findall(r'(https?://\S+)', j_obj[i]['description']))
        phone_list.append(re.findall("|".join(["\+\d\d?-? ?\d{3}-\d{3}-\d{4}","\\+\\d\\d?-? ?\\d{10}","\\+\\d\\d?-? ?\\d{5} \\d{5}","\\+\\d\\d?-? ?\\d{3}\\-? ?\\d{7}","\\+\\d\\d?-? ?\\d{4}\\-? ?\\d{6}"]),j_obj[i]['description']))
    link_list = [ y for x in link_list for y in x]
    print(link_list)
    phone_list = [ y for x in phone_list for y in x]
    print(phone_list)
    most_common,num_most_common = Counter(link_list).most_common(1)[0]
    print(str(most_common)+'-->'+str(num_most_common))
    most_common,num_most_common = Counter(phone_list).most_common(1)[0]
    print(str(most_common)+'-->'+str(num_most_common))
    '''if client.get(str(user_id)+'_contacts') == None:
        client.set(str(user_id)+'_contacts',json.dumps({ "url":','.join(link_list),"phone":','.join(phone_list)})+',',expire=604800)
    else:
        client.append(str(user_id)+'_contacts',json.dumps({ "url":','.join(link_list),"phone":','.join(phone_list)})+',',expire=604800)'''
    '''
     uncomment this if u want to dump all the phone and link in cache'''   
    #whatIsTheSum = sum('the' in s for nested in link_list for s in link_list)
    #re.findall(r'(https?://\S+)', s)
check_spam(args['user_id'])
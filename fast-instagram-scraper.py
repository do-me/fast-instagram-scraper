"""
  _____            _     ___              _                                         ____                                       
 |  ___|__ _  ___ | |_  |_ _| _ __   ___ | |_  __ _   __ _  _ __  __ _  _ __ ___   / ___|   ___  _ __  __ _  _ __    ___  _ __ 
 | |_  / _` |/ __|| __|  | | | '_ \ / __|| __|/ _` | / _` || '__|/ _` || '_ ` _ \  \___ \  / __|| '__|/ _` || '_ \  / _ \| '__|
 |  _|| (_| |\__ \| |_   | | | | | |\__ \| |_| (_| || (_| || |  | (_| || | | | | |  ___) || (__ | |  | (_| || |_) ||  __/| |   
 |_|   \__,_||___/ \__| |___||_| |_||___/ \__|\__,_| \__, ||_|   \__,_||_| |_| |_| |____/  \___||_|   \__,_|| .__/  \___||_|   
                                                     |___/                                                  |_|                
https://github.com/do-me/fast-instagram-scraper
Author: do-me
Release: 22.11.2020
v1.2.2
"""

# install torpy, tqdm and pandas before
from torpy.http.requests import TorRequests
import json
import re
import requests
import time
import pandas as pd
import datetime
from tqdm import tqdm # progress bar
import argparse
from func_timeout import func_timeout, FunctionTimedOut

# just in the beginning: define empty variables
# IMPORTANT: when pausing (=interrupting jupyter) and resuming do not execute this cell! 
# just execute the main loop below as last_cursor and post_list will be in memory
post_list = []

# a cursor is an arbitrary hash to paginate through Instagram's posts
# when opening the first page with 50 results it contains a hash to load the next page and so on
# it's pretty much like a page number just that the numbers are not in order 
# for the first page there is no cursor, so leave it empty
last_cursor = "" 
this_cursor = ""

### Instagram hashes
location_hash = "ac38b90f0f3981c42092016a37c59bf7" # might change in the future
hashtag_hash = "ded47faa9a1aaded10161a2ff32abb6b" # borrowed from https://github.com/arc298/instagram-scraper/blob/master/instagram_scraper/constants.py

# help function
# returns right Instagram link
def ilink(cursor=""):
    if location_or_hashtag == "location":
        instalink = 'https://instagram.com/graphql/query/?query_hash='+location_hash+'&variables={"id":"' + str(object_id_or_string) + '","first":50,"after":"'+ cursor +'"}'
        return instalink
    elif location_or_hashtag == "hashtag":
        instalink = 'https://instagram.com/graphql/query/?query_hash='+hashtag_hash+'&variables={"tag_name":"' + str(object_id_or_string) + '","first":50,"after":"'+ cursor +'"}'
        return instalink
    else:
        raise RuntimeError('location_or_hashtag variable must be location or hashtag')        

# define keys to delete here 
def delete_keys(f_node):
    if 'thumbnail_resources' in f_node: del f_node['thumbnail_resources']
    if 'thumbnail_src' in f_node: del f_node['thumbnail_src']
    return f_node

# adds (redundant) location information to every post
def add_location_data(l_node):
    global ploc
    l_node["location_id"] = ploc["id"]
    l_node["location_name"] = ploc["name"]
    l_node["location_slug"] = ploc["slug"]
    l_node["location_latlong"] = [ploc["lat"],ploc["lng"]]
    return l_node

# executes above functions for a list of posts (JSON-nodes)
def add_locations_data_to_cleaned_node(nodelist, just_clean = False):
    if just_clean == True:
        nodelist = [delete_keys(i["node"]) for i in nodelist]
        return nodelist
    else:
        nodelist = [add_location_data(delete_keys(i["node"])) for i in nodelist] # chained functions and list comprehension
        return nodelist

# "berlin,999111555,[1234567,hamburg],[munich,cologne]" -> ['berlin', '999111555', '[1234567,hamburg]', '[munich,cologne]']
# "111,222,333" -> ['111', '222', '333']
def str_list_parser(raw_str_in):
    raw_str_in_lists = re.findall('\[.*?\]',raw_str_in)
    in_items = re.sub("[\(\[].*?[\)\]]", "", raw_str_in)
    in_items = in_items.split(",")
    parsed = [i for i in in_items if i != ""] +raw_str_in_lists
    return parsed

ploc = None

total_posts = 0
# main scraping function
def torsession():
    global last_cursor, this_cursor, post_list, run_number, total_posts, ploc
    
    # Set user agent, i.e. from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    headers = {}
    headers['User-agent'] = user_agent

    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess, tqdm(total=0) as pbar:
            print("Circuit built.") # conncection works
            i = 0
            
            while i < max_requests: # enter main loop
                print("Start iteration {}: {}".format(i,datetime.datetime.now()))
                import pdb
                from pdb import set_trace as bp
                bp()
                              
                try: 
                    ireq = sess.get(ilink(cursor = last_cursor),headers = headers) # fire request
                    idata = ireq.json() # get data from page as json
                    
                except:
                    try:
                        print("Tor end node blocked. Last response: {}".format(ireq))
                    except:
                        print("Tor end node blocked.")
                    return # go back to main loop and get next session
                
                if idata["data"][location_or_hashtag] == None:
                    print("No posts available!")
                    return "no_more_page"
                    
                # access response json
                edge_to_media = idata["data"][location_or_hashtag]["edge_{}_to_media".format(location_or_hashtag)]
                
                # if while scraping new posts appear, they will be considered!
                total_posts = edge_to_media["count"]
                pbar.total = total_posts
                pbar.refresh()
                
                ipage = edge_to_media["edges"] # get posts
                
                # append location information for location scraping
                if location_or_hashtag == "location":
                    ploc = idata["data"][location_or_hashtag]
                    ipage = add_locations_data_to_cleaned_node(ipage)
                else: 
                    ipage = add_locations_data_to_cleaned_node(ipage, just_clean=True)
                    
                post_list.extend(ipage) # extend list with all posts (50 every time)
                pbar.update(len(ipage))

                # saves all posts as csv for every iteration, 50 at once
                pf = pd.json_normalize(post_list)
                
                file_name = "{}{}{}.csv".format(out_dir, object_id_or_string, run_number)
                pf.to_csv(file_name, index=False)
                print("File saved: iteration: {}".format(i))

                this_cursor = edge_to_media["page_info"]["end_cursor"] # this_cursor is next page cursor means unscraped page

                # compare this and last cursor, just in case
                if this_cursor == last_cursor:
                    print("Last two cursors are the same ({}), finishing.".format(this_cursor))
                    return "no_more_page"

                if not edge_to_media["page_info"]["has_next_page"] and this_cursor == None:
                    print("Successfully scraped until last page for {}".format(object_id_or_string))
                    return "no_more_page"

                # for --last_cursor, long pause or jupyter shutdown: saves only the last cursor
                open("{}{}_last_cursor.txt".format(out_dir,object_id_or_string), 'a').write(this_cursor+"\n") 
                # alternatively just print last_cursor for every iteration
                # print(this_cursor)
                
                if len(post_list) > max_posts:
                    print("Maximum number of posts scraped:{}".format(len(post_list)))
                    return "no_more_page"
                
                # return completely if no more page available (has_next_page: False)
                if not edge_to_media["page_info"]["has_next_page"]:
                    if len(post_list) < max_posts:
                        print("Maybe you scraped too fast. Try setting a higher wait_between_requests.")
                        return "no_more_page"
                    else:
                        return "no_more_page"

                last_cursor = this_cursor  
                
                i+=1   
                time.sleep(wait_between_requests) # take a nap

# main loop
def scrape():
    ii = 0 
    while ii < max_tor_renew:
        print("Initiating tor session {}".format(ii))
        
        # timeout try/except with https://github.com/kata198/func_timeout
        try:
            if func_timeout(tor_timeout, torsession) == "no_more_page": 
                print("Mined {} from {} total posts.".format(len(post_list),total_posts))
                break
        except FunctionTimedOut:
            print ("Torsession terminated after {} seconds tor_timeout.".format(tor_timeout))
        except Exception as e:
            print(e)

        ii += 1

# Instantiate the parser
parser = argparse.ArgumentParser(description="""
Fast Instagram Scraper v1.2.2 https://github.com/do-me/fast-instagram-scraper
""")

# Required positional arguments
parser.add_argument('object_id_or_string', type=str, help='Location id or hashtag like 12345678 or truckfonalddump. If --list, enter the item list here comma separated like loveyourlife,justdoit,truckfonalddump')
parser.add_argument('location_or_hashtag', type=str, help='Must be location or hashtag')

# Optional arguments
parser.add_argument('--out_dir', type=str, help='Path to store csv like /.../scrape/', default="")
parser.add_argument('--max_posts', type=int, help='Limit posts to scrape',default=10000000)
parser.add_argument('--max_requests', type=int, help='Limit requests', default=10000000)
parser.add_argument('--wait_between_requests', type=int, help='Waiting time between requests',default=5)
parser.add_argument('--max_tor_renew', type=int, help='Max number of new tor sessions', default=100000)
parser.add_argument('--run_number', type=str, help='Additional file name part like "_v2" for "1234567_v2.csv"', default="")
parser.add_argument('--location_or_hashtag_list', type=str, help='For heterogenous hashtag/location list scraping only: provide another list with "hashtag","location",...', default="")
parser.add_argument('--tor_timeout', type=int, help='Set tor timeout when tor session gets blocked for some reason (default 600 seconds)', default=600)
parser.add_argument('--user_agent', type=str, help='Change user agent if needed', default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
parser.add_argument('--threads', type=int, help='Change the number of threads. Each thread has a different tor end node when scraping for list.', default=1)

# Optional true/false
parser.add_argument('--list', action='store_true', help='Scrape for list')
parser.add_argument('--last_cursor', action='store_true', help='Continue from last cursor')

args = parser.parse_args()

if __name__ == "__main__":

    # main parameters 
    location_or_hashtag = args.location_or_hashtag # location or hashtag, or list
    object_id_or_string = args.object_id_or_string # "1034863903" # a string for hashtag an int for location id i.e. 12345678 or list
    max_posts = args.max_posts # maximum number of posts to scrape
    out_dir = args.out_dir # directory to save csv file

    # advanced parameters
    max_requests = args.max_requests # maximum number of requests from one tor end node
    wait_between_requests = args.wait_between_requests # time in seconds to wait for next requests adding up to normal execution time ~ 4-8 seconds
    max_tor_renew = args.max_tor_renew # maximum number of new tor sessions
    run_number = args.run_number # will be added to filename; useful for pausing and resuming, see comment in cell5
    tor_timeout = args.tor_timeout
    user_agent = args.user_agent
    threads_no = args.threads

    last_cursor = "" # set globally to "", will be overwritten 

    # runs subprocesses
    if threads_no != 1:
        if threads_no < 1:
            raise RuntimeError('Threads number must be > 1') 
        else:
            from multiprocessing.pool import ThreadPool
            import subprocess
            import sys

            def scrape_subprocess(one_obj):
                # time.sleep(x) # Wait 2 seconds
                #print("Process: {}".format(one_obj))
                print(one_obj)
                time.sleep(1)

                cli_line = 'python fast-instagram-scraper.py "{}" {} --max_posts {} --max_requests {} --wait_between_requests {} --max_tor_renew {} --tor_timeout {} --user_agent "{}"'.format(one_obj, location_or_hashtag,max_posts,max_requests,wait_between_requests, max_tor_renew,tor_timeout,user_agent)

                if args.last_cursor:
                    cli_line += " --last_cursor"
                if run_number != "":
                    cli_line += " --run_number {}".format(run_number)
                if out_dir != "":
                    cli_line += " --out_dir {}".format(out_dir)
                if isinstance(one_obj, list): 
                    cli_line += " --list"

                subprocess.run(cli_line)
                #print(cli_line)
                    
            p = ThreadPool(threads_no)

            p.map(scrape_subprocess, str_list_parser(args.object_id_or_string))
            p.close()
            sys.exit()

    # standard scrape for location or hashtag
    if not args.list: 

        # if you want to take off where you left
        if args.last_cursor:
            from pathlib import Path
            last_cursor = Path("{}{}_last_cursor.txt".format(out_dir,object_id_or_string)).read_text().split("\n")[-2] # reads last cursor
            run_number = int(datetime.datetime.now().timestamp()) # change to some index number or just leave the timestamp but watch out for duplicates!
            scrape()
        else: 
            scrape()

    # Scrape multiple hashtags and/or location ids (list)
    else:
        # technically just iterating through scrape_items_list and executes scrape() for every item with new variables
        # it is possible to scrape for both location ids and hashtags at the same time 
        # by passing "hashtag" or "location" in location_or_hashtag_list

        # main parameters 
        scrape_items_list = str_list_parser(object_id_or_string) # ["justdoit","truckfonalddump"]

        # scraping for heterogenous values (locatoin and hashtags) use as below
        # scrape_items_list = ["12345678","justdoit"]
        # location_or_hashtag_list = ["location","hashtag"]
        #----------------------------------------------------------------------------------------------------------------------
        # main loop for scrape_items_list
        for index, element in enumerate(tqdm(scrape_items_list)):
            object_id_or_string = element
            
            ### start: only relevant for heterogenous values 
            if args.location_or_hashtag_list != "":
                location_or_hashtag_list  = args.location_or_hashtag_list.split(",") 
                if len(location_or_hashtag_list) == len(scrape_items_list):
                    location_or_hashtag = location_or_hashtag_list[index]
                if len(location_or_hashtag_list) != len(scrape_items_list) and index == 0:
                    print('location_or_hashtag_list must have same length as scrape_items_list\nScraping {} for every item as defined globally.'.format(location_or_hashtag))  
            ### end: only relevant for heterogenous values 

            print('#{}. Mining for {}:{}'.format(index, location_or_hashtag, object_id_or_string))
            last_cursor = this_cursor = "" # reset cursors
            post_list = []
            scrape()
            
            # use this try except block when scraping over a longer period so that any ocurring error doesn't stop the main loop
            # try:
            #     scrape()
            # except:
            #     print("Finished with error - see log. Continuing with next item.")

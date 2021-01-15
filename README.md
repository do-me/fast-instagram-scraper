# Fast Instagram Scraper
v2.0.0 (beta) - licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1) 

UPDATE 2021/01/10: Currently sometimes not working due to [Torpy bug](https://github.com/torpyorg/torpy/issues/20).
Until it is fixed, please test the following code after installation before using Fast Instagram Scraper to avoid inconveniences:

```
from torpy.http.requests import TorRequests
with TorRequests() as tor_requests:
    with tor_requests.get_session() as sess:
        response = sess.get("https://www.google.com/")
        print(response)
```

If it returns `<Response [200]>` you are ready to go! If not, it is due to the above mentioned bug and you gotta be a little patient. Retry after some hours or half a day - it should work at some point. 

UPDATE 2021/01/15: Torpy bug is fixed. Just install torpy from [latest master branch](https://github.com/torpyorg/torpy). A quick how-to will follow.

## Downloads metadata and images *fast* over the Tor network. No login, no API-key needed.

A fast Instagram Scraper based on Torpy. Downloads post metadata and images for multiple hashtags and [location ids](https://geo.rocks/post/mining-locations-ids/) sequentially, concurrently or combined. Multithreading supported.

*Requirements: [Torpy](https://github.com/torpyorg/torpy) package installed but no login and no API-Key. Working for all OS.*

## Please use responsibly and respect Instagram's terms of use! This tool is exclusively thought for research purposes, not for commercial use! If you enjoy Fast Instagram Scraper consider giving a ⭐.

*Update December 2020*: Hashtags will be mined around 4-5 times faster due to larger batches even though Tor end nodes get blocked more often than for location IDs.

*Update January 2021*: Downloading images now supported - also in combination with multithreading! 

*For newbies*: See the Helper_Functions.ipynb jupyter notebook to get a quick idea of how Fast Instagram Scraper works! 

## Command Line Version
![Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper/blob/main/fast-instagram-scraper-cli.gif)

## Jupyter Version [deprecated]
![Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper/blob/main/Fast%20Instagram%20Scraper.gif)

For this scraper I had the same motivation as for [Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper):
Due to latest Instagram blocking policy changes [Instagram Scraper](https://github.com/arc298/instagram-scraper) is temporarily not performing well (as of November 2020). 
Particularly in comparison to this scraper it's too slow and struggles with getting blocked after a while. 

## Installation 
Just clone the repo or simply download either the jupyter notebook or the command line version.
Best create a virtual environment with conda first and install the necessary packages with:
```python
conda create --name scrape python=3.9 
conda activate scrape
pip install torpy func-timeout pandas tqdm requests
```
For the jupyter notebook version you need to install ipython as well:
```python
pip install ipython
```
After clone the repo and you are good to go:
```
git clone https://github.com/do-me/fast-instagram-scraper.git
```
For jupyter start the notebook in your cloned repo:
```
jupyter notebook
```
For command line, you can call an [example command](https://github.com/do-me/fast-instagram-scraper#command-line-version-1).


## Why not [Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper)?
[Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper) can mine all of a post's information - technically everything being displayed on the page or in the DOM including location and accessibility caption. As it's literally looking at each post and needs to bahave like a human in order not to get blocked it needs to be relatively slow (a couple of seconds per post, depending on your parameters). [Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper) aims at mining at scale but can only do so by accessing Instagram's JSON objects which come in batches of 50 (for hashtags) or ca. 150 (for locations) posts and unfortunately do not include some information such as location and accessibility caption.

### Scraper Comparison
|Scraper|Pro|Con|
|---|---|---|
|[Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper)|+ all post information|- relatively slow<br>- login required<br> - max. 8-12k posts|
|[Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper)|+ fast<br> + no login required<br> + theoretically no maximum|- not all post information|

## Torpy
[Torpy](https://github.com/torpyorg/torpy) makes use of the tor network to request pages.
Install torpy with: `pip3 install torpy` or `pip install torpy`. If you like Torpy consider giving a ⭐ or donating to https://donate.torproject.org/

The Torpy-logic applied here unfortunately doesn't work to scrape all post information as one needs to be logged in. The amount of requests will be associated with the account which gets blocked no matter where from. Hence Torpy cannot be used for [Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper).

## Idea
Use one tor end node to get as many requests as possible. Experience tells: a normal end node can do 15-40 requests (each one 50 posts) waiting around 10 seconds each time. Let's do some [quick math](https://youtu.be/M3ujv8xdK2w): if you got a good node, you'll get 40x50 posts in 400 seconds which gives you a rate of 5 posts per second or even faster if you just want to scrape <500 posts.

## Jupyter Version
You will find detailed information in the notebook.
All future improvements will be available only for the command line version.

## Command Line Version 

Positional Arguments:
```
  object_id_or_string         Location id or hashtag like 12345678 or truckfonalddump. 
                              If --list, enter the item list here comma separated like    
                              loveyourlife,justdoit,truckfonalddump
  location_or_hashtag         "location" or "hashtag"
```

Optional Arguments:
```
  -h, --help                  Show this help message and exit
  --out_dir                   Path to store csv like scrape/ (default is working directory)
  --max_posts                 Limit posts to scrape 
  --max_requests              Limit requests
  --wait_between_requests     Waiting time between requests in seconds
  --max_tor_renew             Max number of new tor sessions
  --run_number                Additional file name part like "_v2" for "1234567_v2.csv"
  --location_or_hashtag_list  For heterogenous hashtag/location list scraping only: provide another list with hashtag,location,...
  --list                      Scrape for list
  --last_cursor               Continue from where you quit before (last_cursor)
  --tor_timeout               Set tor timeout when tor session gets blocked for some reason (default 600 seconds)
  --user_agent                Change user agent if needed
  --threads                   Number of concurrent threads
  --save_as                   csv | json
```  
Example commands:
```
1. python fast-instagram-scraper.py byebyedonald hashtag 
2. python fast-instagram-scraper.py 123456789987 location --max_posts 10000 --max_tor_renew 100
3. python fast-instagram-scraper.py 123456789987 location --last_cursor --out_dir "/.../directory/folder/"
4. python fast-instagram-scraper.py byebyedonald,hellohereIam,georocks hashtag --list
5. python fast-instagram-scraper.py byebyedonald,123456789987,georocks hashtag --list --location_or_hashtag_list hashtag,location,hashtag --max_posts 100 
```
For the last command hashtag argument is a fallback in case the list passed after is not valid. If --location_or_hashtag_list is valid hashtag will be overwritten by the respective value.

Note that saving as json will be memory expensive as Instagram provides lots of different (unnecessary) image thumbnail URLs. Saving as csv is around 1 kb/post; json 10 kb/post.

## Multithreading 🐙
Fast Instagram Scraper supports multithreading. Each thread has a different tor end node. Don't use the --list flag when multithreading. 
A basic example for 3 threads would look like this:
```
python fast-instagram-scraper.py byebyedonald,hellohereIam,georocks hashtag --threads 3
```
All hashtags will be mined concurrently. The shell output will get quite messy as the threads' outputs will be printed in just one shell.🦥

If you would like to have 3 concurrent threads with each 4 sequential commands pass lists. Each list runs on one thread with the parameters provided:
```
python fast-instagram-scraper.py byebyedonald,hellohereIam,[hereiam,goodlife,geography] hashtag --threads 3
```
You can use all arguments as definded above like `--last_cursor`.

Note that on Ubuntu at the moment you should add `shell=True` argument to `subprocess.run(cli_line, shell=True)` in `scrape_subprocess()` function in source code. It's a [minor issue on Ubuntu](https://stackoverflow.com/questions/3172470/actual-meaning-of-shell-true-in-subprocess#:~:text=After%20reading%20the%20docs%2C%20I,the%20process%20is%20directly%20started.) but working working fine on Windows.

## Parallelizing 👷‍♀️ 👷‍♂️
The above method is the preferred way to mine simultanously for several hashtags/locations. If however you would like to monitor every process in a shell, do as follows.
You can run several parallel tor sessions and hence run multiple instances of Fast Instagram Scraper. Let's say you have a list of location IDs and want to get few posts of every location. When running the script sequentially, it will mine one location after another. 
You can easily parallelize it by spawning multiple shells. For Powershell you could generate your commands in Python: 
``` python
location_list = [1234567,1234564567,1234578765432]
for i in location_list:
    print("start powershell {python fast-instagram-scraper.py " + str(i) + " location --max_posts 500};")
    
# Result
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500};
```
Copy paste these commands in a new Powershell window and execute. The locations will be mined and the Powershell windows closed when finished. 
Note: Could be also done with jobs running in the background.

Of course you shouldn't spawn an infinite amount of new processes. For a longer list of locations (i.e. 1000) the recommended method is to chunk your list so you can parallel processes sequential commands. The following example is a list of 60 location IDs chunked into 15 processes of each 4 locations to scrape. 

``` python
location_list = [1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432,1234567,1234564567,1234578765432]

# chunking function - also works with uneven numbers
def chunks(lst, n): # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
location_chunks = list(chunks(location_list,4))
location_chunks

# Result is a list of 15 lists with each 4 locations
[[1234567, 1234564567, 1234578765432, 1234567],
 [1234564567, 1234578765432, 1234567, 1234564567],
 [1234578765432, 1234567, 1234564567, 1234578765432],
 [1234567, 1234564567, 1234578765432, 1234567],
 [1234564567, 1234578765432, 1234567, 1234564567],
 [1234578765432, 1234567, 1234564567, 1234578765432],
 [1234567, 1234564567, 1234578765432, 1234567],
 [1234564567, 1234578765432, 1234567, 1234564567],
 [1234578765432, 1234567, 1234564567, 1234578765432],
 [1234567, 1234564567, 1234578765432, 1234567],
 [1234564567, 1234578765432, 1234567, 1234564567],
 [1234578765432, 1234567, 1234564567, 1234578765432],
 [1234567, 1234564567, 1234578765432, 1234567],
 [1234564567, 1234578765432, 1234567, 1234564567],
 [1234578765432, 1234567, 1234564567, 1234578765432]]

```
Each list of 4 locations will now be put into a Fast Instagram Scraper sequential command which will be executed in a new Powershell window. 

```python
for i in location_chunks:
    outcmd = ""
    outcmd = "start powershell {"
    pyth= ""
    for loc in i:
        pyth = pyth +"python fast-instagram-scraper.py " + str(loc) + " location --max_posts 500;"
    outcmd = outcmd + pyth + "};"
    print(outcmd)
    
# Result
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;};
start powershell {python fast-instagram-scraper.py 1234578765432 location --max_posts 500;python fast-instagram-scraper.py 1234567 location --max_posts 500;python fast-instagram-scraper.py 1234564567 location --max_posts 500;python fast-instagram-scraper.py 1234578765432 location --max_posts 500;};
```
Same as above: Copy paste these commands in a new Powershell window and execute. The locations will be mined and the Powershell windows closed when finished. 

You can raise the chunk size according to your system but be polite and don't exaggerate as it might affect the tor network. 

However, if for example you would like to visualize the approximately 1000 location IDs Instagram is displaying for each city of a country under https://www.instagram.com/explore/locations you could do this quite fast by first [mining the location IDs as described in my blog post](https://geo.rocks/post/mining-locations-ids/) in two simple steps with javascript and after chunking the locations i.e. to 20 chunks of 50 locations. Limit the max_posts parameter to a low number (technically anything between 1 and 50 will have the same effect) i.e. 20 and go for it! Depending on your luck with good tor connections you'll be done in around 10-20 minutes! 

## Recommendation for mining all posts from one location ID or hashtag 
When mining for locations or hashtags with a vast amount of posts it might be better to scrape with multiple commands by using --last_cursor instead of mining everything in one go. At the moment the saving logic append all JSON data to a list, converts it to csv and saves the entire file which becomes quite inefficient for big files. 
However mining in smaller chunks has more advantages so just go i.e. for maximum 20000 - 50000 posts resulting in 16 - 38 mb files each. In my case one iteration (including the cost efficient saving process) was still executed in a reasonable amount of time (<15 seconds). For the very first iteration mine normally. After don't forget the --last_cursor flag. A timeout of 600 seconds per iteration (default) proved to work well. Chaining commands with a semicolon for Powershell and bash helps to keep the process going i.e.:
```bash
python fast-instagram-scraper.py 123456789987 location --max_posts 20000;
python fast-instagram-scraper.py 123456789987 location --max_posts 20000 --last_cursor;
python fast-instagram-scraper.py 123456789987 location --max_posts 20000 --last_cursor;
# and so on ...
```

## CSV concatination 
Use a simple Powershell command to concat all your freshly mined csv files. Manually create a folder "merged" first and execute this command:
```powershell
Get-ChildItem -Filter *.csv | Select-Object -ExpandProperty FullName | Import-Csv  -Encoding UTF8| Export-Csv .\merged\merged.csv -NoTypeInformation -Append -Encoding UTF8
```

## Data preprocessing 
See the [jupyter notebook in this repo](https://github.com/do-me/fast-instagram-scraper/blob/main/A%20complete%20guide%20to%20preprocess%20Instagram%20post%20data%20mined%20with%20Fast%20Instagram%20Scraper.ipynb) to preprocess all the post data with pandas and create a geodataframe with geopandas for visualizing in ordinary GIS programs such as QGIS. 
Hashtag extraction, reprojetion in web mercator (EPSG:3857) and unique points filter included.

## To Do
- Create interface for [LBSNTransform](https://pypi.org/project/lbsntransform/)

## More
- [Blog article](https://geo.rocks/post/fast-instagram-scraper/) about Fast Instagram Scraper
- Find me and stay tuned on [my blog](https://geo.rocks)!

## Star 
Star this repo if you enjoy! ⭐

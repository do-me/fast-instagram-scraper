# Fast Instagram Scraper
v1.2.1

## Jupyter and fully functional command line version available! 

A fast Instagram Scraper based on Torpy. Scrapes posts for multiple hashtags and [location ids](https://geo.rocks/post/mining-locations-ids/) at once.

*Requirements: [Torpy](https://github.com/torpyorg/torpy) package installed but no login and no API-Key. Working for all OS.*

## Command Line Version
![Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper/blob/main/fast-instagram-scraper-cli.gif)

## Jupyter Version
![Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper/blob/main/Fast%20Instagram%20Scraper.gif)

For this scraper I had the same motivation as for [Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper):
Due to latest Instagram blocking policy changes [Instagram Scraper](https://github.com/arc298/instagram-scraper) is temporarily not performing well (as of November 2020). 
Particularly in comparison to this scraper it's too slow and struggles with getting blocked after a while. 

## Why not [Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper)?
[Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper) can mine all of a post's information - technically everything being displayed on the page or in the DOM including location and accessibility caption. As it's literally looking at each post and needs to bahave like a human in order not to get blocked it needs to be relatively slow (a couple of seconds per post, depending on your parameters). [Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper) aims at mining at scale but can only do so by accessing Instagram's JSON objects which come in batches of 50 posts and unfortunately do not include some information such as location and accessibility caption.

### Scraper Comparison
|Scraper|Pro|Con|
|---|---|---|
|[Simple Instagram Scraper](https://github.com/do-me/Simple-Instagram-Scraper)|+ all post information|- relatively slow<br>- login required<br> - max. 8-12k posts|
|[Fast Instagram Scraper](https://github.com/do-me/fast-instagram-scraper)|+ fast<br> + no login required<br> + theoretically no maximum|- not all post information|

## Torpy
[Torpy](https://github.com/torpyorg/torpy) makes use of the tor network to request pages.
Install torpy with: `pip3 install torpy` or `pip install torpy`. If you like Torpy and enjoy Fast Instagram Scraper consider giving a ⭐ or donating to https://donate.torproject.org/

## Idea
Use one tor end node to get as many requests as possible. Experience tells: a normal end node can do 15-40 requests (each one 50 posts) waiting around 10 seconds each time. Let's do the math: if you got a good node, you'll get 40x50 posts in 400 seconds which gives you a rate of 5 posts per second or even faster if you just want to <500 posts.

## Jupyter Version
You will find detailed information in the notebook.

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
  --out_dir                   Path to store csv like /.../scrape/ default is working directory
  --max_posts                 Limit posts to scrape 
  --max_requests              Limit requests
  --wait_between_requests     Waiting time between requests in seconds
  --max_tor_renew             Max number of new tor sessions
  --run_number                Additional file name part like "_v2" for "1234567_v2.csv"
  --location_or_hashtag_list  For heterogenous hashtag/location list scraping only: provide another list with hashtag,location,...
  --list                      Scrape for list
  --last_cursor               Continue from where you quit before (last_cursor)
  --tor_timeout               Set tor timeout when tor session gets blocked for some reason (default 600 seconds)
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

## To Do
- Fix progress bar (might be tqdm.notebook bug related) and set up logfile
- Set timeout function for torpy connection (occasionally gets stuck) 
- Work with torpy session pool 
- Optionally change saving logic

## More
- [Blog article](https://geo.rocks/post/fast-instagram-scraper/) about Fast Instagram Scraper
- Find me on [my blog](https://geo.rocks)!

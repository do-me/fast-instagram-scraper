# Fast Instagram Scraper
A fast Instagram Scraper based on Torpy. Scrapes posts for multiple hashtags and [location ids](https://geo.rocks/post/mining-locations-ids/).

*Requirements: [Torpy](https://github.com/torpyorg/torpy) package installed but no login and no API-Key. Working for all OS.*

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
Install torpy with: `pip3 install torpy` or `pip install torpy`.

## Idea
Use one tor end node to get as many requests as possible. Experience tells: a normal end node can do 15-40 requests (each one 50 posts) waiting around 10 seconds each time. Let's do the math: if you got a good node, you'll get 40x50 posts in 400 seconds which gives you a rate of 5 posts per second or even faster if you just want to <500 posts.

## To Do
- Fix progress bar and set up logfile (might be tqdm.notebook bug related)

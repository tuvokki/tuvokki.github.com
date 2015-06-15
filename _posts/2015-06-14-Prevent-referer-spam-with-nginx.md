---
layout: post
title: "Prevent referer spam with nginx"
---
A while ago I migrated all my web-endeavors to a new server. It takes up a lot of time and while most of the configuration files are copied between servers a few things have changed.

One of those is the fact that I seem to have gained something called [Referer spam](https://en.wikipedia.org/wiki/Referer_spam).

##The referer
[The HTTP referer](https://en.wikipedia.org/wiki/HTTP_referer) (originally a misspelling of referrer) is an HTTP header field that identifies the address of the webpage (i.e. the URI or IRI) that linked to the resource being requested. This type of spam hes been messing up the statistics of my sites in Google Analytics lately On some, less frequented, sites adding up to almost 15% of the total of requests. I found a nice blog about [Cleanup Google Analytics with .htaccess](http://www.elgervanboxtel.nl/site/blog/cleanup-google-analytics-with-htaccess) and did a little investigation to adjust this to work with my nginx config.

![Strange looking stats](/images/posts/referer-spam.png)

First of all, you need to include a list of blocked sites in your config, then you need to add a block in the server-config you want to protect.

##The blocklist
The main check you want to create is for the `$http_referer` to a list of bad sites. In nginx you can create a map and check against that map. Since `map` uses a hash tables this approach will perform better than a series of individual checks.

I had to fix the bucketsize of the hashmap in my nginx.conf to a size higher than the default 32

```bash
  map_hash_bucket_size 64;
```

Then I need a list of urls I consider **bad**. All sites that dump referer spam are. The urls in the below example are copied from the above mentioned blog

```bash
map $http_referer $bad_referer {
    default                         0;
    "~*event-tracking.com"          1;
    "~*theguardlan.com"             1;
    "~*free-share-buttons.com"      1;
    "~*buy-cheap-online.info"       1;
    "~*googlsucks.com"              1;
    "~*fiverr.com"                  1;
}
```

This will assign 1 to all referers that match the mapped list and defaults to 0. Put all the bad referers you want to block here and save it in a file: `/etc/nginx/conf.d/block-http_referer.conf`. The way I have setup my `nginx.conf` all files in the `/etc/nginx/conf.d` directory are automatically inserted into the main conf like this


```bash
  include /etc/nginx/conf.d/*.conf;
```

otherwise you'll have to do this explicitly somewhere in your nginx.conf:

```bash
  include /etc/nginx/conf.d/block-http_referer.conf
```


##The check
The actual check goes into you server-block. I have not found a way to do this in one simple so for all sites. You'll have to add this check to each of the server definitions and each of the sites you host. The check itself is rater straight forward

```bash
[webserver:pts/7]/etc/nginx% cat sites-available/www.yourhost.nl.vhost
server {
  listen *:80;

  server_name www.yourhost.nl;

  root   /sites/www.yourhost.nl;

  index index.html index.htm index.php;

  include error_pages.inc;

  error_log /nginx/logs/yourhost/error.log;
  access_log /nginx/logs/yourhost/access.log combined;

  # block referers that are in my block-http_referer.conf
  if ($bad_referer) {
      return 444;
  }

  #...the rest of the server configuration
}
```

In this case I just return an empty response. Bye-bye bad-referers.

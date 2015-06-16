---
published: false
---

---
layout: post
title: "Don't hardcode db names"
---
Following the series of blogposts about making a blog [part one]({% post_url 2015-05-28-Lets-make-blogs %}), [part two]({% post_url 2015-06-01-Lets-make-more-blogs %}), [the intermezzo]({ post_url 2015-06-12-Short-intermezzo-for-lazy-bloggers }) and finally [part three]({% post_url 2015-06-13-Lets-make-blogs-with-content %}) I have some todo's left in the code. 

One of those resurfaced as an [issue](https://github.com/tuvokki/bogart-blog/issues/3) in the [github repo for the bogart blog](https://github.com/tuvokki/bogart-blog). So, let's get on fixing it. This one should be really easy. I suppose we could just follow the directions we have in the issue:

```
	Use dotenv for it
```

Heading over to [dotenv](https://github.com/motdotla/dotenv) I see we're not in for much of a challenge. I created a local branch for this so I can do my development and testing. Now let's do the work.

##Installing
```
npm install dotenv --save
```

done.

##Usage

Add the require call to dotenv as early as poosible, so high up in `app.js` at least above the `require('nano')`-statement where we want to use it.

```javascript
var bogart = require('bogart')
    ,path  = require('path');

require('dotenv').load();

var viewEngine = bogart.viewEngine('mustache', path.join(bogart.maindir(), 'views'));
var root = require("path").join(__dirname, "public");
var router = bogart.router();
var nano = require('nano')(/*THIS IS WHAT WE NEED TO GET FROM THE ENV*/);
//...the rest of app.js
```

The key's we need to read go into a file called `.env` in the root directory of your project. Add environment-specific variables on new lines in the form of `NAME=VALUE` in our case we need the following

```
DB_HOST=https://couchdb-f0fd27.smileupps.com
```

Be sure to add the `.env` file to your `.gitignore` so you don't accidentally check it in!

Edit the `app.js` once more to use the information in the `.env`-file

```javascript
var nano = require('nano')(process.env.DB_HOST);
```

Done.

Now we're done I can merge my feature branch and we're ready to commit.
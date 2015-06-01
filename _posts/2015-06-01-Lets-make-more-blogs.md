---
layout: post
title: "Let's make more blogs!"
---
This is part 2 of a series of blogs about blogs. In [part one]({% post_url 2015-05-28-lets-make-blogs %}) we created a simple webserver with [bogart](https://github.com/nrstott/bogart) and did some bogus routing to get it all set up. Now it's time to add some functionality!

##Eye-candy
I started early today so I have already did some work before you finally arrived. Since it is not really on-topic, I added a very basic styling to the layout of the page. This was not free, and it touches the webserver, so I'll quickly go through it.

Firstly I added a directory for static stuff. As you might remember, the views are rendered, but not all what we make needs to be processed. For static files bogart supplies us with static directory middleware. Two simple steps are needed, see [the example](https://github.com/nrstott/bogart/blob/master/examples/static-server/app.js). First create a reference to the designated directory

```javascript
var root = require("path").join(__dirname, "public");
```

then use this in the `bogart.middleware.directory` middleware

```javascript
app.use(bogart.middleware.directory(root));
```
and, of course, create the directory itself.

The directory should look something like this now:
![Dirlisting of our project](/images/posts/Lets-make-more-blogs-dirlist.png)
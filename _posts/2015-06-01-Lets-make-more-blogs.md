---
layout: post
title: "Let's make more blogs!"
published: false
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

In this `public`-folder we canput all stuff that needs to be in or site, but needs not be processed. Like css. So we'll create a css subfolder in it and a nice stylesheet called `site.css` (just grab it from here /*TODO: insert link to site.css*/), and add it in the head of our `layout.html` like this

```html
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" type="text/css" href="css/site.css">
```

##Where's the data?
At this point we still have nothing even remotely resembling a blog. So lets update the `index.html` view to something that looks more like a post. Typically a post has a title and a blob, and maybe a date, author and a category and a tag, and comments eh .... start simple with a title and a body.

```html
<article role="main">
  <h1>{{ "{{ title "}}}}</h1>
  <p>
  {{ "{{ body "}}}}
  </p>
</article>
```

In `app.js` we'll have to match the mustaches required here

```javascript
var article = { locals: { title: "first blog", body: "blog body" } };
```

But that' not data! We must hook up the couchdb. There are two routes that we will need in order to create a post.

- `GET /posts/new` -> returns a form to create a new post
- `POST /posts` -> creates a new post from the form parameters provided

The mustache template to create a new post is as follows

```html
<form method='post' action='/posts'>
  <fieldset>
    <legend>New Post</legend>

    <div>
      <label for='title'>Title</label>
      <input name='title' />
    </div>

    <div>
      <label for='body'>Body</label>
      <textarea name='body' rows='15' columns='25'></textarea>
    </div>

    <div class='buttons'>
      <input type='submit' value='Save Post' />
    </div>
  </fieldset>
</form>
```

And for this form we'll make a route

```javascript
router.get('/posts/new', function(req) {
  return viewEngine.respond('new-post.html', {
    locals: {
      title: 'New Post'
    }
  })
});
```

this will render the form and post to the `/posts` route. All we need is something to listen to this. It's time to set up the couchdb. Add a requirement to the couch in `app.js`. To do so head over to [nano](https://github.com/dscape/nano) and/or install via npm

```bash
npm install --save nano
```

require it

```javascript
var nano = require('nano')('https://couchdb-f0fd27.smileupps.com');
```

to create a new database:

```javascript
//nano.db.create('alice'); done this already in https://couchdb-f0fd27.smileupps.com/_utils/fauxton/
```

and to use it:

```javascript
var articles = nano.db.use('articles');
```


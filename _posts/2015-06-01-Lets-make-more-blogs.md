---
layout: post
title: "Let's make more blogs!"
published: true
---
This is part 2 of a series of blogs about blogs. In [part one](http://tuvokki.github.io/lets-make-blogs/) we created a simple webserver with [bogart](https://github.com/nrstott/bogart) and did some bogus routing to get it all set up. Now it's time to add some functionality!

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

In this `public`-folder we can put all stuff that needs to be in or site, but needs not be processed. Like css. So we'll create a css subfolder in it and a nice stylesheet called `site.css` (just grab it from here [site.css](https://github.com/tuvokki/bogart-blog/blob/part2/public/css/site.css)), and add it in the head of our `layout.html` like this

```html
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" type="text/css" href="/css/site.css">
```

##Where's the data?
At this point we still have nothing even remotely resembling a blog. So lets update the `index.html` view to something that looks more like a post. Typically a post has a title and a blob, and maybe a date, author and a category and a tag, and comments eh .... start simple with a title and a body.

```html
<article role="main">
  <title>{{ "{{ title "}}}}</title>
  <p>
  {{ "{{{ body "}}}}}
  </p>
</article>
```

In `app.js` we'll have to match the mustaches required here

```javascript
var article = { locals: { title: "header title", body: "A body that consists of a lot of things." } };
```

But that's no data! We must hook up the couchdb. There are two routes that we will need in order to create a post.

- `GET /posts/new` -> returns a form to create a new post
- `POST /posts` -> creates a new post from the form parameters provided

Save the mustache template to `views/new-post.html` and add the code to create a new post as follows

```html
<section class="articlenew">
  <title>{{ "{{ title "}}}}</title>
  <p>
    <form method='post' action='/posts' class='articleform'>
      <fieldset>
        <legend>New Post</legend>

        <div>
          <label for='title'>Title</label>
          <input name='title' />
        </div>

        <div>
          <label for='body'>Body</label>
          <textarea name='body' rows='30' columns='125'></textarea>
        </div>

        <div class='buttons'>
          <button>Save</button>
          <a href="/">Cancel</a>
        </div>
      </fieldset>
    </form>
  </p>
</section>
```

And for this form we'll make a route

```javascript
router.get('/posts/new', function(req) {
  return viewEngine.respond('new-post.html', {
    locals: {
      title: 'add some content'
    }
  })
});
```

this will render the new-post-form which posts to the `/posts` route. All we need is something to listen to this. It's time to set up the couchdb. Head over to a [free CouchDB host of your own choice](https://www.smileupps.com/) and create an instance. Remember the url of the instance and add a requirement to the couch in `app.js`. To do so head over to [nano](https://github.com/dscape/nano) and/or install via npm

```bash
npm install --save nano
```

require it

```javascript
var nano = require('nano')('https://[your-couchdb-instance].smileupps.com');
```

to create a new database you can use the nano to do it programatically:

```javascript
nano.db.create('articles');
```

but I have done this already in https://[your-couchdb-instance].smileupps.com/_utils/fauxton/. Head over there and create a database and paste in the name to use it:

```javascript
var articles = nano.db.use('articles');
```

As you can see the new article form does a `POST`-request to a route called `/posts` which handles the incoming data. Let's assume that it is all correct and verified by a much more modern frontend than we have here.
The full `POST` route looks something like this

```javascript
router.post('/posts', function(req) {
  var post = req.params;
  post.type = 'post';

  var articles = nano.db.use('articles');

  var insert_article = bogart.promisify(articles.insert);

  return insert_article(post).then(function(data) {
    console.log('you have inserted the body: ', data)
    return bogart.redirect('/posts');
  });
});
```

It will insert your post in the articles database and redirect your user to the /posts url. Which does not exist yet.

The posts-router fetches the articles and passes them to the view, quite straight forward

```javascript
router.get('/posts', function(req) {
  var articles = nano.db.use('articles');

  var readlist = bogart.promisify(articles.list);

  return readlist().then(function(data) {
    console.log(data);
    return viewEngine.respond('posts.html', {
      locals: {
        title: 'all posts',
        postlist: data.rows
      }
    });
  });
  console.log('render');
});
```

 Next up the view. Lets see how this works. Create a file called `views/posts.html` and put the following in
 
 ```html
<section class="articlelist">
  <title>{{ "{{ title "}}}}</title>
  <p>
    {{ "{{ #postlist "}}}}
      {{ "{{id "}}}} - {{ "{{value "}}}}</br>
    {{ "{{ /postlist "}}}}
  </p>
</section>
```

this produces the following output

![image](https://cloud.githubusercontent.com/assets/181719/8032176/643363b4-0dd4-11e5-8fde-0490e1197733.png)

As you can see I have added some links to our routes in the layout of the page, but this output of our route is not so nice, and definately no sigar ... but we've proven a point here.
If you look at the data (see the `postlist` variable we passed to our view: `data.rows`) we can actually see that it is correct

```
{ total_rows: 8,
  offset: 0,
  rows:
   [ { id: '1ec1ba2efd99b08a296022a471000adc',
       key: '1ec1ba2efd99b08a296022a471000adc',
       value: [Object] },
     { id: '1ec1ba2efd99b08a296022a471000e8f',
       key: '1ec1ba2efd99b08a296022a471000e8f',
       value: [Object] },
     { id: '1ec1ba2efd99b08a296022a471001e83',
       key: '1ec1ba2efd99b08a296022a471001e83',
       value: [Object] },
     { id: '1ec1ba2efd99b08a296022a471002a1a',
       key: '1ec1ba2efd99b08a296022a471002a1a',
       value: [Object] },
     { id: '20ce1f108a8bdf2f19f04f42b0001211',
       key: '20ce1f108a8bdf2f19f04f42b0001211',
       value: [Object] },
     { id: '20ce1f108a8bdf2f19f04f42b0001a04',
       key: '20ce1f108a8bdf2f19f04f42b0001a04',
       value: [Object] },
     { id: '4621304957fe61369fabd57a10000b2a',
       key: '4621304957fe61369fabd57a10000b2a',
       value: [Object] },
     { id: 'debc644610a205948ed3704105002661',
       key: 'debc644610a205948ed3704105002661',
       value: [Object] } ] }
```

You can check the ref-id's in your database and see what you have posted there. What we really want to know and what we need to access are those [Object]-objects. For that we need query the CouchDB a little more. And that's a nice topic for the next article in this series.

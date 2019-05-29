Title: Lets-make-blogs-with-content
Date: 2015-06-13 0:00
Category: Old

We're finally at a point that we start to care about content here. In parts [one]({% post_url 2015-05-28-Lets-make-blogs %}) we created a simple webserver and in part [two]({% post_url 2015-06-01-Lets-make-more-blogs %}) we hooked up the database. Now we have to read that content.

##Fix the first two posts
Ofcourse we made a mess of things the first two posts. That's the way projects like this evolve. En we don't want to do things perfectly in iteration one. That first exploration of the technology we're new in is meant for that. Just exploring and incorporating new ideas. What we have now, downloadble, chekoutable in [the github repo for bogart-blog - intermezzo](https://github.com/tuvokki/bogart-blog/releases/tag/intermezzo) is in screaming need for some structure, as to say, some common Software Engineering practices. Okay, let's not overdo it ... a little sense. Oh, and content, as I promised.

Do you remember the strange looking list of posts we've produced

![It will look something like this](/images/posts/object-allposts.png)

That's because we just dump the post into a CouchDB document and later retrieve that document from the database and refer to it by it's id. If you log the document we retrieve you can see that all the information is there, but not the way we like it. We'll fix that in a minute, but first we will have to add a so called slug to the post. Instead of referring to the id, we can address an article by it's slug, a title without the 'strange' characters. In the `router.post('/posts'` function get the title and strip the characters we don't want and replace spaces with dashes

```javascript
  var slug = req.params.title.replace(/[^a-zA-Z0-9\s]/g,"");
  slug = slug.toLowerCase();
  slug = slug.trim();
  slug = slug.replace(/\s/g,'-');
```

Now, when we post a new article it will have the document title filled with the slug instead of a generated id. This is best practice in saving documents to a CouchDB.

The result, before a post looks like this

![before sluggification](/images/posts/before-sluggification.png)

We should add a todo somewhere to limit the size of that title. After sluggification the document looks much nicer

![after sluggification](/images/posts/after-sluggification.png)

Now let's get those articles into our blogging system in a decent way, and view them.

###Some background
Getting all documents from the database is easy. We already do that. But getting exactly everything we want is a little harder, because we have to define some views to retrieve our posts.

You provide CouchDB with view functions as strings stored inside the views field of a design document. You don’t run it yourself. Instead, when you query your view, CouchDB takes the source code and runs it for you on every document in the database your view was defined in. You query your view to retrieve the view result.

The view we need for the article list only needs to hold two pieces of information to show a link to the article. We need the id so we can fetch an individual article and we need the title so we can show that instead of the id or slug. This is how you do that:

```javascript
function(doc) {
    if (doc.type == 'post') {
        emit(doc._id, {title: doc.title});
    }
}
```

From all the documents in the database we are only interested in the ones of type `post`. We're emitting the document id and an object that holds the title. Head over to Fauxton again and create a new `design doc` calles `article_list` and create a view in it called `articleView`

![Create a new articleView in a design doc](/images/posts/new-design-doc.png)

This view can be fetched in almost exactly the same way as fetching the `article.list`-nano view. Only now we specify the view we have just created

```javascript
  var articlelist = bogart.promisify(articles.view);

  return articlelist('article_list', 'articleView').then(function(data) {
```

The `posts.html` to render now gets a list of objects we can loop through and all those objects have two elements, a `title` in a `value`-object and an `id` (or slug, which is the same in this case). The mustache for this loop looks like this

```html
  <p>
    {{ "{{ #postlist "}}}}
      <a href="/posts/{{ "{{ id "}}}}">{{ "{{ value.title "}}}}</a><br>
    {{ "{{ #postlist "}}}}
  </p>
```

And there it is (we definately have to fix those titles in our lazy blogpost generator, btw):

![Article view rendered](/images/posts/the-article-view-in-action.png)

The only trick left here is to create the route we end the user to when he clicks on this generated link:

```
/posts/[some slug]
```

This is handled by another route with an parameter in it. This time it is the slug, and we use that slug to fetch the article. Later on we can make a view for the post and return more data, like comments, but for now this is enough.

```javascript
router.get('/posts/:slug', function(req) {
  var articles = nano.db.use('articles');

  var articlelist = bogart.promisify(articles.get);

  return articlelist(req.params.slug).then(function(data) {
    console.log(data);
    return viewEngine.respond('post.html', {
      locals: {
        title: data.title,
        body: data.body
      }
    });
  });

});
```

We render the post in a template called post.html

```html
<article role="main">
  <h1>{{ "{{ title "}}}}</h1>
  <p>
  {{ "{{ body "}}}}
  </p>
</article>
```

And that's it. We have a blog, suited for lazy bloggers, that does it all. Read, write, render and eh ... nothing more. Whatever. This is pretty cool as it is. We'll go into [release 1.0.0](https://github.com/tuvokki/bogart-blog/releases/tag/v1.0.0) and see what change requests come in. Let's pick a cool name for our release from [this list](http://www.thenervousbreakdown.com/sbeaudoin/2010/05/22-worst-band-names/) and tag it. As ever, download or checkout the result of this post in the tagged [github repo of the bogart-blog](https://github.com/tuvokki/bogart-blog/tree/v1.0.0).
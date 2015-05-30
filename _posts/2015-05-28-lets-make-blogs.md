---
title: Let's make blogs!
layout: post
published: true
---
Its fun to make blogs. They have anything a developer can wish for, minus the complexity of a multilayered enterprise application with a lot of legacy code. Developers heaven consists of a data-layer with some cross references between entities, a server-component that CRUDs this data and spits out readable messages to a front-end in a modern, HTML5, coat making your user happy.

And it always helps a lot if that user is ... you! Mainly because development takes place in yet another cool new framework and the end product is not intended for particular usage anywhere. So, what are we waiting for? Go, go, go!

##Bogart
Bogart is a fast, Sinatra-Inspired JavaScript Framework running on JSGI with Node.JS! If that is not enough to convince you to start using it, routing in Bogart is simple and intuitive. A route is an HTTP method paired with an URL matching pattern and a handler function. It also handles redirects, CORS headers and file streaming. In this series of blogs we'll see if this promising framework can live up to its expectations.

##CouchDB
CouchDB is a database that completely embraces the web. Store your data with JSON documents. Access your documents and query your indexes with your web browser, via HTTP. Index, combine, and transform your documents with JavaScript. CouchDB works well with modern web and mobile apps. You can even serve web apps directly out of CouchDB. And you can distribute your data, or your apps, efficiently using CouchDB’s incremental replication. CouchDB supports master-master setups with automatic conflict detection.

I mean, that would make a ...

##Lovely combination
To start this we'll have to do two things. Create a repo to dump this in. So, head over to your [github](https://github.com) account and create a new repo. I called mine [bogart-blog](https://github.com/tuvokki/bogart-blog). Let's check it out:

    % cd development/projects
    
    % git clone git@github.com:tuvokki/bogart-blog.git
        Cloning into 'bogart-blog'...
        warning: You appear to have cloned an empty repository.

    % cd bogart-blog 

Now, we can make a project:

    % npm init
This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `npm help json` for definitive documentation on these fields
and exactly what they do.

Use `npm install <pkg> --save` afterwards to install a package and
save it as a dependency in the package.json file.


    Press ^C at any time to quit.
    name: (bogart-blog) 
    version: (1.0.0) 0.0.1
    description: A blog created with bogart and couchdb
    entry point: (index.js) app.js
    test command: mocha
    git repository: (https://github.com/tuvokki/bogart-blog.git) 
    keywords: bogart, blog, couchdb
    author: Wouter Roosendaal
    license: (ISC) MIT
    About to write to /Users/wouter/development/projects/bogart-blog/package.json:
    
    {
      "name": "bogart-blog",
      "version": "0.0.1",
      "description": "A blog created with bogart and couchdb",
      "main": "app.js",
      "scripts": {
        "test": "mocha"
      },
      "repository": {
        "type": "git",
        "url": "git+https://github.com/tuvokki/bogart-blog.git"
      },
      "keywords": [
        "bogart",
        "blog",
        "couchdb"
      ],
      "author": "Wouter Roosendaal",
      "license": "MIT",
      "bugs": {
        "url": "https://github.com/tuvokki/bogart-blog/issues"
      },
      "homepage": "https://github.com/tuvokki/bogart-blog#readme"
    }
    
    
    Is this ok? (yes) yes
Tuck in a readme `echo "My bogart blog with CouchDB" > README.md` et voila. 
Install the prerequisites we've been talking about:

    npm install --save bogart
    npm install --save couchdb

This is the clean slate we're building on. So we'll do a `git add .` and a `git commit -a -m 'initial commit'` to baseline this stuff.

And on this baseline we'll build a simple system. 

> Any intelligent fool can make things bigger and more complex... It
> takes a touch of genius - and a lot of courage to move in the opposite
> direction.
>  - E. F. Schumacher

##The components

Our blog application will only support CRUD methods:

 - Create a new post `(POST /posts)`
 - Show a list of all the posts `(GET
   /posts)`
 - Show a single post `(GET /posts/:id)`
 - Comment on a post `(POST
   /posts/:id/comments)`
   
   Let's start with a basic layout for our application. By convention, Bogart's view engine uses a file called layout.html as the layout if it exists. A Bogart layout is a template with a {{{body}}} tag to include the view inside of the layout. Make a folder called `views` in the main folder of the projects and create layout.html

{% highlight html %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
  <title>{{ "{{ title "}}}}</title>
</head>
<body>
  {{ "{{{ body "}}}}}
</body>
</html>
{% endhighlight %}

Next up is the basics of our webserver. Bogart has routing, as I already told before, so lets use it for something that works, and forget about this HTML above.

{% highlight javascript %}
var bogart = require('bogart');

var router = bogart.router();
router.get('/', function(req) { 
      return "hello world"; 
});

router.get('/:name', function(req) {
      return 'hello '+req.params.name;
});

var app = bogart.app();
app.use(bogart.batteries({ secret: 'xGljGo7f4g/a1QveU8VRxhZP5Hwi2YWelejBq5h4ynM'})); // A batteries included JSGI stack including streaming request body parsing, session, flash, and much more.
app.use(router); // Our router

app.start(9981);
{% endhighlight %}

This will start a server on port `9981`:

    % nodemon app.js 
    29 May 22:36:38 - [nodemon] v1.2.1
    29 May 22:36:38 - [nodemon] to restart at any time, enter `rs`
    29 May 22:36:38 - [nodemon] watching: *.*
    29 May 22:36:38 - [nodemon] starting `node app.js`
    util.puts: Use console.log instead
    Server running on port 9981
   
   We can open this in our browser [http://localhost:9981/](http://localhost:9981/) to see what happens. And guess what? We, and the whole world with us, is welcomed. Do you feel that? To make it special add a name [http://localhost:9981/tuvokki](http://localhost:9981/tuvokki) in the mix.

Adding the following will make our system ready for the layout we just created.

{% highlight javascript %}
var viewEngine = bogart.viewEngine('mustache', path.join(bogart.maindir(), 'views'));
{% endhighlight %}

Ps. don't forget to add a reference to the path module in your app.js and change the `/` route to use our view

{% highlight javascript %}
router.get('/', function(req, res) {
  return viewEngine.respond('index.html', { locals: { description: 'This is content' } });
});
{% endhighlight %}

And all we have to do is add an index to render it all. Save index.html in the view folder, and make it render the description ('this is content') we pass into it

{% highlight html %}
<p>
{{ "{{ description "}}}}
</p>
{% endhighlight %}

Now check [http://localhost:9981/](http://localhost:9981/) again and voila, there we have a HTML5 powered message coming from our back-end. The only thing left is hook up this CouchDB and we have a blog. But that's work left for part two of this series.
---
title: Let's make blogs!
layout: post
published: true
---
Its fun to make blogs. They have anything a developer can wish for, minus the complexity of a multilayered enterprise application with a lot of legacy code. Developers heaven consists of a data-layer with some cross references between entities, a server-component that CRUDs this data and spits out readable messages to a front-end in a modern, HTML5, coat making your user happy.

And it always helps a lot if that user is ... you! Mainly because development takes place in yet another cool new framework and the end product is not intended for particular usage anywhere. So, what are we waiting for? Go, go, go!

##Bogart
Bogart is a fast, Sinatra-Inspired JavaScript Framework running on JSGI with Node.JS! If that is not enough to convince you to start using it, routing in Bogart is simple and intuitive. A route is an HTTP method paired with an URL matching pattern and a handler function. It also handles redirects, CORS headers and file streaming. Today we'll see if this promising framework can live up to its expectations.

##CouchDB
CouchDB is a database that completely embraces the web. Store your data with JSON documents. Access your documents and query your indexes with your web browser, via HTTP. Index, combine, and transform your documents with JavaScript. CouchDB works well with modern web and mobile apps. You can even serve web apps directly out of CouchDB. And you can distribute your data, or your apps, efficiently using CouchDB’s incremental replication. CouchDB supports master-master setups with automatic conflict detection.

I mean, that would make a ...

##Lovely combination
To start this we'll have to do two things. Create a repo to dump this in. So, head over to your [github](https://github.com) account and create a new repo. I called mine [bogart-blog](https://github.com/tuvokki/bogart-blog). Let's check it out:

    % cd development/projects                                                                                                                                 % git clone git@github.com:tuvokki/bogart-blog.git
        Cloning into 'bogart-blog'...
        warning: You appear to have cloned an empty repository.
        Checking connectivity... done.
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

Our blog application will only support CRUD methods:

 - Create a new post `(POST /posts)`
 - Show a list of all the posts `(GET
   /posts)`
 - Show a single post `(GET /posts/:id)`
 - Comment on a post `(POST
   /posts/:id/comments)`
   
   Let's start with a basic layout for our application. By convention, Bogart's view engine uses a file called layout.html as the layout if it exists. A Bogart layout is a template with a {{{body}}} tag to include the view inside of the layout.

layout.html
{% highlight jade %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
  <title>{{title}}</title>
</head>
<body>
  {{{body}}}
</body>
</html>
{% endhighlight %}


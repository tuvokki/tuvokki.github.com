---
title: Livereload with Jekyll
layout: post
published: true
---
A few days ago I revived this blog with a quite standard installation of jekyll. This comes with a nice, sparse and very white layout. Now it is time to add some eye-candy to it.

##Livereload
Starting some development on the layout of a site is almost undoable without livereload. We use it in all our projects over at [T.V.K.](https://github.com/TuvokVersatileKolinahr) The only thing is that we mainly use nodejs based projects, and this Jekyll thing is in Ruby. Surely there is a simple solution to do this exact same thing.

All I have to do is find out how this works. Lets do a quick google, and throw together the information found. First thing that sounds interesting enough is [Setting Up LiveReload With Jekyll](http://dan.doezema.com/2014/01/setting-up-livereload-with-jekyll/), which is almost exactly what I want. 

It starts with setting up a Gemfile and adding some stuff in it. But since I use the github-pages gem not all suggested gems were needed. I added the the guard-gems to my `Gemfile` which now looks like this:

    source 'https://rubygems.org'
    gem 'github-pages'
    gem 'rouge', '1.6.2'
    #added for livereload
    gem 'guard'
    gem 'guard-jekyll-plus'
    gem 'guard-livereload'

After that I needed to adjust my Guardfile, which was not there. And I didn't quite understand why. The installation section in the [Guard](https://github.com/guard/guard) documentation gave the answer.

The simplest way to install Guard is to use [Bundler](http://gembundler.com/). Add Guard (and any other dependencies) to a `Gemfile` in your project’s root. We just did that.

then install it by running Bundler:

```bash
$ bundle
```

Generate an empty `Guardfile` with:

```bash
$ bundle exec guard init
```

Ah, that last step provides me with a `Guardfile` with some default options. Going back to that previous blog, and fill the options they supply to my situation. Add this to the `Guardfile` and comment out everything else.

    guard 'jekyll-plus', :serve => true do
      watch /.*/
      ignore /^_site/
    end
    
    guard 'livereload' do
      watch /.*/
    end

##Running
All that is needed is the following:

    % guard

And all goodies we need are there, see:

    WARN: Unresolved specs during Gem::Specification.reset:
          listen (~> 2.7)
    WARN: Clearing out unresolved specs.
    Please report a bug if this causes problems.
    Configuration file: _config.yml
    11:00:47 - INFO - Jekyll building... 
    11:00:47 - INFO - Jekyll build completed in 0.24s /Users/wouter/development/projects/tuvokki.github.com → _site
    11:00:47 - INFO - Jekyll watching and serving using jekyll at 0.0.0.0:4000
    11:00:47 - INFO - Jekyll watching
    11:00:47 - INFO - LiveReload is waiting for a browser to connect.
    Configuration file: /Users/wouter/development/projects/tuvokki.github.com/_config.yml
    11:00:47 - INFO - Guard is now watching at '/Users/wouter/development/projects/tuvokki.github.com'
    [1] guard(main)>     Server address: http://0.0.0.0:4000/
      Server running... press ctrl-c to stop.
    11:01:09 - INFO - Browser connected.
    11:01:19 - INFO - Jekyll Files changed:  building...
    | 
    |  ~ style.scss
    | 
    11:01:19 - INFO - Jekyll build completed in 0.16s /Users/wouter/development/projects/tuvokki.github.com → _site
    11:01:19 - INFO - Reloading browser: style.scss
    11:01:24 - INFO - Jekyll Files changed:  building...
    | 
    |  ~ style.scss
    | 
    11:01:25 - INFO - Jekyll build completed in 0.14s /Users/wouter/development/projects/tuvokki.github.com → _site
    11:01:25 - INFO - Reloading browser: style.scss
    11:02:33 - INFO - Jekyll Files added:  building...
    | 
    |  + _posts/2015-05-31-livereload-with-jekyll.md
    | 
    11:02:33 - INFO - Jekyll build completed in 0.15s /Users/wouter/development/projects/tuvokki.github.com → _site
    11:07:11 - INFO - Jekyll Files changed:  building...
    | 
    |  ~ _posts/2015-05-31-livereload-with-jekyll.md
    | 
    11:07:11 - INFO - Jekyll build completed in 0.17s /Users/wouter/development/projects/tuvokki.github.com → _site
    11:07:11 - INFO - Reloading browser: _posts/2015-05-31-livereload-with-jekyll.md
    [1] guard(main)> 
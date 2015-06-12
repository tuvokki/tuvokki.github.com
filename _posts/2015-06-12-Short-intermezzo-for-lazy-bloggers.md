---
layout: post
title: "Intermezzo for lazy bloggers"
---
Recently I sumbled on the Markov Chain.  A Markov chain is collection of random variables {X_t} (where the index t runs through 0, 1, ...) having the property that, given the present, the future is conditionally independent of the past.

[Wikipedia](https://en.wikipedia.org/wiki/Markov_chain) is a little clearer

 ...Markov chain is a stochastic process with markov property ... [Which means] state changes are probabilistic, and future state depend on current state only.
Markov chains have various uses, but now let's see how it can be used to generate gibberish, which might look legit.

The algorithm is

1. Have a text which will serve as the corpus from which we choose the next transitions.
2. Start with two consecutive words from the text. The last two words constitute the present state.
3. Generating next word is the markov transition. To generate the next word, look in the corpus, and find which words are present after the given two words. Choose one of them randomly.
4. Repeat 2, until text of required size is generated.

The above description is borrowed from [Generating pseudo random text with Markov chains using Python](http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/) written by Shabda Raaj. It holds a very nice code sample in python.

###Lazy blogging
That sounds interesting enough when you come to the topic of lazy bloggers. A long text, fed into a markov chain generator produces a new text that reads like legit text, but in fact is gibberish. Brilliant.

A little more googling revealed a number of generators that do exactly that, but then with an API. I will show how easy it is to populate the new-posts form in our bogart blog with this text using the API privided by [Schmipsum](http://www.schmipsum.com/). Here's the code

The schmipsum API can be called with two parameters, the `set` and the `number`, like this:

    http://www.schmipsum.com/ipsum/patents/100

which produces a text of 100 words that looks like it is a US Patent. The following sets are available:

```javascript
  // possible values of schmipsum sets
  var sets = ["shakespeare",
    "jane_austen",
    "lewis_carroll",
    "patents",
    "nixon_tapes",
    "college_essays",
    "mission_statements",
    "beatrix_potter",
    "frankenstein",
    "bible"];
```

We use this set to randomly forward the user that visits the 'old' new-posts route

```javascript
router.get('/posts/new', function(req) {
  //redirect to a random set
  return bogart.redirect('/posts/new/' + sets[Math.floor(Math.random() * sets.length)]);
});
```

Then the new new-posts route handles this.

```javascript
router.get('/posts/new/:name', function(req) {
  var rp = require('request-promise');
  return rp('http://www.schmipsum.com/ipsum/'+req.params.name+'/1000')
    .then(function(response) {
        responseObject = JSON.parse(response);

        return viewEngine.respond('new-post.html', {
        locals: {
          pagetitle: 'add some content based on ' + req.params.name,
          title: responseObject.ipsum.substring(0,responseObject.ipsum.indexOf('\n')),
          body: responseObject.ipsum.substring(responseObject.ipsum.indexOf('\n')),
          allsets: sets
        }
      })
    })
    .catch(console.error);
});
```

And the steps to get there.
First get [request-promise](https://www.npmjs.com/package/request-promise), the world-famous HTTP client 'Request' now Promises/A+ compliant.

    npm install --save request-promise

Then modify the router to get a parameter, the `/:name` part. This parameter is available in `req.params.name`. With the help of the request-promise all we have to do is get the JSON, and make an object from it. Then the object is split from the first `\n` so we have a nice title, and the rest is put into the body.

Pass the body, title and sets to the mustache, and read them when rendering.

I've added the sets in the html of the new-posts so that we can choose after we have been redirected to a random set.

```html
  <input name='title' value="{{ title }}"></input>

  <textarea name='body' rows='30' columns='125'>{{ body }}</textarea>

    <hr>
    <ul class="sets">Or create a new article based on:<br>
      {{#allsets}}
      <li><a href="/posts/new/{{.}}">{{.}}</a></li>
      {{/allsets}}
    </ul>
```

and finally add a little css to put all the options from the set on one line:

```css
.articlenew ul.sets li {
  display: inline;
}
```

And here's the result, nice huh?

![It will look something like this](/images/posts/Intermezzo-result.png)

Some things can be cleaned up, but this is all there is to it. Remember, we're lazy. So if the blogpost is not what we like ... refresh! You can get the code for this blog on [the github repo for bogart-blog](https://github.com/tuvokki/bogart-blog/releases/tag/intermezzo). Next up is [reading the blog entries]({% post_url 2015-06-14-Lets-make-blogs-with-content %}).

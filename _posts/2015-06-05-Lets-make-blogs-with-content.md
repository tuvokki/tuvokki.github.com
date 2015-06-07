---
layout: post
title: "Let's make blogs with content"
published: false
---

You provide CouchDB with view functions as strings stored inside the views field of a design document. You don’t run it yourself. Instead, when you query your view, CouchDB takes the source code and runs it for you on every document in the database your view was defined in. You query your view to retrieve the view result.

```javascript
function(doc) {
  if(doc.date && doc.title) {
    emit(doc.date, doc.title);
  }
}
```

This is a map function, and it is written in JavaScript. If you are not familiar with JavaScript but have used C or any other C-like language such as Java, PHP, or C#, this should look familiar. It is a simple function definition.

Here is the simplest example of a map function:

```javascript
  //Toggle line numbers
   1 function(doc) {
   2   emit(doc._id, doc);
   3 }
```

This function defines a table that contains all the documents in a CouchDB database, with the _id as the key.

Now let’s talk about two simple views. First, it’s pretty likely you’ll want to be able to list all your recipes by name. Here’s the one possible view for that:

```javascript
function(doc) {
  if (doc.type === 'DrinkRecipe') {
    emit(doc.name.toLowerCase(), doc.name);
  }
}
```

We’ll store that in the ‘drinks’ design doc as ‘byName’. We’re emitting the document name in lowercase as the key (the first argument to emit), and the name as the value so we can preserve the case. Let’s grab at that view with curl:

$ curl http://127.0.0.1:5984/drinks/_design/drinks/_view/byName
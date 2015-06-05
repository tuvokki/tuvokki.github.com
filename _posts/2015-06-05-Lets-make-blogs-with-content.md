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

---
layout: post
title: Test that data into Mongo
---

I'm currently using a test in my Python project to get some data into my Mongo DB. I like it this way, since a unit-test to do such a thing comes in handy in two ways.

* get you project started initially
* migrate your project from D to TAP

##The initial start
Sometimes it is hard to start with a new project. Especially when you have one or more new technologies to include or integrate. I like to follow tutorials, and I never do that by the letter. I just go about my way. But deferring from that 'hello world'-copy-paste-away-thing leaves you with some sample data to be added to your cool, new technology to fetch. This is where a unit-test comes in handy. It gives you the insight into the basics of a technology without having to get all the i's dotted.

##That DTAP thing
And when your new hipster product is ready to be deployed? When it is matured enough to even leave the `localhost` and go to a testserver? Then a unit test comes in handy to do exactly the same thing as it done before. Namely to insert data into the next step in the lifecycle of a program. In a repeatable way, using the technology that underlies the actual program you are developing.

##Example
A while ago I started with [an API implementation usng PyMongo, Flask and Flask-Classy](https://github.com/tuvokki/data-api). So I needed to have some data in my project. I wrote the following unit-test:

{% highlight python %}
    import unittest
	from pymongo import MongoClient
	
	class TestMongoInsertFunctions(unittest.TestCase):
	
	  def setUp(self):
	    # Get a reference to the MongoDB
    self.client = MongoClient('mongodb://localhost:27017/')
    self.db = self.client['quotes']
    self.collection = self.db['simple']

	  def testConn(self):
	    quotes = [
	      {
	        'text': "Waar ik inmiddels behoorlijk zenuwachtig van wordt is het lot van Jip en Janneke.",
	        'who': "Erik van Wunnik"
	      },
	      {
	        'text': "Since there is absolutely no logical reason to assume there is an afterlife, I decided to make the life I have now as much fun as possible.",
	        'who': "Erik van Wunnik"
	      },
{% endhighlight %}

and a whole bunch more ([see](https://github.com/tuvokki/data-api/blob/master/mongo_add_quotes_to_db.py)) ...

{% highlight python %}

	      {
	        'text': "The more future to come, the more customers to satisfy",
	        'who': "Erik van Wunnik"
	      }
	    ]
	    for quote in quotes:
	      ## print values
	      # for kk, vv in quote.iteritems():
	      #   print kk, ': ', vv
	      quote_id = self.collection.insert(quote)
	      print 'inserted: ', quote_id
	
	suite = unittest.TestLoader().loadTestsFromTestCase(TestMongoInsertFunctions)
	unittest.TextTestRunner(verbosity=2).run(suite)
{% endhighlight %}

To run this, just execute this test and you'll have all these (and more) quotes in your database. Also you have some insight in how to use Mongo from Python. And you just do this same trick when you want to go to another box, platform or stack you want to migrate to.

##todo's
And while this example is maybe proof of good intentions done wrong, you know where and what to improve. Any suggestions? Just [open an issue](https://github.com/tuvokki/data-api/issues/new) of fork and pull this repo. You're always welcome to join in.
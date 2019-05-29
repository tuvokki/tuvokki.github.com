Title: couchdb-behind-nginx
Date: 2016-05-09 0:00
Category: Old

Ik really like [CouchDB](http://couchdb.apache.org/) and recently I came across the [official CouchDB Docker image](https://github.com/klaemo/docker-couchdb), so I installed it. And running it behind my nginx reverse proxy lead me to an error stating `"reason": "no_db_file"`, while I expected that nice welcome message. The answer was simple.

I installed the docker image with:

    docker pull klaemo/couchdb:latest

then started it binding to the default port, and the check revealed the so wanted welcome message on the command line:

    docker run -d -p 5984:5984 --name couchdb klaemo/couchdb
    curl http://localhost:5984

Then I created the following nginx `location` in my server definition:

        location /mycouch {
                proxy_pass http://localhost:5984;
        }

And that's where it went wrong. This is what happened, my browser showed this when requesting [the couchdb url](https://example.com/mycouch/):

    {
        "error": "not_found",
        "reason": "no_db_file"
    }

Luckily the fix was rather easy to find.

    #Reverse proxy for subdirectory
    location /couchdb {
        rewrite /couchdb/(.*) /$1 break;
        proxy_pass http://localhost:5984;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

Thanks to the excellent documentation on [using Nginx as a reverse proxy for CouchDB](https://cwiki.apache.org/confluence/display/COUCHDB/Nginx+as+a+proxy). Now I see this welcoming json object when I go to the couchdb url...

    {
        "couchdb": "Welcome",
        "uuid": "f9af63504cc811e6bdf40800200c9a66",
        "version": "1.6.1",
        "vendor": {
            "version": "1.6.1",
            "name": "The Apache Software Foundation"
        }
    }

Yay!

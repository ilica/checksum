# Checksum

This is a web api that creates checksums for URLs and checks them.

# Running It

Included are a requirements.txt and virtual env.

```
python checksum.py
```

This will run some simple tests, then start the webserver.

# Using It

```
curl -i "localhost:5000/createchecksum?url=http://www.google.com?q=foo&fb=x&g=y"
curl -i "localhost:5000/checkchecksum?url=http://www.google.com?q=foo&fb=x&g=y&checksum=[checksum from /createchecksum]"
```


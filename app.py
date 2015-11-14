###--------------------------------------------------------------------------- 
### Simple Flask application to demonstrate plugging Flask into MongoDB via 
### docker
###
### EMB 20151113
###--------------------------------------------------------------------------- 
import os
import pymongo
import ssl
import sys

from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Get MONGO_URI from environment
#
# Format is: mongodb://USER:PASSWORD@HOSTNAME:PORT/DATABASE?ssl=false
MONGO_URI = os.getenv('MONGO_URI')

# Set up MongoDB connection
try:
    conn = MongoClient(MONGO_URI, ssl_cert_reqs = ssl.CERT_NONE)
    db = conn.get_default_database()
except Exception, ex:
    print "Failed to connect to MongoDB: ", ex
    sys.stdout.flush()

@app.route('/')
def hello():
    # Increment our hit counter, or set it to 1 if it doesn't exist yet
    _update = db.sample.update({"name": "hit_counter"}, 
                               {"$inc": {"total_requests": 1}}, 
                               upsert = True)

    # Query for our document
    _requests = db.sample.find_one({"name": "hit_counter"})

    if 'total_requests' not in _requests:
        # Something probably went wrong 
        abort(500)
        
    return render_template('hello.html', total_requests = _requests['total_requests'])

# Run with built-in webserver by default
if __name__ == "__main__":
    app.run(debug = False)

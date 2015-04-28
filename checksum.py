import hashlib
from flask import Flask
from flask import request
import os

app = Flask(__name__)

# Note: this will create a new salt every time this program is run, meaning
# that restarting it will create different checksums.
SALT = os.urandom(16).encode('base_64')

# hash and salt the url using sha256
def make_checksum(payload):
	return hashlib.sha256(payload+SALT).hexdigest()

# Becuase flask thinks url params on urls are actually url params
# for *my* url, not for the payload url, we need to reconstruct it  
def reconstruct_url(url_params_dict):
	url = url_params_dict.get('url')
	for key in sorted(url_params_dict):
		if not key == 'url' and not key == 'checksum':
			url += "&%s=%s" % (key, url_params_dict.get(key))
	return url

# Creates a checksum for the contents of the "url" key
@app.route("/createchecksum")
def create_checksum():
	url = reconstruct_url(request.args)
	checksum = make_checksum(url)

	url_char = "?"
	if "?" in url:
		url_char = "&"
	return '%s%schecksum=%s\n' % (url, url_char, checksum)

# Checks the checksum provided in the "checksum" key against
# the actual checksum computed from the url in the "url" key
@app.route("/checkchecksum")
def check_checksum():
	checksum_to_check = request.args.get('checksum')
	url = reconstruct_url(request.args) 
	checksum = make_checksum(url)

	if checksum == checksum_to_check:
		return "verified\n"
	else:
		return "not verified\n", 400

if __name__ == "__main__":
	print "Running test(s):"
	url_params = {"url":"google.com?key=val", "a" : "foo", "b" : "bar", "checksum":"abc"}
	print reconstruct_url(url_params) == "google.com?key=val&a=foo&b=bar"
	url_params = {"url":"google.com?key=val"}
	print reconstruct_url(url_params) == "google.com?key=val"

	app.run()
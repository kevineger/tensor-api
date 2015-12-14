#!flask/bin/python
from flask import Flask, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import os
import classify
from urllib2 import Request, urlopen, URLError, HTTPError

app = Flask(__name__)
api = Api(app)


class ImageAPI(Resource):
    # Define arguments and how to validate them
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True, location='json',
                                   help='No url provided.')
        super(ImageAPI, self).__init__()

    def get(self):
        return 'Get Image Endpoint!'

    def post(self):
        args = self.reqparse.parse_args()
        url = args['url']
        # Read the image and save it
        path = read_image_from_url(url)
        # Run the classifier on the image
        results = classify.run(path)
        # Remove the image after analyzing
        remove_image(path)
        return results


api.add_resource(ImageAPI, '/tensor/api/v1.0/images', endpoint='images')


def remove_image(path):
    try:
        os.remove(path)
    except OSError, e:
        print "OS Error:", e.message, path


# Read the specified url for a jpg image
def read_image_from_url(url):
    # Get the image filename (string after the last /)
    filename = url.split('/')[-1]
    req = Request(url)
    # Open the url
    try:
        f = urlopen(req)
        print "Downloading " + url
        # Open our local file for writing
        local_file = open('/home/kevin/Downloads/' + filename, "wb")
        # Write to our local file
        local_file.write(f.read())
        local_file.close()
        return '/home/kevin/Downloads/' + filename

        # handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


if __name__ == '__main__':
    app.run(debug=True)

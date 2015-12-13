#!flask/bin/python
from flask import Flask, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import os

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
        return os.popen('python ~/Downloads/tensorflow/tensorflow/models/image/imagenet/classify_image.py').read()
        # return url
        # return {'task': marshal(task, task_fields)}, 201


api.add_resource(ImageAPI, '/tensor/api/v1.0/images', endpoint='images')

if __name__ == '__main__':
    app.run(debug=True)

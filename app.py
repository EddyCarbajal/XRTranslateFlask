from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask, request, jsonify, Response
# from urllib.parse import urlparse, parse_qs
from endpoints.wordDetection.OCR import ocr
from endpoints.wordDetection.cloudvision import detect_text
from endpoints.translation.translator import translate
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r'/*': {'origins': '*'}})


class OCR(Resource):
    def post(self):
        # Check if the request contains a file
        if 'file' not in request.files:
            errors = {"error": "No file part"}
            message = json.dumps(errors)
            return Response(message, status=400, mimetype='application/json')

        file = request.files['file']
        text_response = detect_text(file)
        return jsonify(text_response)


class Translator(Resource):
    def get(self):

        translation = translate(request.args["phrase"], "en")

        return translation


api.add_resource(OCR, '/ocr')

api.add_resource(Translator, '/translator')

if __name__ == '__main__':
    app.run()
    # app.run(use_reloader=True, port=5000, threaded=True)

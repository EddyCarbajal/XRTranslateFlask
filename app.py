from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask, request, jsonify
# from urllib.parse import urlparse, parse_qs
# from endpoints.wordDetection.OCR import ocr
from endpoints.translation.translator import translate

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources ={r'/*': {'origins': '*'}})


class Home(Resource):
    def hello_world():
        return "hello world!"

# class OCR(Resource):
#     def post(self):
#         # Check if the request contains a file
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400

#         file = request.files['file']
#         text_response = ocr(file)

#         if text_response.status_code == 200:
#             response_data = text_response.get_json()
#             if "text" in response_data:
#                 text = response_data["text"]
#                 return jsonify({"text": text})
#             else:
#                 return jsonify({"error": "Text not found in response"}), 500
#         else:
#             return jsonify({"error": text_response.data.decode('utf-8')}), text_response.status_code

class Translator(Resource):
    def get(self):
        
        translation = translate(request.args["phrase"], "en")

        return translation

        


api.add_resource(Home, "/")

# api.add_resource(OCR, '/ocr')

api.add_resource(Translator, '/translator')

if __name__ == '__main__':
    app.run()
    # app.run(use_reloader=True, port=5000, threaded=True)

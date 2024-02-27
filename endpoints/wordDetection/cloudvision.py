from google.cloud import vision
import os
from flask import jsonify
import tempfile
import argparse
import google.auth
from PIL import Image, ImageDraw

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "endpoints/wordDetection/xrtranslate-2e55424687ae.json"


def get_block_text(block):
    block_text = ""
    for paragraph in block.paragraphs:
        for word in paragraph.words:
            word_text = ''.join([symbol.text for symbol in word.symbols])
            block_text += word_text
            # If there's a detected break at the end of the word, handle it
            if word.symbols[-1].property and word.symbols[-1].property.detected_break:
                type_of_break = word.symbols[-1].property.detected_break.type_
                if type_of_break == vision.TextAnnotation.DetectedBreak.BreakType.SPACE:
                    block_text += ' '
                elif type_of_break == vision.TextAnnotation.DetectedBreak.BreakType.LINE_BREAK:
                    block_text += '\n'
        block_text += '\n'

    return block_text


def detect_text(path):

    print("PATH", path)
    client = vision.ImageAnnotatorClient()

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        path.save(temp.name)
        content = temp.read()
    print(temp)

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    boundings = response.full_text_annotation
    observed_blocks = []
    # for testing only
    # draw_boxes(path, boundings.pages[0].blocks[0].bounding_box, 'red')

    for block in boundings.pages[0].blocks:
        print(block)
        block_dict = {}
        vertices = [
            {"x": vertices.x, "y": vertices.y} for vertices in block.bounding_box.vertices
        ]
        block_dict["vertices"] = vertices

        text_dict = get_block_text(block)
        block_dict["text"] = text_dict

        observed_blocks.append(block_dict)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message)
        )

    # # Return the list of dictionaries instead of the original texts object
    return observed_blocks


def draw_boxes(image, bounds, color):
    """Draws a border around the image using the hints in the vector list.

    Args:
        image: the input image object.
        bounds: list of coordinates for the boxes.
        color: the color of the box.

    Returns:
        An image with colored bounds added.
    """
    pil_img = Image.open(image)
    draw = ImageDraw.Draw(pil_img)
    print(bounds)
    vertices = bounds.vertices
    polygon = [(vertex.x, vertex.y) for vertex in vertices]

    draw.polygon(polygon, outline=color)

    pil_img.save("testing.jpg")

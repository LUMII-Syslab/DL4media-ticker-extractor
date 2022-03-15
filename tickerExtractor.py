from code.video import Video
from code.tesseract import TesseractOCR
import code.tsv
from code.slidingreader import read_tickers
import json, uuid

default = {
    'resize_font': True,
    'interpolation': 'cubic',
    'height': 10,
    'add_padding': False,
    'padding': 4,
    'method': None,
    'gamma_correct': True,
    'merge_method': 'char_frequency',
    'garbage_method': 'char_confidence',
    'overlap_method': 'hybrid'
}

def extract_text(file):
    data = file[0].read()

    video_path = "/data/" + str(uuid.uuid4()) + ".mp4"

    f = open(video_path, 'wb')
    f.write(data)
    f.close()
    
    video = Video(video_path, TesseractOCR())
    output_stories = read_tickers(video, **default)
    result = json.dumps(output_stories, indent = 2)
    
    return result
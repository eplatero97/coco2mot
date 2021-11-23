import json
import numpy as np
import pandas as pd
from pathlib import Path
import argparse
from pandas import json_normalize
import os

parser = argparse.ArgumentParser(description = "convert coco files to mot format")

parser.add_argument("--cpath", type = str, help = "coco path", required = True)
parser.add_argument("--mpath", type = str, help = "mot path", required = True)

args = parser.parse_args()

def coco2mot(fname: str = r"coco/path.json") -> pd.DataFrame:
    """
    :obj: output a pandas dataframe with each column corresponding to values in `det.txt` file in MOT structure
    :arg fname: absolute path to coco json file name
    """
    
    # input coco json as python dictionary 
    with open(fname) as file:
        coco = json.load(file)
        
    # extract all information under "annotations" sections
    annts = coco["annotations"]
    
    # turn json into pandas dataframe 
    df = json_normalize(annts)[["id", "image_id", "category_id", "bbox"]]
    
    # extract bounding box coordinates
    bboxes = df.bbox.values
    tl_xs = [bbox[0] for bbox in bboxes]
    tl_ys = [bbox[1] for bbox in bboxes]
    widths = [bbox[2] for bbox in bboxes]
    heights = [bbox[3] for bbox in bboxes]

    # init dictionary that will be turned into a pandas dataframe that's in the same format as `det.txt` in MOT structure
    mot_dict = {
        "frame" : df.image_id,
        "id" : -1,
        "tl_x": tl_xs,
        "tl_y" : tl_ys,
        "width" : widths,
        "height" : heights,
        "conf" : 1,
        'x' : -1,
        'y' : -1,
        'z' : -1
    }

    del df

    # return dataframe
    mot_df = pd.DataFrame(mot_dict)
    return mot_df


# assume we already have a "backbone" mot directory
cfiles = list(Path(args.cpath).rglob("*.json"))
cfiles_wo_ext = [os.path.splitext(cfile.name) for cfile in cfiles]

for cfile in cfiles:
	df = coco2mot(cfile)
	cfile_wo_ext = os.path.splitext(cfile.name)[0]
	detpath = os.path.join(args.mpath, cfile_wo_ext, "det", "det.txt")
	df.to_csv(detpath, index = False, header = False)

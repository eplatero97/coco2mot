import json
import numpy as np
import pandas as pd
from pathlib import Path
from pandas import json_normalize
import os

def mot_backbone(fnames: list = ["vid1", "vid2", "vid3"], opath: str = r"/some/path/train") -> None:
    """
    :obj: create empty MOT directory structure
    :arg fnames: for each value in `fnames`, a new mot sequence directory structure will be created
    :arg opath: output path
    ----------------------------------------------------------------
    Creates below directory structure:
    └─ opath/
        ├── vid1
        │   ├── det
        │   ├── gt
        │   ├── img1
        ├── vid2
        │   ├── . . .
        ├── . . .
    """
    opath = Path(opath)
    opath.mkdir(parents = True, exist_ok = True) 

    for fname in fnames:
        fpath = opath / fname
        fpath.mkdir(exist_ok = True) # create vid dir
        (fpath / "det").mkdir() # create det dir
        (fpath / "gt").mkdir() # create gt dir
        (fpath / "img1").mkdir() # create img1 dir


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
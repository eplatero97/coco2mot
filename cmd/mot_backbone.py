import json
import numpy as np
import pandas as pd
from pathlib import Path
import argparse
import os

parser = argparse.ArgumentParser(description = "convert coco-to-mot format")

parser.add_argument("--pname", type = str, default = "coco2mot", help = "name to parent directory", required = False)
parser.add_argument("--opath", type = str, help = "output path", required = True)
parser.add_argument("--cpath", type = str, help = "coco path", required = True)

args = parser.parse_args()



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


opath = Path(args.opath) / args.pname
opath.mkdir(parents = True, exist_ok = True) # recursively mkdir if it does not exist
files = list(Path(args.cpath).rglob(f"*.json"))
files_wo_ext = [os.path.splitext(vfile.name)[0] for vfile in files]

mot_backbone(files_wo_ext, opath)

from pathlib import Path
import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser(description = "convert videos to mot format frames")

parser.add_argument("--mpath", type = str, help = "mot path", required = True)
parser.add_argument("--vpath", type = str, help = "video path", required = True)
parser.add_argument("--meta", type = str, help = "csv file path where 0th column contains video names and 1st column contains corresponding mot sequence directory name", required = True)

args = parser.parse_args()


# extract video to corresponding mot sequence mapping
map = pd.read_csv(args.meta)
vfiles = map.iloc[:, 0].values.reshape(-1).tolist() # name of video file
mdirs = map.iloc[:, 1].values.reshape(-1).tolist() # name of corresponding mot sequence directory

# extract all video directories in `mpath`
live_mdirs: list = os.listdir(args.mpath)
"""
It may be the case that there exists more videos in `meta` then there are in `mpath`.
For example, we may have directories for only three videos in `mpath` out of the
20 videos listed in `meta`.

Thus, `live_mdirs` will allows us to only extract subset of the videos in `mpath`
"""

for vfile, mdir in zip(vfiles, mdirs):
    if mdir not in live_mdirs:
        continue 
    source = os.path.join(args.vpath, vfile)
    dest = os.path.join(args.mpath, mdir, "img1")
    ffmpegexe = f"ffmpeg -i \"{source}\" -start_number 1 -b:v 10000k -vsync 0 -an -y -q:v 16 \"{dest}/%06d.jpg\" &"
    os.popen(ffmpegexe)

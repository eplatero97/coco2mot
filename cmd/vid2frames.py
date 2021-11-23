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

for vfile, mdir in zip(vfiles, mdirs):
    source = os.path.join(args.vpath, vfile)
    dest = os.path.join(args.mpath, mdir, "img1")
    ffmpegexe = f"ffmpeg -i \"{source}\" -start_number 1 -b:v 10000k -vsync 0 -an -y -q:v 16 \"{dest}/%06d.jpg\" &"
    os.popen(ffmpegexe)

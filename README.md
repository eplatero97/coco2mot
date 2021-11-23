# coco2mot

### Purpose?

This module has utilities to transform a COCO scheme into MOT format.

### Dependencies?

* pandas
* numpy 

### Features?

Two types of features:

* module features
* command-line features

#### module features?

`coco2mot(fname)`

```python
from coco2mot import coco2mot

fname = r"coco/path.json" # file name
df = coco2mot(fname)
df.columns # [frame, id, tl_x, tl_y, width, height, conf, x,y,z]
```

given a coco json path, it returns a dataframe in `det.txt` mot format

`mot_backbone(fnames)`

```python
from coco2mot import mot_backbone

fnames = ["vid1", "vid2", "vid3"] # file names
opath = r"/output/path" # output path
mot_backbone(fnames, opath)
```

Output:

```bash
└─ opath/
    ├── vid1
    │   ├── det
    │   ├── gt
    │   ├── img1
    ├── vid2
    │   ├── . . .
    ├── . . .
```

give a list of names, it makes a sequence directory for each name in list. All these directories are empty.

#### command-line features?

`mot_backbone.py`

```bash
python ./cmd/mot_backbone.py --pname parent_dir --opath output/dir --cpath /coco/files/dir
```

Output:

```bash
└─ output/dir/parent_dir
    ├── coco_json_1
    │   ├── det
    │   ├── gt
    │   ├── img1
    ├── coco_json_2
    │   ├── . . .
    ├── . . .
```



`coco2mot.py`

```bash
python ./cmd/coco2mot.py --mpath /mot/dir/ --cpath /coco/files/dir
```

Output:

```bash
└─ output/dir/pname
    ├── coco_json_1
    │   ├── det
    │   │   ├── det.txt
    │   ├── gt
    │   ├── img1
    ├── coco_json_2
    │   ├── det
    │   │   ├── det.txt
    │   ├── gt
    │   ├── img1
    ├── . . .
```

Adds a `det.txt` file in mot format from coco json files specified in `--cpath`.



`vid2frames.py`

```bash
python ./cmd/vid2frames.py --mpath /mot/dir --vpath /videos/dir --meta vid/to/dir/map.csv
```

Output:

```bash
└─ output/dir/pname
    ├── coco_json_1
    │   ├── det
    │   │   ├── det.txt
    │   ├── gt
    │   ├── img1
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    │   │   ├── . . .
    ├── coco_json_2
    │   ├── det
    │   │   ├── det.txt
    │   ├── gt
    │   ├── img1
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    │   │   ├── . . .
    ├── . . .
```

Adds frames `%06d.jpg` that correspond to each specified mapping in `map.csv`. 

This csv contains two columns with any names where the first column represents the video names stored in `--vpath` and the second column represents the corresponding coco json file that it corresponds to. For example, our above example could be seen as:

```python
vid_name,dir_name
vid1,coco_json_1
vid2,coco_json_2
. . .
```



> NOTE: as you can see from above, `mot_backbone.py`, `coco2mot.py`, and `vid2frames.py` all sequentially build around each other. 

### New Features?

A few simple features are offered in this repository. Any new functionalities that you create from the extension of these modules are welcome!

# j-vision

A project (for educational purposes) on computer vision for face detection.

###To detect faces:

Save images to a folder called *images* and run:

```shell
python detect_faces.py -i images/*
```
The faces are saved in the folder *faces*.

####Optional arguments

To select a specific faceclassifier, use:

```shell
python detect_faces.py -f cascades/haarcascade_frontalface_alt.xml -i images/*
```

###To save images from web search:

To save the first 100 images, run:

```shell
python image_search.py -q "brad pitt"
```

The images will be saved in *images/BradPitt*. The image URLs with the corresponding status will be saved in *images/BradPitt/list.txt*. You can run detect_faces on it as follows:

```shell
python detect_faces.py -f cascades/haarcascade_frontalface_alt.xml -i images/BradPitt/*
```

The faces are saved in the folder *faces/BradPitt*.

####Optional arguments

```shell
usage: image_search.py [-h] -q QUERY [-n NUM] [-d DOWNLOADDATA] [-c CONTINUEFROM]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Query string
  -n NUM, --num NUM     Number of images required (optional, int, default = 100)
  -d DOWNLOADDATA, --downloadData DOWNLOADDATA
                        Request image query or use downloaded data (optional, yes/no, default = yes)
  -c CONTINUEFROM, --continueFrom CONTINUEFROM
                        Continue download from index, should be less than
                        total number of images (optional, int, default = 1)
```

To save the first 37 images, run:

```shell
python image_search.py -q "brad pitt" -n 37
```

To use already downloaded data (saved in *data.txt*), run:

```shell
python image_search.py -q "brad pitt" -d "no"
```

To continue downloading images from 56th image, run:

```shell
python image_search.py -q "brad pitt" -c 56
```

# j-vision

A project (for educational purposes) on computer vision for face detection.

###To detect faces:

Save images to a folder called *images* and run:

```shell
python detect_faces.py -f cascades/haarcascade_frontalface_alt.xml -i images/*
```

The faces are saved in the folder *faces*.

###To save images from web search:

To save the first 100 images, run:

```shell
python image_search.py -q "brad pitt"
```

To save the first 37 images, run:

```shell
python image_search.py -q "brad pitt" -n 37
```

The images will be saved in *images/BradPitt*. The image URLs with the corresponding status will be saved in *images/BradPitt/list.txt*. You can run detect_faces on it as follows:

```shell
python detect_faces.py -f cascades/haarcascade_frontalface_alt.xml -i images/BradPitt/*
```

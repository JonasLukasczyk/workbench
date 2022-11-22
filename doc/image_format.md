# PyCinema Image Data Object
The PyCinema image data object has two attributes:
- **meta**: a dictionary where key-value pairs record meta information associated with the image (e.g., *timestep:23*).
  - Each key is a lower-case string recording the name of the meta information.
  - The value can be of any type (including a numpy array).
- **channels**: a dictionary where each key-value pair records a single channel.
  - Each key is a lower-case string representing the name of a channel (e.g., *rgba*, *depth*, or *some_scalar_data*).
  - Each dictionary value is a numpy array holding the information of the channel, where the first two dimensions of the array must correspond to the resolution of the image. The third dimension of the array determines how many values are recorded per pixel. For instance, a *depth* channel corresponds to a (width,height,1) array since the array records one scalar per pixel, while a *rgba* channel corresponds to a (width,height,4) array since it records three values per pixel.
  - Note: A PyCinema image can have any number of channels storing any kind of scalars or vectors per pixel. However, certain channels are treated specially in PyCinema, such as the *rgba* and *depth* channels.

# Storing PyCinema Images as HDF5  Files
- PyCinema supports common image formats such as *png* and *jpeg* files. However, these formats have limited support for meta data and multiple channels per image.
- The *Hierarchical Data Format (HDF)* is an abstract data container format that can represent any kind of information. An hdf5 file is essentially a tree where intermediate nodes are called **groups**, and leaf nodes are called **datasets**. Groups can be thought of as directories, and datasets as named numpy arrays.
- A PyCinema image stored in a hdf5 file uses the following structure:
  - The root group contains the **meta** group which stores each key-value pair of the meta attribute of the PyCinema image as a dataset.
  - The root group contains the **channels** group which stores each key-value pair of the channel attribute of the PyCinema image as a dataset.

# Example
```
HDF5 File
├── version: 1.0
├── meta
│   ├── timestep: 12
│   ├── simulation: "Sim01" (hdf5 also supports string datasets)
│   ├── camera_position: [1.0,1.0,0.5]
│   ├── camera_direction: [0.0,1.0,0.0]
│   └── camera_up: [0.0,0.0,1.0]
└── channels
    ├── rgba: [255,0,0,255, 0,255,0,255, 0,0,255,255, 255,255,255,255] (4 unsinged chars per pixel)
    ├── depth: [0.0, 0.33, 0.66, 1.0] (1 float value per pixel)
    └── uv: [0.0,0.0, 1.0,0.0, 0.0,1.0, 1.0,1.0] (2 float values per pixel)
```

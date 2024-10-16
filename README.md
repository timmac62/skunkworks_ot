# SW_ObjectTracker
> Skunk Works Object Tracker OT

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

This OT application:
* runs on the NVidia Jetson Orin utilizing the camera to detect people
* assigns them a unique ID
* sends that ID with X Y coordinates to AOS app

![](nano.jpg)

## Development setup

The NVidia Jetson Orin development environment is setup to utilize prebuilt docker containers

**NOTE:**  you can alternatively build these projects from source

These containers include l4tpytorch and many other useful libraries and tools

This application takes advantage of these containers as noted below in the Usage example

## File Descriptions

| File | Description |
| ----------- | ----------- |
| udp_server.cpp | Server implementation to be mimiced in the AOS app | 
| object_tracking.py | Jetson Inference application - object tracking and sending ID, X, Y coordinates sent via sockets to udp_server | 



## Usage example

Execute the following commands to get the Object Tracking application running. This requires 2 terminals:

```sh
cd ~/skunkworks
g++ udp_server.cpp -o udp_server
./udp_server
```

```sh
cd ~/Documents/jetson-inference
docker/run.sh -v ~/.bash_aliases:/root/.bash_aliases --volume ~/skunkworks/:/my-object-tracking
python3 /my-object-tracking/object_tracking.py
```


## Release History

* 0.1.2
    * CHANGE: added support to send UDP sockets with ID, x, y coordinates to the udp_server.cpp application which should prove useful for the AOS app
    * g++ udp_server.cpp -o udp_server
    * ./udp_server
    * then execute OT application as noted above (from container)
    * housekeeping: removed unused files I developed for IPC mkfifo - now using UDP to udp_server app (AOS)
* 0.1.1
    * CHANGE: Changed from IPC/mkfifo to a non blocking socket using UDP, 
    * Note that this requires **server.py** to be up and running but this server does not need to be running in container
* 0.1.0
    * CHANGE: Initial implementation

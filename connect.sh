docker -H 192.168.0.107  run -it --rm -e ROS_MASTER_URI=http://192.168.0.107:11311/  \
                                 -e ROS_IP=192.168.0.109 \
                                 -v ~/my-ros-duckiebot/packages:/code/catkin_ws/src/my-ros-duckiebot/packages \
                                 --net=host \
                                 --privileged  \
                                  bgloh/my-ros-duckiebot:daffy-arm32v7   /bin/bash

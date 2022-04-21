#FROM docker.io/duckietown/dt-ros-commons:daffy-arm32v7
FROM docker.io/duckietown/dt-ros-commons:ente-amd64
# use daffy-arm64v8 if you are using a Duckiebot MOOC Founder's Edition

# define/create repository path
ARG REPO_NAME="my-ros-duckiebot"
ARG CATKIN_WS_DIR="/code/catkin_ws"
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"
ARG ROS_DISTRO="noetic"

RUN mkdir -p "${REPO_PATH}"
#RUN mkdir -p "/code/catkin_ws/src/my-ros-duckiebot"
WORKDIR "${REPO_PATH}"

# install apt dependencies
#COPY ./dependencies-apt.txt "${REPO_PATH}/"
#RUN apt install ${REPO_PATH}/dependencies-apt.txt
RUN apt install nano

# update pip
RUN python3 -m pip install --upgrade pip

# install python3 dependencies
COPY ./dependencies-py3.txt "${REPO_PATH}/"
RUN python3 -m pip install -r ${REPO_PATH}/dependencies-py3.txt --verbose

# copy the source code
COPY ./packages "${REPO_PATH}/packages"

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && catkin build --workspace ${CATKIN_WS_DIR}/



#COPY requirements.txt ./

#RUN pip install -r requirements.txt

#COPY color_detector.py ./

#CMD python3 ./color_detector.py

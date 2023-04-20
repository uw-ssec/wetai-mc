# This is a PRP->Braingeneers image which should later be extended to
# PRP->Braingeneers->WetAI

FROM gitlab-registry.nrp-nautilus.io/prp/jupyter-stack/prp

RUN sudo apt-get update && sudo apt-get install -y \
    glances \
    wget \
    curl \
    ncdu \
    ffmpeg \
    rclone \
    awscli \
    hdf5-tools

RUN python -m pip install --force-reinstall --no-cache git+https://github.com/braingeneers/braingeneerspy.git#egg=braingeneerspy[all]

RUN git clone git@github.com:braingeneers/mission_control.git

#!/usr/bin/env bash
source env.sh
cd swapper

$DFD_PYTHON "train_DFL.py" \
    -si "../$DFD_WORKSPACE/data_source/crop_img" \
    -sm "../$DFD_WORKSPACE/data_source/face_mask" \
    -ti "../$DFD_WORKSPACE/data_target/crop_img" \
    -tm "../$DFD_WORKSPACE/data_target/face_mask" \
    -m "../$DFD_WORKSPACE/model" \
    -b "8" \
    -e "50" \
    -lr "1e-4" \
    -r 256 \
    -cl 0 \
    -n 2 \
    -M 5000 \
    --cuda
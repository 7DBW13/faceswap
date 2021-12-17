#!/usr/bin/env bash
source env.sh
cd swapper

$DFD_PYTHON "train_Disney.py" \
    -si "../$DFD_WORKSPACE/data_source/crop_img" \
    -sm "../$DFD_WORKSPACE/data_source/face_mask" \
    -ti "../$DFD_WORKSPACE/data_target/crop_img" \
    -tm "../$DFD_WORKSPACE/data_target/face_mask" \
    -m "../$DFD_WORKSPACE/model" \
    -b "[64, 64, 64, 32, 16, 4, 2, 4, 2]" \
    -e "[30, 30, 30, 100, 100, 100, 100, 150, 175]" \
    -lr "[1e-4, 1e-4, 1e-4, 1e-4, 5e-5, 5e-5, 3e-5, 3e-5, 3e-5]" \
    -r 128 \
    -cl 2 \
    -n 2 \
    -M 5000 \
    --cuda
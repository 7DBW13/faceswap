#!/usr/bin/env bash
source env.sh
cd preprocessor

$DFD_PYTHON "preprocessor.py" \
    -i "../$DFD_WORKSPACE/data_source/origin"\
    -m "../$DFD_WORKSPACE/data_source/face_mask"\
    -f "../$DFD_WORKSPACE/data_source/face_img"\
    -c "../$DFD_WORKSPACE/data_source/crop_img"\
    -t "../$DFD_WORKSPACE/data_source/trans_matrix"\
    -r "128"

$DFD_PYTHON "preprocessor.py" \
    -i "../$DFD_WORKSPACE/data_target/origin"\
    -m "../$DFD_WORKSPACE/data_target/face_mask"\
    -f "../$DFD_WORKSPACE/data_target/face_img"\
    -c "../$DFD_WORKSPACE/data_target/crop_img"\
    -t "../$DFD_WORKSPACE/data_target/trans_matrix"\
    -r "128"

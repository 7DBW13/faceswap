#!/usr/bin/env bash
source env.sh

mv "$DFD_WORKSPACE/source.mp4" "tempsource.mp4" 2> /dev/null
mv "$DFD_WORKSPACE/target.mp4" "temptarget.mp4" 2> /dev/null

rm -r "$DFD_WORKSPACE"
mkdir "$DFD_WORKSPACE"

mv "tempsource.mp4" "$DFD_WORKSPACE/source.mp4" 2> /dev/null
mv "temptarget.mp4" "$DFD_WORKSPACE/target.mp4" 2> /dev/null

mkdir "$DFD_WORKSPACE/data_source"
mkdir "$DFD_WORKSPACE/data_source/origin"
mkdir "$DFD_WORKSPACE/data_source/face_img"
mkdir "$DFD_WORKSPACE/data_source/face_mask"
mkdir "$DFD_WORKSPACE/data_source/crop_img"
mkdir "$DFD_WORKSPACE/data_source/swap_face"
mkdir "$DFD_WORKSPACE/data_source/merge_result"
mkdir "$DFD_WORKSPACE/data_source/trans_matrix"
mkdir "$DFD_WORKSPACE/data_target"
mkdir "$DFD_WORKSPACE/data_target/origin"
mkdir "$DFD_WORKSPACE/data_target/face_img"
mkdir "$DFD_WORKSPACE/data_target/face_mask"
mkdir "$DFD_WORKSPACE/data_target/crop_img"
mkdir "$DFD_WORKSPACE/data_target/swap_face"
mkdir "$DFD_WORKSPACE/data_target/merge_result"
mkdir "$DFD_WORKSPACE/data_target/trans_matrix"
mkdir "$DFD_WORKSPACE/model"
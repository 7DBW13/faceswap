Deep Face Swap
==================================

**University of Pennsylvania, CIS 581, Final Project**

* Lanqing Bao
* Yichun Cao
* Zhangkaiwen Chu
* Bowen Deng
* Chen Fan
* Zhenglin Zhang

## How to Build

We highly recommend for using Anaconda to build a virtual environment and install required packages.
```
conda create -n DFD python=3.6.8
```
Before building or running, make sure the environment is activated.
```
conda activate DFD
```
The packages required can be installed by running the following line in the root directory.
```
pip install -r requirements.txt
```
Besides, PyTorch is needed for this project and the way to download it with correct CUDA version can be found on https://pytorch.org/. For example, this command works for a Windows computer with CUDA 11.3.
```
pip3 install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```
After installing all packages, the last thing is to build for the 3DDFA model.
```
cd preprocessor
bash build.sh
```
**Note:** This script seems not compatible with a Windows system. Try to use Linux or Mac instead.

## Usage

All runtime scripts can be located at `./scripts`.
```
.
└── scripts
    ├── 0_clear_workspace.sh
    ├── 1_video_to_img.sh
    ├── 2_face_extraction.sh
    ├── 3_train_swapper.sh
    ├── 3_1_train_swapper_dfl.sh
    ├── 4_gen_swap_face.sh
    ├── 5_merge.sh
    └── 6_img_to_video.sh
```

#### Step 0
```
cd scripts
bash 0_clear_workspace.sh
```
A new directory named `workspace` will be created in the root directory. Copy the source video and target video into this directory, and rename them as `source.mp4` and `target.mp4`.

#### Step 1
```
cd scripts
bash 1_video_to_img.sh
```
The videos will be split into frames.

#### Step 2
```
cd scripts
bash 2_face_extraction.sh
```
By 3DDFA, faces are extracted, along with face masks and transformation matrices.

#### Step 3
To viusalize the training process, `visdom` module is used, and it can be started by running this line in another shell.
```
python -m visdom.server
```
Then the loss curve and real-time output can be viewed online.
```
cd scripts
bash 3_train_swapper.sh
```

#### Step 3.1 (Alternate)
```
cd scripts
bash 3_1_train_swapper_dfl.sh
```
We offer an option to train without progressive training. If applied, the pipeline is similar to DeepFake.

#### Step 4
```
cd scripts
bash 4_gen_swap_face.sh
```
Generate the swapped faces by the trained model.

#### Step 5
```
cd scripts
bash 5_merge.sh
```
Merge the fake faces to target person.

#### Step 6
```
cd scripts
bash 6_img_to_video.sh
```
Combine all the frames together to produce the final video.

## Training Parameters

| Name      | Description |
| ----------- | ----------- |
| -b      | batch size       |
| -e   | number of epoch        |
| -lr   | learning rate     |
| -r   | resolution    |
| -cl   | number of common layers on decoder  |
| -n   | number of people  |
| -M   | max number of training images used |
| --cuda   | use GPU  |
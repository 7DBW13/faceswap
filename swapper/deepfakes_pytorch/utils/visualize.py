from pathlib import Path
import cv2
import numpy as np
import os
import torch
import math
from matplotlib import pyplot as plt
import multiprocessing
import time
import pickle


def get_image_list(path2dir, max_img_num):
    '''
    get the image paths from the path2dir
    '''

    dir_path = Path(path2dir)
    if not dir_path.exists():
        raise ValueError("the path to image dir doesn't exist")
    images = []
    selected = []
    for root, directory, filenames in os.walk(dir_path):
        for file in filenames:
            if(Path(file).suffix == '.jpg' or Path(file).suffix == '.png'):
                images.append(Path(os.path.join(root, file)))

    for i in range(0, len(images), int(len(images)/max_img_num)+1):
        selected.append(images[i])
    selected.sort()
    return selected


def get_label_images(image_batch, size=(128, 128)):
    label = []
    for i in range(image_batch.shape[0]):
        b, g, r = image_batch[i][0], image_batch[i][1], image_batch[i][2]
        image = np.stack((b, g, r), axis=-1)
        image = cv2.resize(image, size)
        b, g, r = cv2.split(image)
        b, g, r = b[np.newaxis][:], g[np.newaxis][:], r[np.newaxis][:]
        out = np.vstack((b, g, r))
        label.append(out)
    return np.array(label, dtype=np.float32)


def get_label_mask(image_batch, size=(128, 128)):
    label = []
    for i in range(image_batch.shape[0]):
        mask = cv2.resize(image_batch[i][0], size)
        mask = mask[np.newaxis][:]
        label.append(mask)
    return np.array(label, dtype=np.float32)


def visualize_output(name, batch_image):
    imgs = batch_image.transpose(1, 3)*255
    num_images, h, w = imgs.size()[0:3]
    cols = 2
    rows = math.ceil(num_images/cols)
    window = np.zeros((cols*w, rows*h, 3))

    images = imgs.type(torch.uint8).cpu().numpy()
    for i in range(num_images):
        r = i//cols
        c = i % cols
        img = images[i]
        window[c*w:(c+1)*w, r*h:(r+1)*h, :] = img

    # cv2.imshow(name, cv2.cvtColor(
    #     images[0].astype(np.uint8), cv2.COLOR_RGB2BGR))
    cv2.imshow(name, window.astype(np.uint8))
    cv2.waitKey(1)

def visualize_listoutput(name,saving_dir=None,iter=0,*batch_images):
    col= len(batch_images)
    num_images,h,w = batch_images[0].transpose(1,3).size()[0:3]
    window = np.zeros((num_images*h,col*w,3))
    c=0
    for batch in batch_images:
        imgs=batch.transpose(1, 3)*255
        images = imgs.type(torch.uint8).cpu().numpy()
        for i in range(num_images):
            img=images[i]
            window[i*h:(i+1)*h,c*w:(c+1)*w,:]=img
        c+=1
    cv2.imshow(name, window.astype(np.uint8))
    # if saving path is not None ,save the result to show
    if saving_dir is not None:
        if not os.path.exists(saving_dir):
            os.mkdir(saving_dir)
        save_path=os.path.join(saving_dir,"{:05d}".format(iter)+".png")
        cv2.imwrite(save_path,window)
    cv2.waitKey(1)

def umeyama(src, dst, estimate_scale):
    """Estimate N-D similarity transformation with or without scaling.
    Parameters
    ----------
    src : (M, N) array
        Source coordinates.
    dst : (M, N) array
        Destination coordinates.
    estimate_scale : bool
        Whether to estimate scaling factor.
    Returns
    -------
    T : (N + 1, N + 1)
        The homogeneous similarity transformation matrix. The matrix contains
        NaN values only if the problem is not well-conditioned.
    References
    ----------
    .. [1] "Least-squares estimation of transformation parameters between two
            point patterns", Shinji Umeyama, PAMI 1991, DOI: 10.1109/34.88573
    """

    num = src.shape[0]
    dim = src.shape[1]

    # Compute mean of src and dst.
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)

    # Subtract mean from src and dst.
    src_demean = src - src_mean
    dst_demean = dst - dst_mean

    # Eq. (38).
    A = np.dot(dst_demean.T, src_demean) / num

    # Eq. (39).
    d = np.ones((dim,), dtype=np.double)
    if np.linalg.det(A) < 0:
        d[dim - 1] = -1

    T = np.eye(dim + 1, dtype=np.double)

    U, S, V = np.linalg.svd(A)

    # Eq. (40) and (43).
    rank = np.linalg.matrix_rank(A)
    if rank == 0:
        return np.nan * T
    elif rank == dim - 1:
        if np.linalg.det(U) * np.linalg.det(V) > 0:
            T[:dim, :dim] = np.dot(U, V)
        else:
            s = d[dim - 1]
            d[dim - 1] = -1
            T[:dim, :dim] = np.dot(U, np.dot(np.diag(d), V))
            d[dim - 1] = s
    else:
        T[:dim, :dim] = np.dot(U, np.dot(np.diag(d), V.T))

    if estimate_scale:
        # Eq. (41) and (42).
        scale = 1.0 / src_demean.var(axis=0).sum() * np.dot(S, d)
    else:
        scale = 1.0

    T[:dim, dim] = dst_mean - scale * np.dot(T[:dim, :dim], src_mean.T)
    T[:dim, :dim] *= scale

    return T

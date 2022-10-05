# CRDDC2022
Crowdsensing-based Road Damage Detection Challenge 2022
# SGG-RS-GROUP submission
This repository contains source code and trained models for Crowdsensing-based Road Damage Detection Challenge 2022 that was held as a part of 2022 IEEE Big Data conference.

The best results:

① Overall (6 countries): 0.727400750059923

② India: 0.544689286943075

③ Japan: 0.726542388326749

④ Norway: 0.480894358569388

⑤ United States: 0.779325357306657

Average F1-Score achieved： 0.651770

## Table of Contents

* [Introduction](#introduction)
* [Install](#install)
* [Preparation](#preparation)
* [Detection and Submission](#detection-and-submission)
* [Results](#results)
* [Training](#training)

## Introduction
The best results were obtained by the ***ensemble model*** with ***test time augmentation*** based on the modified ***[YOLOv5](https://github.com/ultralytics/yolov5/tree/v6.0)*** with ***attention modules***. Details:
### Modified YOLOv5 with attention modules
The ***[Squeeze-and-Excitation Block](https://github.com/hujie-frank/SENet)*** (SE) and the ***[Coordinate Attention Block](https://github.com/Andrew-Qibin/CoordAttention)*** (CA) were used. There are five modified YOLOv5 models:
- ***YOLOv5_SE***: The SE block is incorporated before the tenth layer (i.e., the SPPF layer) of YOLOv5.
- ***YOLOv5_CA***: The CA block is incorporated after the tenth layer (i.e., the SPPF layer) of YOLOv5.
- ***YOLOv5_BB***: Three CA blocks are incorporated in the backbone.
- ***YOLOv5_HD***: Three CA blocks are incorporated in the head.
- ***YOLOv5_BBHD***: Three CA blocks are incorporated in the backbone of YOLOv5, while three CA blocks are incorporated in the head of YOLOv5.
### Test Time Augmentation
The input image is processed by scaling, flipping, etc. Then the model needs to predict both the original image and the transformed ones. Finally the merged results by using *non-maximum suppression* (NMS) method will be returned.
### Ensemble Model
The used ensemble method works with the output of the models. The ensemble model contains multiple models, and each model needs to predict the input image.
## Install
This code is based on the [YOLOv5](https://github.com/ultralytics/yolov5/tree/v6.0).
Use `requirements.txt` to install required python dependencies:
```
pip install -r requirements.txt
```
## Preparation
1. Download and unzip the [RDD2022 dataset](https://github.com/sekilab/RoadDamageDetector) in `yolov5/datasets/RDD2022`.
**RDD2022 dataset tree structure:**
```
datasets
|
└─RDD2022
    ├─China_Drone
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    ├─China_MotorBike
    │  ├─test
    │  │  └─images
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    ├─Czech
    │  ├─test
    │  │  └─images
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    ├─India
    │  ├─test
    │  │  └─images
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    ├─Japan
    │  ├─test
    │  │  └─images
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    ├─Norway
    │  ├─test
    │  │  └─images
    │  └─train
    │      ├─annotations
    │      │  └─xmls
    │      └─images
    └─United_States
        ├─test
        │  └─images
        └─train
            ├─annotations
            │  └─xmls
            └─images
```
2. Go to `yolov5` directory:
```
cd yolov5
```
3. Use `prepare/Norway_resize.py` to resize the images from Norway to 640×640:
```
python prepare/Norway_resize.py
```
4. Use `prepare/prepare_data_txt.py` to create `datasets/RDD2022/train.txt`, `datasets/RDD2022/val.txt` and `datasets/RDD2022/test.txt`:
```
python prepare/prepare_data_txt.py
```
5. Use `prepare/prepare_test_imgs.py` to move test images to `datasets/RDD2022/testimgs`. Note that test images from `Norway` and `China_Drone` are not included. There will be 6,995 images under `datasets/RDD2022/testimgs`.
```
python prepare/prepare_data_txt.py
```
6. Download weights in [SGG-RS-GROUP Model Zoo](https://drive.google.com/drive/folders/16oJ03noL5DE1-D1HLUAxSEP0lixbbfnf?usp=sharing). Then move the weights to `weights/`. Details of the training process are in [Training](#training).
## Detection and Submission
During the detection process, images of Norway were adjusted to a fixed 1280 width due to the large original size. Images of all other countries were resized to 640×640.

Remember to delete or move the existing `.csv` file before getting the results each time to prevent confusion.

1. Get the best detection results for ***Norway*** test set:
   - Use the ensemble model of ***YOLOv5_SE***, ***YOLOv5_CA***, ***YOLOv5_BB***, and ***YOLOv5_HD***:
    ```
    python detect.py --weights weights/yolov5_SE.pt weights/yolov5_CA.pt weights/yolov5_backbone.pt weights/yolov5_head.pt --img 1280 --source datasets/RDD2022/Norway/test/images --conf-thres 0.2 --iou-thres 0.999 --agnostic-nms --augment
    ```
    - The results are saved in `RDD2022_Norway.csv` under `yolov5/`.

2. Get the best detection results for ***India***, ***Japan***, ***United States*** test set
    * Use the ensemble model of all six models (original YOLOv5, and five modified YOLOv5 models):
    ```
    python detect.py --weights weights/yolov5_origin.pt weights/yolov5_SE.pt weights/yolov5_CA.pt weights/yolov5_backbone.pt weights/yolov5_head.pt weights/yolov5_backbone_head.pt --img 640 --source datasets/RDD2022/testimgs --conf-thres 0.2 --iou-thres 0.999 --agnostic-nms --augment
    ```
    * The results are saved in `RDD2022__China__Czech__India__Japan__United_States.csv` under `yolov5/`. Split the test results of each country:
    ```
    python prepare/split_predict.py
    ```
    * The results are saved in `yolov5/RDD2022_India.csv`, `yolov5/RDD2022_Japan.csv`, and `RDD2022_United_States.csv`.

3. Get the best detection results for ***all countries*** test set
    * Use the ensemble model of ***YOLOv5***, ***YOLOv5_SE***, ***YOLOv5_CA***, ***YOLOv5_BB***, and ***YOLOv5_HD*** to predict ***Norway*** test set:
    ```
    python detect.py --weights weights/yolov5_origin.pt weights/yolov5_SE.pt weights/yolov5_CA.pt weights/yolov5_backbone.pt weights/yolov5_head.pt --img 1280 --source datasets/RDD2022/Norway/test/images --conf-thres 0.2 --iou-thres 0.999 --agnostic-nms --augment
    ```
    * Use the same ensemble model to predict ***China***, ***Czech***, ***India***, ***Japan***, and ***United States*** test set:
    ```
    python detect.py --weights weights/yolov5_origin.pt weights/yolov5_SE.pt weights/yolov5_CA.pt weights/yolov5_backbone.pt weights/yolov5_head.pt --img 640 --source datasets/RDD2022/testimgs --conf-thres 0.2 --iou-thres 0.999 --agnostic-nms --augment
    ```
    * Merge the results:
    ```
    python prepare/merge_predict.py
    ```
    * The results are saved in `yolov5/RDD2022_allcountries.csv`.

## Results
The performance on the test set.
| model | 6 countries  | India | Japan | Norway| United States |
| -------- | -------- | -------- | -------- | --------| --------|
| YOLOv5 | 0.692628705 | 0.500088075 | 0.687858782 | 0.428820566 | 0.730890487 |
| YOLOv5_SE | 0.695626061 | 0.510223108 | 0.687713701 | 0.436399512 | 0.746002804 |
| YOLOv5_CA | 0.695138906 | 0.503787389 | 0.685749183 | 0.434805323 | 0.7403341 |
| YOLOv5_BB | 0.697378149 | 0.497351033 | 0.687480584 | 0.441600782 | 0.746825919 |
| YOLOv5_HD | 0.69653853 | 0.498276749 | 0.691392403 | 0.442335774 | 0.749298545 |
| YOLOv5_BBHD | 0.698419224 | 0.526107253 | 0.690392969 | 0.43993245 | 0.729384189 |
| **Ensemble Model** <br> YOLOv5_SE, YOLOv5_CA, YOLOv5_BB, YOLOv5_HD | ————— | —————  |  —————  | **0.480894359** | —————  |
| **Ensemble Model** <br> YOLOv5, YOLOv5_SE, YOLOv5_CA, YOLOv5_BB, YOLOv5_HD | **0.72740075** |  —————  |  —————  |  —————  |  —————  |
| **Ensemble Model** <br> all six models  |  —————  | **0.544689287** | **0.726542388** |  —————  | **0.779325357** |

## Training
All models are trained with the **same** hyperparameters.

1. Download [pre-trained weights](https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5x.pt) of YOLOv5, and move it to `yolov5/weights/yolov5x.pt`
2. Train YOLOv5:
   ```
   python train.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```
3. Train YOLOv5_SE:
   ```
   python train_yolov5_SE.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_SE_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```
4. Train YOLOv5_CA:
   ```
   python train_yolov5_CA.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_CA_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```
5. Train YOLOv5_BB:
   ```
   python train_yolov5_backbone.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_backbone_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```
6. Train YOLOv5_HD:
   ```
   python train.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_head_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```
7. Train YOLOv5_BBHD:
   ```
   python train_yolov5_backbone.py --img 640 --data data/CRDDC2022.yaml --epochs 100 --cfg models/yolov5x_backbone_head_RDD.yaml --weights weights/yolov5x.pt --batch-size 16 --workers 0
   ```

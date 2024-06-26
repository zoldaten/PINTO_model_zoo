# Gold-YOLO-Body-Head-Hand

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10229410.svg)](https://doi.org/10.5281/zenodo.10229410)

Lightweight human detection model generated using a high-quality human dataset. I annotated all the data by myself. Extreme resistance to blur and occlusion. In addition, the recognition rate at short, medium, and long distances has been greatly enhanced. The camera's resistance to darkness and halation has been greatly improved.

`Head` does not mean `Face`. Thus, the entire head is detected rather than a narrow region of the face. This makes it possible to detect all 360° head orientations.

## 1. Dataset
  - COCO-Hand (14,667 Images, 66,903 labels, All re-annotated manually)
  - http://vision.cs.stonybrook.edu/~supreeth/COCO-Hand.zip
  - I am adding my own enhancement data to COCO-Hand and re-annotating all images. In other words, only COCO images were cited and no annotation data were cited.
  - I have no plans to publish my own dataset.
    ```
    body_label_count: 30,729 labels
    head_label_count: 26,268 labels
    hand_label_count: 18,087 labels
    ===============================
               Total: 66,903 labels
               Total: 14,667 images
    ```
    ![image](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/22b56779-928b-44d8-944c-25431b83e24f)

## 2. Annotation

  Halfway compromises are never acceptable.

  ![000000000544](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/557b932b-767b-4f8c-87f5-75f403fa9c50)

  ![000000000716](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/9acb2308-eba1-4a05-91ed-ccbb6e122f67)

  ![000000002470](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/c1809eeb-7b2c-41de-a519-9834c804c656)

  ![icon_design drawio (3)](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/72740ed3-ae9f-4ab7-9b20-bea62c58c7ac)

## 3. Test
  - Python 3.10
  - onnxruntime-gpu v1.16.1 (TensorRT Execution Provider Enabled Binary)
  - opencv-contrib-python 4.8.0.76
  - numpy 1.24.3
  - TensorRT 8.5.3-1+cuda11.8

  With CUDA. TensorRT not used. Approximately twice as fast with TensorRT enabled. (250 FPS)

  ```
  usage: demo_goldyolo_onnx.py [-h] [-m MODEL] [-v VIDEO]
  
  options:
    -h, --help            show this help message and exit
    -m MODEL, --model MODEL
    -v VIDEO, --video VIDEO
  ```

  - 640x480 CUDA RTX3070

    ```bash
    python demo/demo_goldyolo_onnx.py \
    -m gold_yolo_n_body_head_hand_post_0461_0.4428_1x3x480x640.onnx \
    -v 0
    ```

    https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/de3f24db-051d-4c84-8348-2369b084c589

  - 320x256 CPU Corei9

    ```bash
    python demo/demo_goldyolo_onnx.py \
    -m gold_yolo_n_body_head_hand_post_0461_0.4428_1x3x256x320.onnx \
    -v 0
    ```

    https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/97c33beb-58d8-401e-b2fa-2e24e195fddd

  - 160x128 CPU Corei9

    ```bash
    python demo/demo_goldyolo_onnx.py \
    -m gold_yolo_n_body_head_hand_post_0461_0.4428_1x3x128x160.onnx \
    -v 0
    ```

    https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/2d73c77f-bdfd-4b10-9d7a-27ca1f038e96

  - Still image

    ```
    usage: demo_goldyolo_onnx_image.py [-h] [-m MODEL] [-i IMAGES_PATH] [-o OUTPUT_PATH]
    
    options:
      -h, --help            show this help message and exit
      -m MODEL, --model MODEL
      -i IMAGES_PATH, --images_path IMAGES_PATH
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
    ```

    ```bash
    python demo/demo_goldyolo_onnx_image.py \
    -m gold_yolo_n_body_head_hand_post_0461_0.4428_1x3x480x640.onnx \
    -i images_folder
    ```

    ![000000000764](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/ec57bec0-6655-499f-a78a-072082da38ac)

    ![image](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/4e8582a9-f223-4bb8-a244-85a6f83832a7)

- Body-Head-Hand - N
  ```
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.443
  Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.689
  Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.467
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.303
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.654
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.830
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.135
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.389
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.515
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.381
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.739
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.872
  Results saved to runs/train/gold_yolo-n
  Epoch: 462 | mAP@0.5: 0.6892104619015829 | mAP@0.50:0.95: 0.4427396559181031

  Class Labeled_images Labels P@.5iou R@.5iou F1@.5iou mAP@.5 mAP@.5:.95
  all              486   8858   0.856    0.62    0.719  0.689      0.443
  body             486   3747   0.857    0.60    0.706  0.662      0.440
  head             475   3269   0.912    0.68    0.779  0.726      0.497
  hand             483   1842   0.842    0.59    0.694  0.680      0.391
  ```

- Body-Head-Hand - S
  ```
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.460
  Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.704
  Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.491
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.327
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.665
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.838
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.137
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.399
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.526
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.397
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.739
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.874
  Results saved to runs/train/gold_yolo-s
  Epoch: 456 | mAP@0.5: 0.7040425163160517 | mAP@0.50:0.95: 0.46049785564440426

  Class Labeled_images Labels P@.5iou R@.5iou F1@.5iou mAP@.5 mAP@.5:.95
  all              486   8858   0.852    0.65    0.738  0.704      0.460
  body             486   3747   0.848    0.63    0.723  0.669      0.455
  head             475   3269   0.919    0.69    0.788  0.730      0.511
  hand             483   1842   0.814    0.65    0.723  0.712      0.415
  ```

- Body-Head-Hand - M
  ```
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.500
  Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.738
  Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.540
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.359
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.722
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.864
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.143
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.427
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.562
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.430
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.788
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.892
  Results saved to runs/train/gold_yolo-m
  Epoch: 488 | mAP@0.5: 0.7378339081274632 | mAP@0.50:0.95: 0.5004409472223532

  Class Labeled_images Labels P@.5iou R@.5iou F1@.5iou mAP@.5 mAP@.5:.95
  all              486   8858   0.872    0.68    0.764  0.738      0.500
  body             486   3747   0.895    0.64    0.746  0.701      0.499
  head             475   3269   0.937    0.71    0.808  0.751      0.536
  hand             483   1842   0.842    0.69    0.759  0.762      0.466
  ```

- Body-Head-Hand - L
  ```
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.509
  Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.739
  Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.556
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.367
  Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.729
  Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.869
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.146
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.432
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.567
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.434
  Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.792
  Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.903
  Results saved to runs/train/gold_yolo-l
  Epoch: 339 | mAP@0.5: 0.7393661924683652 | mAP@0.50:0.95: 0.5093183767567647

  Class Labeled_images Labels P@.5iou R@.5iou F1@.5iou mAP@.5 mAP@.5:.95
  all              486   8858   0.890    0.68    0.771  0.740      0.509
  body             486   3747   0.880    0.66    0.754  0.704      0.509
  head             475   3269   0.933    0.71    0.806  0.751      0.540
  hand             483   1842   0.843    0.70    0.765  0.765      0.479
  ```

- Post-Process

  Because I add my own post-processing to the end of the model, which can be inferred by TensorRT, CUDA, and CPU, the benchmarked inference speed is the end-to-end processing speed including all pre-processing and post-processing. EfficientNMS in TensorRT is very slow and should be offloaded to the CPU.

  ![image](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/05e528b7-6ace-4878-94f0-ad86ac46324e)

## 4. Citiation
  If this work has contributed in any way to your research or business, I would be happy to be cited in your literature.
  ```
  @software{Gold-YOLO-Body-Head-Hand,
    author={Katsuya Hyodo},
    title={Lightweight human detection model generated using a high-quality human dataset},
    url={https://github.com/PINTO0309/PINTO_model_zoo/tree/main/425_Gold-YOLO-Body-Head-Hand},
    year={2023},
    month={11},
    doi={10.5281/zenodo.10229410},
  }
  ```

## 5. Cited
  I am very grateful for their excellent work.
  - COCO-Hand

    https://vision.cs.stonybrook.edu/~supreeth/
  
    ```
    @article{Hand-CNN,
      title={Contextual Attention for Hand Detection in the Wild},
      author={Supreeth Narasimhaswamy and Zhengwei Wei and Yang Wang and Justin Zhang and Minh Hoai},
      booktitle={International Conference on Computer Vision (ICCV)},
      year={2019},
      url={https://arxiv.org/pdf/1904.04882.pdf}
    }
    ```
  - Gold-YOLO

    https://github.com/huawei-noah/Efficient-Computing/tree/master/Detection/Gold-YOLO

    ```
    @misc{wang2023goldyolo,
      title={Gold-YOLO: Efficient Object Detector via Gather-and-Distribute Mechanism}, 
      author={Chengcheng Wang and Wei He and Ying Nie and Jianyuan Guo and Chuanjian Liu and Kai Han and Yunhe Wang},
      year={2023},
      eprint={2309.11331},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
    }
    ```
    
## 6. TODO
- [ ] Synthesize and retrain the dataset to further improve model performance. [CD-COCO: Complex Distorted COCO database for Scene-Context-Aware computer vision](https://github.com/aymanbegh/cd-coco)
  ![image](https://github.com/PINTO0309/PINTO_model_zoo/assets/33194443/69603b9b-ab9f-455c-a9c9-c818edc41dba)
  ```
  @INPROCEEDINGS{10323035,
    author={Beghdadi, Ayman and Beghdadi, Azeddine and Mallem, Malik and Beji, Lotfi and Cheikh, Faouzi Alaya},
    booktitle={2023 11th European Workshop on Visual Information Processing (EUVIP)}, 
    title={CD-COCO: A Versatile Complex Distorted COCO Database for Scene-Context-Aware Computer Vision}, 
    year={2023},
    volume={},
    number={},
    pages={1-6},
    doi={10.1109/EUVIP58404.2023.10323035}}
  ```

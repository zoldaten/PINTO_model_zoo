#!/usr/bin/env python

"""
This demo code is designed to run a lightweight model for edge devices
at high speed instead of degrading accuracy due to INT8 quantization.
Automatic determination of the runtime that should be executed based
on the file extension.

runtime: https://github.com/microsoft/onnxruntime
runtime: https://github.com/PINTO0309/TensorflowLite-bin
"""
from __future__ import annotations
import os
import sys
import copy
import cv2
import time
import numpy as np
from enum import Enum
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import Tuple, Optional, List, Dict
import importlib.util
from abc import ABC, abstractmethod

class Color(Enum):
    BLACK          = '\033[30m'
    RED            = '\033[31m'
    GREEN          = '\033[32m'
    YELLOW         = '\033[33m'
    BLUE           = '\033[34m'
    MAGENTA        = '\033[35m'
    CYAN           = '\033[36m'
    WHITE          = '\033[37m'
    COLOR_DEFAULT  = '\033[39m'
    BOLD           = '\033[1m'
    UNDERLINE      = '\033[4m'
    INVISIBLE      = '\033[08m'
    REVERSE        = '\033[07m'
    BG_BLACK       = '\033[40m'
    BG_RED         = '\033[41m'
    BG_GREEN       = '\033[42m'
    BG_YELLOW      = '\033[43m'
    BG_BLUE        = '\033[44m'
    BG_MAGENTA     = '\033[45m'
    BG_CYAN        = '\033[46m'
    BG_WHITE       = '\033[47m'
    BG_DEFAULT     = '\033[49m'
    RESET          = '\033[0m'

    def __str__(self):
        return self.value

    def __call__(self, s):
        return str(self) + str(s) + str(Color.RESET)

@dataclass(frozen=False)
class Box():
    classid: int
    score: float
    x1: int
    y1: int
    x2: int
    y2: int

class AbstractModel(ABC):
    """AbstractModel
    Base class of the model.
    """
    _runtime: str = 'onnx'
    _model_path: str = ''
    _class_score_th: float = 0.35
    _input_shapes: List[List[int]] = []
    _input_names: List[str] = []
    _output_shapes: List[List[int]] = []
    _output_names: List[str] = []

    # onnx/tflite
    _interpreter = None
    _inference_model = None
    _providers = None
    _swap = (2, 0, 1)
    _h_index = 2
    _w_index = 3

    # onnx
    _onnx_dtypes_to_np_dtypes = {
        "tensor(float)": np.float32,
        "tensor(uint8)": np.uint8,
        "tensor(int8)": np.int8,
    }

    # tflite
    _input_details = None
    _output_details = None

    @abstractmethod
    def __init__(
        self,
        *,
        runtime: Optional[str] = 'onnx',
        model_path: Optional[str] = '',
        score_threshold: Optional[float] = 0.50,
        iou_threshold: Optional[float] = 0.40,
        providers: Optional[List] = [
            (
                'TensorrtExecutionProvider', {
                    'trt_engine_cache_enable': True,
                    'trt_engine_cache_path': '.',
                    'trt_fp16_enable': True,
                }
            ),
            'CUDAExecutionProvider',
            'CPUExecutionProvider',
        ],
    ):
        self._runtime = runtime
        self._model_path = model_path
        self._score_threshold = score_threshold
        self._iou_threshold = iou_threshold
        self._providers = providers

        # Model loading
        if self._runtime == 'onnx':
            import onnxruntime # type: ignore
            session_option = onnxruntime.SessionOptions()
            session_option.log_severity_level = 3
            self._interpreter = \
                onnxruntime.InferenceSession(
                    model_path,
                    sess_options=session_option,
                    providers=providers,
                )
            self._providers = self._interpreter.get_providers()
            self._input_shapes = [
                input.shape for input in self._interpreter.get_inputs()
            ]
            self._input_names = [
                input.name for input in self._interpreter.get_inputs()
            ]
            self._input_dtypes = [
                self._onnx_dtypes_to_np_dtypes[input.type] for input in self._interpreter.get_inputs()
            ]
            self._output_shapes = [
                output.shape for output in self._interpreter.get_outputs()
            ]
            self._output_names = [
                output.name for output in self._interpreter.get_outputs()
            ]
            self._model = self._interpreter.run
            self._swap = (2, 0, 1)
            self._h_index = 2
            self._w_index = 3

        elif self._runtime in ['tflite_runtime', 'tensorflow']:
            if self._runtime == 'tflite_runtime':
                from tflite_runtime.interpreter import Interpreter # type: ignore
                self._interpreter = Interpreter(model_path=model_path)
            elif self._runtime == 'tensorflow':
                import tensorflow as tf # type: ignore
                self._interpreter = tf.lite.Interpreter(model_path=model_path)
            self._input_details = self._interpreter.get_input_details()
            self._output_details = self._interpreter.get_output_details()
            self._input_shapes = [
                input.get('shape', None) for input in self._input_details
            ]
            self._input_names = [
                input.get('name', None) for input in self._input_details
            ]
            self._input_dtypes = [
                input.get('dtype', None) for input in self._input_details
            ]
            self._output_shapes = [
                output.get('shape', None) for output in self._output_details
            ]
            self._output_names = [
                output.get('name', None) for output in self._output_details
            ]
            self._model = self._interpreter.get_signature_runner()
            self._swap = (0, 1, 2)
            self._h_index = 1
            self._w_index = 2

    @abstractmethod
    def __call__(
        self,
        *,
        input_datas: List[np.ndarray],
    ) -> List[np.ndarray]:
        datas = {
            f'{input_name}': input_data \
                for input_name, input_data in zip(self._input_names, input_datas)
        }
        if self._runtime == 'onnx':
            outputs = [
                output for output in \
                    self._model(
                        output_names=self._output_names,
                        input_feed=datas,
                    )
            ]
            return outputs
        elif self._runtime in ['tflite_runtime', 'tensorflow']:
            outputs = [
                output for output in \
                    self._model(
                        **datas
                    ).values()
            ]
            return outputs

    @abstractmethod
    def _preprocess(
        self,
        *,
        image: np.ndarray,
        swap: Optional[Tuple[int,int,int]] = (2, 0, 1),
    ) -> np.ndarray:
        pass

    @abstractmethod
    def _postprocess(
        self,
        *,
        image: np.ndarray,
        boxes: np.ndarray,
    ) -> List[Box]:
        pass


class YOLOX(AbstractModel):
    def _create_grids_and_expanded_strides(
        self,
        *,
        strides: List[int],
    ):
        grids = []
        expanded_strides = []
        hsizes = [self._input_shapes[0][self._h_index] // stride for stride in strides]
        wsizes = [self._input_shapes[0][self._w_index] // stride for stride in strides]
        for hsize, wsize, stride in zip(hsizes, wsizes, strides):
            xv, yv = np.meshgrid(np.arange(wsize), np.arange(hsize))
            grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
            grids.append(grid)
            shape = grid.shape[:2]
            expanded_strides.append(np.full((*shape, 1), stride))
        grids = np.concatenate(grids, 1)
        expanded_strides = np.concatenate(expanded_strides, 1)
        return grids, expanded_strides

    def __init__(
        self,
        *,
        runtime: Optional[str] = 'onnx',
        model_path: Optional[str] = 'yolox_ti_body_head_hand_n_1x3x256x320_uint8.onnx',
        score_threshold: Optional[float] = 0.50,
        iou_threshold: Optional[float] = 0.40,
        providers: Optional[List] = None,
    ):
        """YOLOX

        Parameters
        ----------
        runtime: Optional[str]
            Runtime for YOLOX. Default: onnx

        model_path: Optional[str]
            ONNX/TFLite file path for YOLOX

        class_score_th: Optional[float]
            Score threshold. Default: 0.35

        providers: Optional[List]
            Providers for ONNXRuntime.
        """
        super().__init__(
            runtime=runtime,
            model_path=model_path,
            score_threshold=score_threshold,
            iou_threshold=iou_threshold,
            providers=providers,
        )
        self.strides = [8, 16, 32]
        self.grids, self.expanded_strides = \
            self._create_grids_and_expanded_strides(strides=self.strides)

    def __call__(
        self,
        image: np.ndarray,
    ) -> List[Box]:
        """YOLOX

        Parameters
        ----------
        image: np.ndarray
            Entire image

        Returns
        -------
        boxes: np.ndarray
            Predicted boxes: [N, x1, y1, x2, y2]

        scores: np.ndarray
            Predicted box scores: [N, score]
        """
        temp_image = copy.deepcopy(image)

        # PreProcess
        resized_image = \
            self._preprocess(
                temp_image,
            )

        # Inference
        inferece_image = np.asarray([resized_image], dtype=self._input_dtypes[0])
        outputs = super().__call__(input_datas=[inferece_image])
        boxes = outputs[0]
        result_boxes = \
            self._postprocess(
                image=temp_image,
                output_blob=boxes,
            )
        return result_boxes

    def _preprocess(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """_preprocess

        Parameters
        ----------
        image: np.ndarray
            Entire image

        swap: tuple
            HWC to CHW: (2,0,1)
            CHW to HWC: (1,2,0)
            HWC to HWC: (0,1,2)
            CHW to CHW: (0,1,2)

        Returns
        -------
        resized_image: np.ndarray
            Resized and normalized image.
        """
        # Resize + Transpose
        resized_image = cv2.resize(
            image,
            (
                int(self._input_shapes[0][self._w_index]),
                int(self._input_shapes[0][self._h_index]),
            )
        )
        resized_image = resized_image.transpose(self._swap)
        return resized_image

    def _postprocess(
        self,
        image: np.ndarray,
        output_blob: np.ndarray,
    ) -> List[Box]:
        """_postprocess

        Parameters
        ----------
        image: np.ndarray
            Entire image.

        boxes: np.ndarray
            float32[1, N, 8]

        Returns
        -------
        result_boxes: List[Box]
            Predicted boxes: [classid, score, x1, y1, x2, y2]
        """
        image_height = image.shape[0]
        image_width = image.shape[1]
        resize_ratio_w = self._input_shapes[0][self._w_index] / image_width
        resize_ratio_h = self._input_shapes[0][self._h_index] / image_height

        # Box encoding
        output_blob[..., :2] = (output_blob[..., :2] + self.grids) * self.expanded_strides
        output_blob[..., 2:4] = np.exp(output_blob[..., 2:4]) * self.expanded_strides
        predictions: np.ndarray = output_blob[0]
        boxes = predictions[:, :4]
        """boxes: [N,cx,cy,w,h]
            ┌───────┐
            │       │
            │[cx,cy]| h
            │       │
            └───────┘
                w
        """
        boxes_xywh = np.ones_like(boxes)
        boxes[:, 0] = boxes[:, 0] / resize_ratio_w
        boxes[:, 1] = boxes[:, 1] / resize_ratio_h
        boxes[:, 2] = boxes[:, 2] / resize_ratio_w
        boxes[:, 3] = boxes[:, 3] / resize_ratio_h
        boxes_xywh[:, 0] = (boxes[:, 0] - boxes[:, 2] * 0.5)
        boxes_xywh[:, 1] = (boxes[:, 1] - boxes[:, 3] * 0.5)
        boxes_xywh[:, 2] = ((boxes[:, 0] + boxes[:, 2] * 0.5) - boxes_xywh[:, 0])
        boxes_xywh[:, 3] = ((boxes[:, 1] + boxes[:, 3] * 0.5) - boxes_xywh[:, 1])
        scores = predictions[:, 4:5] * predictions[:, 5:]
        class_ids = scores.argmax(1)
        scores = scores[np.arange(len(class_ids)), class_ids]

        # NMS - OpenCV DNN
        """boxes_xywh: [N,x,y,w,h]
        [x,y]
            ┌───────┐
            │       │
            │       │ h
            │       │
            └───────┘
                w
        """
        indices = \
            cv2.dnn.NMSBoxesBatched(
                bboxes=boxes_xywh,
                scores=scores,
                class_ids=class_ids,
                score_threshold=self._score_threshold,
                nms_threshold=self._iou_threshold,
            ) # OpenCV 4.7.0 or later
        boxes_xywh_keep = []
        scores_keep = []
        class_ids_keep = []
        for index in indices:
            boxes_xywh_keep.append(boxes_xywh[index])
            scores_keep.append(scores[index])
            class_ids_keep.append(class_ids[index])
        if len(boxes_xywh_keep) > 0:
            boxes_xywh_keep = np.vectorize(int)(boxes_xywh_keep)

        result_boxes: List[Box] = []
        if len(boxes_xywh_keep) > 0:
            """box: [x,y,w,h]
            [x,y]
                ┌───────┐
                │       │
                │       │ h
                │       │
                └───────┘
                    w
            """
            for box, score, classid in zip(boxes_xywh_keep, scores_keep, class_ids_keep):
                x_min = int(max(0, box[0]))
                y_min = int(max(0, box[1]))
                x_max = int(min(box[0]+box[2], image_width))
                y_max = int(min(box[1]+box[3], image_height))
                result_boxes.append(
                    Box(
                        classid=int(classid),
                        score=float(score),
                        x1=x_min,
                        y1=y_min,
                        x2=x_max,
                        y2=y_max,
                    )
                )

        return result_boxes


def is_parsable_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_package_installed(package_name: str):
    """Checks if the specified package is installed.

    Parameters
    ----------
    package_name: str
        Name of the package to be checked.

    Returns
    -------
    result: bool
        True if the package is installed, false otherwise.
    """
    return importlib.util.find_spec(package_name) is not None

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-m',
        '--model',
        type=str,
        default='yolox_ti_body_head_hand_n_1x3x256x320_uint8.onnx',
        help='ONNX/TFLite file path for YOLOX.',
    )
    parser.add_argument(
        '-st',
        '--score_threshold',
        type=float,
        default=0.50,
        help='NMS score threshold.',
    )
    parser.add_argument(
        '-it',
        '--iou_threshold',
        type=float,
        default=0.40,
        help='NMS IoU threshold.',
    )
    parser.add_argument(
        '-v',
        '--video',
        type=str,
        default="0",
        help='Video file path or camera index.',
    )
    parser.add_argument(
        '-ep',
        '--execution_provider',
        type=str,
        choices=['cpu', 'cuda'], # 'tensorrt'
        default='cpu',
        help='Execution provider for ONNXRuntime.',
    )
    parser.add_argument(
        '-dvw',
        '--disable_video_writer',
        action='store_true',
        help=\
            'Disable video writer. '+
            'Eliminates the file I/O load associated with automatic recording to MP4. '+
            'Devices that use a MicroSD card or similar for main storage can speed up overall processing.',
    )
    args = parser.parse_args()

    # runtime check
    model_file: str = args.model
    model_ext: str = os.path.splitext(model_file)[1][1:].lower()
    runtime: str = None
    if model_ext == 'onnx':
        if not is_package_installed('onnxruntime'):
            print(Color.RED('ERROR: onnxruntime is not installed. pip install onnxruntime or pip install onnxruntime-gpu'))
            sys.exit(0)
        runtime = 'onnx'
    elif model_ext == 'tflite':
        if is_package_installed('tflite_runtime'):
            runtime = 'tflite_runtime'
        elif is_package_installed('tensorflow'):
            runtime = 'tensorflow'
        else:
            print(Color.RED('ERROR: tflite_runtime or tensorflow is not installed.'))
            print(Color.RED('ERROR: https://github.com/PINTO0309/TensorflowLite-bin'))
            print(Color.RED('ERROR: https://github.com/tensorflow/tensorflow'))
            sys.exit(0)
    video: str = args.video
    execution_provider: str = args.execution_provider
    providers: List[Tuple[str, Dict] | str] = None
    if execution_provider == 'cpu':
        providers = [
            'CPUExecutionProvider',
        ]
    elif execution_provider == 'cuda':
        providers = [
            'CUDAExecutionProvider',
            'CPUExecutionProvider',
        ]
    elif execution_provider == 'tensorrt':
        providers = [
            (
                'TensorrtExecutionProvider', {
                    'trt_engine_cache_enable': True,
                    'trt_engine_cache_path': '.',
                    'trt_fp16_enable': True,
                }
            ),
            'CUDAExecutionProvider',
            'CPUExecutionProvider',
        ]

    score_threshold: float = args.score_threshold
    iou_threshold: float = args.iou_threshold

    # Model initialization
    model = YOLOX(
        runtime=runtime,
        model_path=model_file,
        score_threshold=score_threshold,
        iou_threshold=iou_threshold,
        providers=providers,
    )

    cap = cv2.VideoCapture(
        int(video) if is_parsable_to_int(video) else video
    )
    disable_video_writer: bool = args.disable_video_writer
    video_writer = None
    if not disable_video_writer:
        cap_fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            filename='output.mp4',
            fourcc=fourcc,
            fps=cap_fps,
            frameSize=(w, h),
        )

    while cap.isOpened():
        res, image = cap.read()
        if not res:
            break

        debug_image = copy.deepcopy(image)
        # debug_image_h = debug_image.shape[0]
        debug_image_w = debug_image.shape[1]

        start_time = time.perf_counter()
        boxes = model(debug_image)
        elapsed_time = time.perf_counter() - start_time
        cv2.putText(
            debug_image,
            f'{elapsed_time*1000:.2f} ms',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            debug_image,
            f'{elapsed_time*1000:.2f} ms',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

        for box in boxes:
            color = (255,255,255)
            if box.classid == 0:
                color = (255,0,0)
            elif box.classid == 1:
                color = (0,0,255)
            elif box.classid == 2:
                color = (0,255,0)
            cv2.rectangle(
                debug_image,
                (box.x1, box.y1),
                (box.x2, box.y2),
                (255,255,255),
                2,
            )
            cv2.rectangle(
                debug_image,
                (box.x1, box.y1),
                (box.x2, box.y2),
                color,
                1,
            )
            cv2.putText(
                debug_image,
                f'{box.score:.2f}',
                (
                    box.x1 if box.x1+50 < debug_image_w else debug_image_w-50,
                    box.y1-10 if box.y1-25 > 0 else 20
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                debug_image,
                f'{box.score:.2f}',
                (
                    box.x1 if box.x1+50 < debug_image_w else debug_image_w-50,
                    box.y1-10 if box.y1-25 > 0 else 20
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                1,
                cv2.LINE_AA,
            )

        key = cv2.waitKey(1)
        if key == 27: # ESC
            break

        cv2.imshow("test", debug_image)
        if video_writer is not None:
            video_writer.write(debug_image)

    if video_writer is not None:
        video_writer.release()

    if cap is not None:
        cap.release()

if __name__ == "__main__":
    main()

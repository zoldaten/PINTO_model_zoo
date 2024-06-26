# Demo projects

## Person Attributes Recognition with TensorFlow Lite in C++
https://github.com/iwatake2222/play_with_tflite/tree/master/pj_tflite_person-attributes-recognition-crossroad-0230

## person-attributes-recognition-crossroad-0230 with ONNX Runtime in Python
```
python demo_person-attributes-recognition-crossroad-0230_onnx.py
```

If you want to change the model, specify it with an argument.<br>
Check the source code for other argument specifications.<br>
```python
    parser.add_argument(
        "--model",
        type=str,
        default='saved_model/model_float32.tflite',
    )
```

## person-attributes-recognition-crossroad-0230 with TensorFlow Lite in Python
```
python demo_person-attributes-recognition-crossroad-0230_tflite.py
```

If you want to change the model, specify it with an argument.<br>
Check the source code for other argument specifications.<br>
```python
    parser.add_argument(
        "--model",
        type=str,
        default='saved_model/model_float32.tflite',
    )
```

## About sample images
The sample image uses the image of "[PAKUTASO](https://www.pakutaso.com/)".<br>
If you want to use the image itself for another purpose, you must follow the [userpolicy of PAKUTASO](https://www.pakutaso.com/userpolicy.html).


"""
To run the .tflite model in Termux, you need the lightweight tflite-runtime library. This allows your Android phone to use its hardware acceleration without the massive overhead of full TensorFlow.
1. Install Runtime in Termux

pip install tflite-runtime


2. TFLite Inference Script (run_tflite.py)
This script loads your optimized model and measures how fast it processes a single puzzle state.


"""

import numpy as np
import tflite_runtime.interpreter as tflite
import time

def predict_tflite(model_path, input_data):
    # 1. Load the model and allocate tensors
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # 2. Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 3. Prepare input (54 stickers)
    input_data = np.array([input_data], dtype=np.float32)
    
    # 4. Measure speed
    start_time = time.time()
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    end_time = time.time()

    prediction = np.argmax(output_data)
    print(f"Prediction: {prediction} | Latency: {(end_time - start_time)*1000:.2f}ms")
    return prediction

# Test with mock state
mock_state = [random.randint(0, 5) for _ in range(54)]
predict_tflite("expert_model.tflite", mock_state)

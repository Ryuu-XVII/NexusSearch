# Intel NPU Optimization Pipeline

This document explains how NexusSearch AI leverages Intel Core Ultra NPU (AI Boost) using OpenVINO.

## 1. Why OpenVINO and Intel NPU?

Standard PyTorch models execute sequentially on the CPU, causing high latency for semantic searches. The Intel NPU is a dedicated AI accelerator that uses low power while providing high throughput for parallel operations (like matrix multiplications in Transformers).

## 2. Optimization Pipeline

Our pipeline uses the HuggingFace `optimum-intel` library, which provides a seamless bridge between standard Transformers and OpenVINO runtime.

### Conversion (`scripts/convert_models.py`)
1. **Load Standard Model**: PyTorch model is downloaded from HF Hub.
2. **ONNX Export**: The model is traced and exported to ONNX format.
3. **OpenVINO IR Compilation**: The Model Optimizer converts the ONNX graph into OpenVINO IR (`.xml` and `.bin` files), optimizing graph operations, folding constants, and fusing layers.
4. **Quantization (Optional/Advanced)**: Weights can be compressed to INT8 using Neural Network Compression Framework (NNCF) to double throughput with minimal accuracy loss.

### Inference Execution (`app/embeddings.py`)
- We use `OVModelForFeatureExtraction` initialized with `device="AUTO"`.
- The `AUTO` plugin queries the system for available execution units (CPU, integrated GPU, dedicated GPU, NPU).
- It transparently routes inference to the NPU if available. 
- **Latency Target**: We aim for <50ms per batch of embeddings when routed through the NPU.

## 3. Benchmarking
To benchmark, we recommend writing a simple script that measures time-to-first-token using the native PyTorch model vs. the OpenVINO NPU-accelerated model. Expect to see at least a 2-4x speedup on Core Ultra chips.

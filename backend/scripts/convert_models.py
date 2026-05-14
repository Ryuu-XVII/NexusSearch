from optimum.intel import OVModelForFeatureExtraction
from transformers import AutoTokenizer
import os

def convert_model(model_id: str, save_dir: str):
    print(f"Exporting {model_id} to OpenVINO format...")
    # export=True forces ONNX export then OpenVINO IR conversion
    ov_model = OVModelForFeatureExtraction.from_pretrained(model_id, export=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    os.makedirs(save_dir, exist_ok=True)
    ov_model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Model successfully saved to {save_dir}")

if __name__ == "__main__":
    # all-MiniLM-L6-v2 is compact and excellent for fast semantic search
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    save_dir = os.path.join(os.path.dirname(__file__), "..", "app", "models", "ov_all_MiniLM_L6_v2")
    
    convert_model(model_id, save_dir)
    print("Run app with this model_path pointing to 'ov_all_MiniLM_L6_v2'")

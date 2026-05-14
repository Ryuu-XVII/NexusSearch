import logging

logger = logging.getLogger(__name__)

class OpenVINOEmbedder:
    def __init__(self, model_path: str, device: str = "AUTO"):
        self.device = device
        self.model_path = model_path
        self.model = None

    def load_model(self):
        try:
            from optimum.intel import OVModelForFeatureExtraction
            from transformers import AutoTokenizer
            import os
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            if self.device == "NPU":
                self.model = OVModelForFeatureExtraction.from_pretrained(
                    self.model_path, 
                    device=self.device,
                    compile=False
                )
                self.model.reshape(1, 512)
                self.model.compile()
            else:
                self.model = OVModelForFeatureExtraction.from_pretrained(
                    self.model_path, 
                    device=self.device
                )
            self.is_openvino = True
            logger.info("OpenVINO model loaded successfully.")
        except Exception as e:
            logger.warning(f"OpenVINO failed ({e}). Falling back to native SentenceTransformer.")
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.is_openvino = False

    def encode(self, texts: list[str]) -> list[list[float]]:
        if not self.model:
            self.load_model()
            
        if not self.is_openvino:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
            
        import torch
        
        if self.device == "NPU":
            all_embeddings = []
            for text in texts:
                inputs = self.tokenizer(text, padding="max_length", max_length=512, truncation=True, return_tensors="pt")
                with torch.no_grad():
                    outputs = self.model(**inputs)
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                embeddings = sum_embeddings / sum_mask
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                all_embeddings.append(embeddings[0].tolist())
            return all_embeddings
        else:
            inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)
            attention_mask = inputs['attention_mask']
            token_embeddings = outputs.last_hidden_state
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            embeddings = sum_embeddings / sum_mask
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            return embeddings.tolist()

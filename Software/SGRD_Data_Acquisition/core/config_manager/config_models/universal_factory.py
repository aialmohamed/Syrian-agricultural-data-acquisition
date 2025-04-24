# universal_factory.py
from typing import Any
from core.config_manager.config_models.model_registry import MODEL_REGISTRY

def from_config(config: dict) -> Any:
    for key, model_cls in MODEL_REGISTRY.items():
        if key in config:
            value = config.get(key, config)
            if isinstance(value, dict):
                print(f"🧩 Matched key '{key}' → {model_cls.__name__}")
                return model_cls(**value)
            return model_cls(**config)
    raise ValueError("❌ No matching model found in config keys.")

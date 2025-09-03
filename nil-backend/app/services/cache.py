import hashlib
import json
from typing import Any, Dict, Optional


class InMemoryCache:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def _key(self, namespace: str, payload: Dict) -> str:
        raw = json.dumps(payload, sort_keys=True)
        h = hashlib.sha256(raw.encode()).hexdigest()
        return f"{namespace}:{h}"

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get_or_set_hashed(self, namespace: str, payload: Dict, value_fn):
        key = self._key(namespace, payload)
        existing = self.get(key)
        if existing is not None:
            return existing
        value = value_fn()
        self.set(key, value)
        return value

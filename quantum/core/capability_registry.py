from dataclasses import dataclass
from typing import Callable


@dataclass
class PhysicsCapability:
    name: str
    description: str
    category: str
    handler: Callable


class QuantumCapabilityRegistry:
    def __init__(self):
        self._capabilities = {}

    def register(self, capability: PhysicsCapability):
        self._capabilities[capability.name] = capability

    def get(self, name: str):
        return self._capabilities.get(name)

    def list_capabilities(self):
        return list(self._capabilities.values())

    def find(self, query: str):
        query = query.lower()

        results = []

        for capability in self._capabilities.values():
            searchable = (
                capability.name.lower()
                + " "
                + capability.description.lower()
                + " "
                + capability.category.lower()
            )

            if query in searchable:
                results.append(capability)

        return results


registry = QuantumCapabilityRegistry()

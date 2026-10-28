from quantum.core.capability_registry import registry
from quantum.core.register_capabilities import register_quantum_capabilities


class QuantumQueryEngine:
    def __init__(self):
        register_quantum_capabilities()

    def find_capabilities(self, question: str):
        question = question.strip().lower()

        if not question:
            return []

        results = registry.find(question)

        if results:
            return results

        keyword_groups = {
            "quantum_tunneling": [
                "tunneling",
                "tunnel",
                "barrier",
                "potential barrier",
            ],
            "harmonic_oscillator": [
                "harmonic oscillator",
                "oscillator",
                "energy levels",
            ],
            "superposition": [
                "superposition",
                "measurement",
                "probability",
            ],
            "operators_eigenstates": [
                "operator",
                "eigenstate",
                "eigenvalue",
            ],
            "bloch_sphere": [
                "bloch",
                "spin",
                "qubit state",
            ],
            "interactive_bloch_sphere": [
                "interactive bloch",
                "theta",
                "phi",
            ],
            "quantum_gates": [
                "quantum gate",
                "gate",
                "hadamard",
                "pauli",
                "qubit",
            ],
        }

        matches = []

        for capability_name, keywords in keyword_groups.items():
            if any(keyword in question for keyword in keywords):
                capability = registry.get(capability_name)

                if capability and capability not in matches:
                    matches.append(capability)

        return matches

    def analyze(self, question: str):
        matches = self.find_capabilities(question)

        return {
            "question": question,
            "matches": [
                {
                    "name": capability.name,
                    "category": capability.category,
                    "description": capability.description,
                }
                for capability in matches
            ],
        }


if __name__ == "__main__":
    engine = QuantumQueryEngine()

    test_questions = [
        "What is quantum tunneling?",
        "Show me the harmonic oscillator",
        "Explain quantum superposition",
        "What are quantum gates?",
        "Show the Bloch sphere",
    ]

    print("Quantum Query Engine")
    print("====================")
    print()

    for question in test_questions:
        result = engine.analyze(question)

        print(f"Question: {question}")

        if result["matches"]:
            for match in result["matches"]:
                print(
                    f"  -> {match['name']} "
                    f"[{match['category']}]"
                )
        else:
            print("  -> No matching capability found")

        print()

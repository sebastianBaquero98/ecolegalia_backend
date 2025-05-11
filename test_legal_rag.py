#!/usr/bin/env python

import logging
from legal_rag_tool import consultar_base_legal

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_consultar_base_legal():
    """Test the legal database query function with metadata filters."""
    print("\n--- Test with string metadata values ---")
    result1 = consultar_base_legal._run(
        query="licencia ambiental",
        metadata_filters={
            "tipo_acto": "Decreto",
            "año": "2020"
        },
        top_k=2
    )
    print(result1)
    
    print("\n--- Test with list metadata values ---")
    result2 = consultar_base_legal._run(
        query="licencia ambiental",
        metadata_filters={
            "tipo_acto": ["Decreto", "Concepto"],
            "año": ["2019", "2020"]
        },
        top_k=2
    )
    print(result2)
    
    print("\n--- Test with automatic filter detection ---")
    result3 = consultar_base_legal._run(
        query="Requisitos para licencia ambiental en proyectos mineros según decreto de 2015",
        top_k=2
    )
    print(result3)

if __name__ == "__main__":
    test_consultar_base_legal() 
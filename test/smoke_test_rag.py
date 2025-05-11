import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legal_rag_tool import consultar_base_legal, index, embeddings

def test_basic_query():
    # Print index statistics
    #print("\nPinecone Index Statistics:")
    #print(f"Index name: {index.describe_index_stats()}")
    
    # Test a simple query
    print("\nTesting simple query:")
    #query = "Parque Nacional Natural Los Corales del Rosario y de San Bernardo"
    #print(f"Query: {query}")
    
    # Get and print the embedding
    #query_embedding = embeddings.embed_query(query)
    #print(f"Embedding dimension: {len(query_embedding)}")
    
    # Make the query
    # s
    
    # If we have results, show more details
    # if out_no_filters['matches']:
    #     print("\nFirst match details:")
    #     first_match = out_no_filters['matches'][0]
    #     print(f"Score: {first_match.get('score', 'N/A')}")
    #     print(f"Metadata: {first_match.get('metadata', {})}")
    # """Test the legal database query function with metadata filters."""
    # print("\n--- Test with string metadata values ---")
    # result1 = consultar_base_legal._run(
    #     query="licencia ambiental",
    #     metadata_filters={
    #         "tipo_acto": "Auto",
    #     },
    #     top_k=2
    # )
    # print(result1)
    
    # print("\n--- Test with list metadata values ---")
    # result2 = consultar_base_legal._run(
    #     query="Autónomas Regionales",
    #     metadata_filters={
    #         "tipo_acto": ["Concepto Jurídico"],
    #         "año": ["2023", "2024"]
    #     },
    #     top_k=5
    # )
    # print(result2)
    
    print("\n--- Test with automatic filter detection ---")
    result3 = consultar_base_legal._run(
        query="¿Qué diligencia específica ordena el Artículo Tercero sobre el muelle del predio “Isla Vigía” y con qué propósito ambiental se practica?",
    )
    print(result3)
    # Assertions
    #assert len(out_no_filters['matches']) > 0, "No results found in Pinecone index"
    #"print("\n✅ RAG tool smoke test passed")


if __name__ == "__main__":
    test_basic_query()

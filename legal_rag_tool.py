from langchain_core.tools import tool
from pinecone import Pinecone
from typing import Optional, Dict, List, Any, Union, Type
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import json
import logging
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

try:
    # Inicializar cliente Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "normas")
    index = pc.Index(index_name)
    
    # Inicializar embeddings con el modelo text-embedding-3-small
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    logger.info(f"Conexión exitosa a Pinecone. Índice: {index_name}")
    logger.info(f"Usando modelo de embeddings: text-embedding-3-small")
except Exception as e:
    logger.error(f"Error al inicializar Pinecone: {str(e)}")
    raise


class ConsultarBaseLegalInput(BaseModel):
    """Input schema for ConsultarBaseLegal tool."""
    query: str = Field(..., description="La pregunta o consulta legal para la que necesitas información.")
    metadata_filters: Optional[Dict[str, Union[str, List[str]]]] = Field(
        None, 
        description="Filtros de metadata opcionales para refinar la búsqueda. Puede incluir 'nombre', 'tipo_acto' y/o 'año'. Ejemplo: {'tipo_acto': 'Concepto Jurídico', 'año': '2020'}"
    )
    top_k: int = Field(10, description="Número de resultados a devolver (por defecto 10).")


class ConsultarBaseLegalTool(BaseTool):
    name: str = "Consulta Base Legal"
    description: str = """
    Consulta la base de datos vectorial que contiene más de 7GB de documentos ambientales legales colombianos.
    
    Esta herramienta te permite:
    1. Buscar información legal relevante para responder consultas específicas
    2. Filtrar por tipo de documento (Auto, Concepto Jurídico, Decreto, Anexo, Formato, Guía)
    3. Filtrar por año del documento
    4. Filtrar por nombre del documento
    
    IMPORTANTE: Considera que los documentos tienen metadata que puedes usar para filtrar y obtener
    resultados más precisos:
    - nombre: nombre del archivo del documento
    - tipo_acto: categoría del documento (Auto, Concepto Jurídico, Decreto, Anexo, Formato, Guía)
    - año: año de emisión del documento
    """
    args_schema: Type[BaseModel] = ConsultarBaseLegalInput

    def _sugerir_filtros_metadata(self, query: str) -> Dict[str, Any]:
        """
        Sugiere filtros de metadata basados en la consulta del usuario.
        """
        filtros: Dict[str, Any] = {}
        años = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', query)
        if años:
            filtros["año"] = años[0] if len(años) == 1 else años
        tipos_docs = {
            "Auto": ["auto", "autos"],
            "Concepto Jurídico": ["concepto", "conceptos", "opinión jurídica"],
            "Decreto": ["decreto", "decretos"],
            "Anexo": ["anexo", "anexos"],
            "Formato": ["formato", "formatos"],
            "Guia": ["guia", "guías", "guía"]
        }
        for tipo, palabras in tipos_docs.items():
            for palabra in palabras:
                if re.search(r'\b' + palabra + r'\b', query.lower()):
                    filtros["tipo_acto"] = tipo
                    break
        logger.info(f"Filtros automáticos sugeridos: {filtros}")
        return filtros

    def _run(
        self,
        query: str,
        metadata_filters: Optional[Dict[str, Union[str, List[str]]]] = None,
        top_k: int = 10
    ) -> Dict[str, Any]:
        """
        Consulta la base de datos vectorial de documentos legales para encontrar información relevante.
        Retorna un diccionario con dos claves:
        - matches: lista de matches completos (to_dict)
        - summary: nombres de los 3 primeros documentos
        """
        try:
            logger.info(f"Consultando base legal con query: {query}")
            logger.info(f"Filtros de metadata originales: {metadata_filters}")
            filtros_auto = self._sugerir_filtros_metadata(query)
            filtros_finales: Dict[str, Any] = {}
            if metadata_filters:
                if isinstance(metadata_filters, str):
                    try:
                        metadata_filters = json.loads(metadata_filters)
                        logger.info(f"Convertido metadata_filters de string a dict: {metadata_filters}")
                    except Exception:
                        logger.warning("No se pudo parsear metadata_filters, se ignora formato string.")
                if isinstance(metadata_filters, dict):
                    filtros_finales.update(metadata_filters)
            for k, v in filtros_auto.items():
                if k not in filtros_finales:
                    filtros_finales[k] = v
            filter_dict: Dict[str, Any] = {}
            if "nombre" in filtros_finales:
                val = filtros_finales["nombre"]
                filter_dict["nombre"] = {"$eq": val} if isinstance(val, str) else {"$in": val}
            if "tipo_acto" in filtros_finales:
                val = filtros_finales["tipo_acto"]
                filter_dict["tipo_acto"] = {"$eq": val} if isinstance(val, str) else {"$in": val}
            if "año" in filtros_finales:
                val = filtros_finales["año"]
                filter_dict["año"] = {"$eq": val} if isinstance(val, str) else {"$in": val}

            # Embedding y query
            query_embedding = embeddings.embed_query(query)
            logger.info(f"Realizando consulta a Pinecone con filtros: {filter_dict}")
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                filter=filter_dict if filter_dict else None,
                include_metadata=True,
                namespace="ambiental"
            )

            # Si no hay matches
            if not results.matches:
                return {"matches": [], "summary": []}

            # Logging y summary
            logger.info(f"Pinecone devolvió {len(results.matches)} matches")
            for m in results.matches:
                nm = m.metadata.get("nombre", "<unknown>")
                logger.info(f" • {nm} (score={m.score:.2f})")
            summary = [m.metadata.get("nombre", "") for m in results.matches]

            # Construir lista de matches completos
            matches = [m.to_dict() for m in results.matches]

            return {
                "matches": matches,
                "summary": summary
            }

        except Exception as e:
            logger.error(f"Error al consultar la base de datos legal: {str(e)}")
            return {"matches": [], "summary": [], "error": str(e)}

# Instancia de la herramienta para usar directamente
consultar_base_legal = ConsultarBaseLegalTool()

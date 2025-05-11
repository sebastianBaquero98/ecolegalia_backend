# Herramienta RAG para Investigación Legal

Esta herramienta implementa un sistema de Retrieval Augmented Generation (RAG) optimizado para consultar una base de datos vectorial de documentos legales colombianos alojada en Pinecone.

## Características principales

- **Consulta semántica**: Busca documentos relevantes basados en el significado de la consulta, no solo en coincidencias de palabras clave.
- **Filtrado por metadata**: Permite refinar búsquedas por tipo de documento, año y nombre.
- **Detección automática de filtros**: Identifica automáticamente años y tipos de documentos mencionados en la consulta.
- **Integración con CrewAI**: Se integra perfectamente con el sistema de agentes de investigación legal.

## Componentes

El sistema consta de los siguientes componentes:

1. **legal_rag_tool.py**: Implementación base de la herramienta RAG con Pinecone.
2. **legal_research_tool.py**: Wrapper para CrewAI que facilita el uso por parte de los agentes.
3. **Integración en agents.py**: Configuración de los agentes para utilizar la herramienta.
4. **Actualización en tasks.py**: Instrucciones específicas para el uso óptimo de la herramienta.

## Configuración

1. Renombra `example.env` a `.env` y configura las siguientes variables:

   ```
   OPENAI_API_KEY=tu_clave_api_de_openai
   PINECONE_API_KEY=tu_clave_api_de_pinecone
   PINECONE_INDEX_NAME=nombre_del_indice_pinecone
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso por el agente de investigación legal

El agente de investigación legal está configurado para utilizar la herramienta RAG como su primera fuente de información, siguiendo este protocolo:

1. **Consulta inicial**: El agente formula una consulta precisa basada en la pregunta original.
2. **Aplicación de filtros**: Utiliza filtros de metadata para refinar la búsqueda cuando es pertinente.
3. **Análisis de resultados**: Extrae información relevante de los documentos recuperados.
4. **Refinamiento**: Si es necesario, reformula la consulta o ajusta los filtros para obtener resultados más precisos.
5. **Complemento con búsqueda web**: Complementa la información con búsquedas en fuentes web oficiales.

## Ejemplo de consulta

```python
# Consulta simple
resultado = legal_database_tool._run(
    query="Requisitos para obtener licencia ambiental para proyectos mineros"
)

# Consulta con filtros específicos
resultado = legal_database_tool._run(
    query="Requisitos para licencia ambiental",
    metadata_filters={"tipo_acto": "Decreto", "año": "2015"},
    top_k=15
)

# Consulta con detección automática de filtros
resultado = legal_database_tool._run(
    query="Decretos de 2018 sobre licencias ambientales",
    use_auto_filters=True
)
```

## Estructura de metadata

La base de datos legal utiliza la siguiente estructura de metadata:

- **nombre**: Nombre del archivo/documento
- **tipo_acto**: Categoría del documento (Auto, Concepto, Decreto, Anexo, Formato, Guía)
- **año**: Año de emisión del documento

## Mejores prácticas para el agente de investigación

1. **Consultas específicas**: Formular consultas precisas y específicas a la base de datos.
2. **Uso estratégico de filtros**: Aplicar filtros de metadata cuando se tiene información sobre el tipo de documento o año.
3. **Iteración**: Si los resultados iniciales no son satisfactorios, reformular la consulta y ajustar filtros.
4. **Verificación cruzada**: Contrastar la información obtenida con fuentes web oficiales.
5. **Documentación**: Registrar detalladamente las consultas realizadas y los resultados obtenidos.

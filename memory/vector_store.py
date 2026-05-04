import chromadb
from chromadb.config import Settings
import uuid
from schemas.research_finding import ResearchFindingSchema
from schemas.financial_analysis import FinancialAnalysisSchema


# Initialize ChromaDB client (persistent)
_chroma_client = chromadb.Client(
    Settings(
        persist_directory="memory/.chroma",
        anonymized_telemetry=False
    )
)

# Create / load collections
_research_collection = _chroma_client.get_or_create_collection(
    name="research_findings"
)

_financial_collection = _chroma_client.get_or_create_collection(
    name="financial_analysis"
)



def store_research_finding(finding: ResearchFindingSchema):
    """
    Stores a research finding in the vector store.
    """
    # Generate a unique ID for this finding
    doc_id = f"{finding.ticker}_research_{uuid.uuid4()}"

    # Text used for embedding
    embedding_text = f"{finding.headline}. {finding.summary}"

    # Structured metadata
    metadata = {
        "ticker": finding.ticker,
        "source": finding.source,
        "published_date": (
            finding.published_date.isoformat()
            if finding.published_date
            else None
        ),
        "relevance_score": finding.relevance_score,
        "tags": ",".join(finding.tags) if finding.tags else None,

    }

    # Remove None values (Chroma metadata constraint safety)
    metadata = {k: v for k, v in metadata.items() if v is not None}
    

    # Store in ChromaDB
    _research_collection.add(
        documents=[embedding_text],
        metadatas=[metadata],
        ids=[doc_id],
    )



def store_financial_analysis(analysis: FinancialAnalysisSchema):
    """
    Stores a financial analysis in the vector store.
    Overwrites any existing analysis for the same ticker.
    """
    # Deterministic ID per ticker (overwrite-safe)
    doc_id = f"{analysis.ticker}_financial_analysis"

    # Text used for embedding
    embedding_text = analysis.analyst_notes

    # Structured metadata (flattened scalars only)
    metadata = {
        "ticker": analysis.ticker,
        "price_current": analysis.price_current,
        "price_change_pct": analysis.price_change_pct,
        "pe_ratio": analysis.pe_ratio,
        "roe": analysis.roe,
        "debt_to_equity": analysis.debt_to_equity,
        "revenue_growth_yoy": analysis.revenue_growth_yoy,
        "eps_growth_yoy": analysis.eps_growth_yoy,
        "volatility": analysis.volatility,
    }

    # Remove None values (Chroma metadata constraint safety)
    metadata = {k: v for k, v in metadata.items() if v is not None}

    _financial_collection.add(
        documents=[embedding_text],
        metadatas=[metadata],
        ids=[doc_id],
    )



def retrieve_context(ticker: str):
    """
    Retrieves all relevant context for a given ticker from the vector store.
    """
    # Retrieve research findings
    research_results = _research_collection.get(
        where={"ticker": ticker}
    )

    research_findings = []
    for metadata in research_results.get("metadatas", []):
        research_findings.append(metadata)

    # Retrieve financial analysis (single document)
    financial_results = _financial_collection.get(
        ids=[f"{ticker}_financial_analysis"]
    )

    financial_analysis = None
    if financial_results.get("metadatas"):
        financial_analysis = financial_results["metadatas"][0]

    return {
        "research_findings": research_findings,
        "financial_analysis": financial_analysis,
    }

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline

# Path to FAISS index
FAISS_INDEX = "vectorstore/"

def create_qa_pipeline():
    """
    Create the Question-Answering pipeline with a free Hugging Face model.
    """
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load the existing FAISS vector store
    db = FAISS.load_local(
        FAISS_INDEX, 
        embeddings, 
        allow_dangerous_deserialization=True  # Only if you trust the source of the vector store
    )

    # Custom Prompt Template
    custom_prompt = PromptTemplate(
        template="""[INST] <<SYS>>
You are an expert assistant specializing in Indian Law. Answer the question based on the given context.
If the context does not provide enough information, honestly state that you cannot confidently answer.
<</SYS>>

Context:
{context}

Question:
{question}

Helpful Answer: [/INST]""",
        input_variables=["context", "question"]
    )

    # Load a small Hugging Face model (adjust as needed)
    model_name = "facebook/opt-350m"  # A smaller model for free usage

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Create a Hugging Face pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=200,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    # Convert the pipeline to a LangChain LLM
    llm = HuggingFacePipeline(pipeline=pipe)

    # Create a Retrieval QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Specify the chain type
        retriever=db.as_retriever(search_kwargs={"k": 2}),  # Adjust 'k' for relevance
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True  # Include source documents in the response
    )

    return qa_chain

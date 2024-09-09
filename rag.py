from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import prompt_template as promps

class ChatPDF:
    local_model = 'mistral'
    vector_store = None
    retriever = None
    chain = None
    active_prompt = None

    def __init__(self):
        self.model = ChatOllama(model=self.local_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.active_prompt = promps.prompt_base

    def switch_prompt(self):
        if self.active_prompt == promps.prompt_base:
            self.active_prompt = promps.prompt_athlete
        elif self.active_prompt == promps.prompt_athlete:
            self.active_prompt = promps.prompt_base

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3, # maximium results
                "score_threshold": 0.5, #min similarity
            },
        )
        self.prompt = PromptTemplate.from_template(self.active_prompt)
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."
        self.prompt = PromptTemplate.from_template(self.active_prompt)
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                | self.prompt
                | self.model
                | StrOutputParser())
        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
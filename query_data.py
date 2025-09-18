# Fix for SQLite version issue on Streamlit Cloud
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # pysqlite3 not available, use default sqlite3
    pass

import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def query_bot(query_text: str) -> dict:
    """
    Query the bot with a question and return the response.
    
    Args:
        query_text (str): The question to ask
        
    Returns:
        dict: Contains 'response' and 'success' keys
    """
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        results = db.similarity_search_with_relevance_scores(query_text, k=15)
        if len(results) == 0 or results[0][1] < 0.5:
            return {
                "response": "I couldn't find relevant information to answer your question. Could you try rephrasing it or asking something else about Kirill?",
                "success": False
            }

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI(model="gpt-5-mini")
        response_text = model.predict(prompt)

        return {
            "response": response_text,
            "success": True
        }
    
    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "success": False
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    result = query_bot(query_text)
    
    if result["success"]:
        print(f"Response: {result['response']}")
    else:
        print(result["response"])


if __name__ == "__main__":
    main()
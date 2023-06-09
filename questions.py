#questions.py
from utils import clean_and_tokenize, format_documents
# questions.py
from utils import format_documents
from file_processing import search_documents

class QuestionContext:
    def __init__(self, index, documents, llm_chain, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames):
@@ -14,11 +15,7 @@ def __init__(self, index, documents, llm_chain, model_name, repo_name, github_ur
        self.filenames = filenames

def ask_question(question, context: QuestionContext):
    tokenized_question = clean_and_tokenize(question)
    scores = context.index.get_scores(tokenized_question)
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
    similar_docs = [context.documents[i] for i in top_k_indices]
    relevant_docs = [doc for doc in similar_docs if len(set(tokenized_question).intersection(clean_and_tokenize(doc.page_content))) >= 3]
    relevant_docs = search_documents(question, context.index, context.documents, n_results=5)

    numbered_documents = format_documents(relevant_docs)
    question_context = f"This question is about the GitHub repository '{context.repo_name}' available at {context.github_url}. The most relevant documents are:\n\n{numbered_documents}"
@@ -30,6 +27,8 @@ def ask_question(question, context: QuestionContext):
        repo_name=context.repo_name,
        github_url=context.github_url,
        conversation_history=context.conversation_history,
        numbered_documents=numbered_documents
        numbered_documents=numbered_documents,
        file_type_counts=context.file_type_counts,
        filenames=context.filenames
    )
    return answer_with_sources

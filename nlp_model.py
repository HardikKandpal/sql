from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer, util

class NLPProcessor:
    def __init__(self, model_name="bert-base-uncased"):
        """Initialize BERT model for query classification and similarity checking."""
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")  # Faster sentence similarity model
        
        # Define known query templates
        self.known_queries = {
            "employees_in_department": "Show all employees in {department} department",
            "department_manager": "Who is the manager of {department} department?",
            "hired_after": "List employees hired after {date}",
            "salary_expense": "What is the total salary expense for {department} department?",
            "all_employees": "List all employees",
            "all_departments": "Show all departments"
        }
        
        # Precompute embeddings for known queries
        self.known_embeddings = {k: self.sentence_model.encode(v, convert_to_tensor=True) for k, v in self.known_queries.items()}

    def classify_query(self, query):
        """Determine the type of user query using semantic similarity."""
        query_embedding = self.sentence_model.encode(query, convert_to_tensor=True)
        
        best_match = None
        highest_score = -1
        
        for key, emb in self.known_embeddings.items():
            score = util.pytorch_cos_sim(query_embedding, emb).item()
            if score > highest_score:
                highest_score = score
                best_match = key
        
        # If similarity is below a threshold, return an error
        if highest_score < 0.7:
            return None, "Sorry, I didn't understand your query. Can you rephrase?"
        
        return best_match, None

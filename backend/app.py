from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database_setup import QueryProcessor
import os

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
CORS(app)

# Instantiate the QueryProcessor (ensure correct db path)
query_processor = QueryProcessor(db_path='data\company.db')
#query_processor = NLPQueryProcessor(db_path='data\company.db')

# Serve the main HTML page
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

# Serve static files like CSS and JS
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory("../frontend", path)

# API endpoint to handle the query
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get("query", "")

    # Use the QueryProcessor to process the query
    response = query_processor.process_query(query)
    
    # Return the response from the query processor
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


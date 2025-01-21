import logging
from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# pip install accelerate
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto")

# Set pad_token to eos_token (common practice for text generation models)
tokenizer.pad_token = tokenizer.eos_token

# Token limit for GPT-2 (important to ensure we don't exceed the model's token capacity)
MAX_TOKENS = 1024

@app.before_request
def log_request_info():
    logger.debug(f"Request Method: {request.method}")
    logger.debug(f"Request URL: {request.url}")
    logger.debug(f"Request Headers: {request.headers}")
    if request.method == "POST":
        logger.debug(f"Request Body: {request.get_data()}")

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    data = request.get_json()

    # Check if the necessary fields are in the request
    if not data or 'document' not in data or 'prompt' not in data:
        logger.error("Invalid input data received")
        return jsonify({'error': 'Invalid input, both document and prompt are required'}), 400

    document = data.get('document', '')  # Current content of the document
    prompt = data.get('prompt', '')      # User's prompt for the document

    # Modify the prompt to explicitly ask for a rewrite
    input_text = f"{prompt}: {document}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

    # Debug log the tokenization process
    logger.debug(f"Input text for model: {input_text}")
    logger.debug(f"Tokenized input: {input_ids}")

    # Check for token count and log if close to the limit
    input_length = input_ids.shape
    logger.debug(f"Input text contains: {input_length} tokens.")


    outputs = model.generate(input_ids)

    logger.debug(f"Tokenized output: {outputs}")

    # Decode the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Debug log the generated response
    logger.debug(f"Generated response: {response}")

    # Remove the original document from the generated output to avoid redundancy
    staged_changes = response  

    # Generate the updated document by applying staged changes
    updated_document = staged_changes  # Only the new generated text (the rewrite)

    return jsonify({
        'staged_changes': staged_changes,
        'updated_document': updated_document  # Return the updated document with improvements
    })
@app.route('/refine_changes', methods=['POST'])
def refine_changes():
    data = request.get_json()

    # Check if the necessary fields are in the request
    if not data or 'document' not in data or 'prompt' not in data:
        logger.error("Invalid input data received for refine_changes")
        return jsonify({'error': 'Invalid input, both document and prompt are required'}), 400

    document = data.get('document', '')
    prompt = data.get('prompt', '')

    # Log the input for refinement
    logger.debug(f"Refining with document: {document} and prompt: {prompt}")

    # Reuse the logic from process_prompt to avoid redundancy
    return process_prompt()  # This calls process_prompt internally to handle refinement

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, host="0.0.0.0", port=5000)
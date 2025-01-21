# inference_service.py

from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Initialize GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    data = request.get_json()
    document = data.get('document', '')  # Current content of the document
    prompt = data.get('prompt', '')      # User's prompt for the document

    # Combine document and prompt for context
    input_text = f"Document: {document}\n\nPrompt: {prompt}"

    # Tokenize and generate response
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(inputs['input_ids'], max_length=300)
    
    # Decode the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Staged changes can be returned here
    staged_changes = response[len(input_text):]  # Remove prompt context to get the staged changes

    return jsonify({
        'staged_changes': staged_changes,
        'current_document': document  # Return the document as-is for reference
    })

@app.route('/refine_changes', methods=['POST'])
def refine_changes():
    data = request.get_json()
    document = data.get('document', '')
    prompt = data.get('prompt', '')

    # Refine document with new prompt or changes
    return process_prompt()

if __name__ == '__main__':
    app.run(debug=True)

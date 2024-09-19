# OpenGPT

OpenGPT is a context-aware chatbot designed to provide precise and useful information from a comprehensive knowledge base. The chatbot integrates with various document formats and handles multiple use cases, including FAQs and escalation handling.

## API Usage

OpenGPT, powered by OpenAI API, can operate mostly offline after initial setup. However, embedding functionality and API calls require an internet connection to access the OpenAI services.

## Project Structure

The project is organized as follows:

- `OpenGPT/OpenAI/frontend/` - Contains the frontend application code.
- `OpenGPT/OpenAI/backend/` - Contains the backend application code.

## Tech Stack

- **Model**: OpenAI API for natural language processing - [OpenAI Documentation](https://beta.openai.com/docs/)
- **Text Extraction**: Tesseract OCR for optical character recognition - [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- **Image Processing**: PIL (Python Imaging Library) - [PIL Documentation](https://pillow.readthedocs.io/en/stable/)
- **Backend**: Flask (Python) - [Flask Documentation](https://flask.palletsprojects.com/en/latest/)
- **Frontend**: React (JavaScript) - [React Documentation](https://reactjs.org/docs/getting-started.html)
- **Session Management**: Chainlit - [Chainlit Documentation](https://docs.chainlit.io/)
- **Embeddings**: OpenAI API - [OpenAI Embeddings Documentation](https://beta.openai.com/docs/)
- **Vector Store**: ChromaDB - [ChromaDB Documentation](https://docs.trychroma.com/)

## Getting Started

To set up and run the project, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/msnabiel/OpenGPT.git
cd OpenGPT/OpenAI
```

### 2. Set Up Git LFS (Optional)

Ensure you have Git Large File Storage (LFS) installed and initialized (for handling large files, if any):

```bash
git lfs install
```

### 3. Set Up the Frontend

Navigate to the `frontend` folder and install dependencies:

```bash
cd frontend
npm install
```

### 4. Prepare Documents

Upload your documents to the `documents` folder located in the `backend` directory. Ensure the documents are properly formatted and ready for processing.

### 5. Set Up Your OpenAI API Key

1. Navigate to the `backend` directory:

   ```bash
   cd ../backend
   ```

2. Create a `.env` file in the `backend` directory and add your OpenAI API key:

   ```bash
   touch .env
   ```

3. Open the `.env` file and add your OpenAI API key like this:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Save the file.

### 6. Load Documents

Run the script to load the documents into the backend:

```bash
python load_documents.py
```

### 7. Start the Frontend

Navigate to the `frontend` folder and start the application:

```bash
cd ../frontend
npm start
```

### 8. Start the Backend

Navigate back to the `backend` folder and run the Flask server:

```bash
cd ../backend
python flask_server.py
```

### 9. Access the Application

Open your web browser and go to `http://localhost:3000` to log in. Register if you haven't already. If the page initially says "can't reach," wait for a moment as the application is loading. Reload the page if necessary, and it should appear.

## Contributing

If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out to [Nabiel](mailto:msyednabiel@gmail.com).

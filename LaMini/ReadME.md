# OpenGPT

OpenGPT is a context-aware chatbot designed to provide precise and useful information from a comprehensive knowledge base. The chatbot integrates with various document formats and handles multiple use cases, including FAQs and escalation handling.

## Project Structure

The project is organized as follows:

- `OpenGPT/LaMini/frontend/` - Contains the frontend application code.
- `OpenGPT/LaMini/backend/` - Contains the backend application code.
- `OpenGPT/LaMini/LaMini-T5-738M/` - Contains the model and related files.

## Getting Started

To set up and run the project, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/msnabiel/OpenGPT.git
cd OpenGPT/LaMini
```

### 2. Set Up Git LFS

Ensure you have Git Large File Storage (LFS) installed and initialized:

```bash
git lfs install
```

### 3. Clone the Model

Download the LaMini model into the `LaMini-T5-738M` folder:

```bash
git clone https://huggingface.co/MBZUAI/LaMini-T5-738M
```

### 4. Set Up the Frontend

Navigate to the `frontend` folder and install dependencies:

```bash
cd frontend
npm install
```

### 5. Prepare Documents

Upload your documents to the `documents` folder located in the `backend` directory. Ensure the documents are properly formatted and ready for processing.

### 6. Load Documents

Run the script to load the documents into the backend:

```bash
cd ../backend
python doc_load_combine.py
```

### 7. Start the Frontend

Navigate to the `frontend` folder and start the application:

```bash
cd ../frontend
npm start
```

### 8. Start the Backend

Navigate to the `backend` folder and run the Flask server:

```bash
cd ../backend
python flask_server.py
```

### 9. Access the Application

Open your web browser and go to `http://localhost:3000` to log in. Register if you haven't already. If the page initially says "can't reach," wait for a moment as the application is loading. Reload the page if necessary, and it should appear.

## Offline Usage

The OpenGPT application is designed to operate completely offline, with the exception of the embedding functionality. The embedding process can also be handled offline. The application does not require an internet connection for its core features once set up.

## Contributing

If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out to [Nabiel](mailto:msyednabiel@gmail.com).
```


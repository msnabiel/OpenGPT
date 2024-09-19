# OpenGPT

OpenGPT is a specialized chatbot framework that utilizes ChromaDB to deliver answers based solely on a specific knowledge base. It integrates with various language models, including OpenAI, Gemini, and LaMini, to provide precise information relevant to the context of the query. Users can upload documents to the knowledge base and modify it as needed to tailor the chatbot's responses to their requirements.

## Snapshots

![Diagram](images/image_1.png)

## Project Structure

The project contains the following key directories:

- **[OpenGPT/Gemini/](/Gemini/)** - Contains integration code for the Gemini API, including utilities for interacting with Gemini’s NLP models.
- **[OpenGPT/OpenAI/](/OpenAI/)** - Contains integration code for the OpenAI API, including utilities for leveraging OpenAI’s models.
- **[OpenGPT/LaMini/](/LaMini/)** - Contains integration code for LaMini models, including utilities for using these models in NLP tasks.

## Key Tech Stack

- **[OpenAI API](https://beta.openai.com/docs/)**: For natural language processing and embeddings.
- **[Gemini](https://cloud.google.com/ai-platform/gemini)**: For advanced generative AI tasks.
- **[LaMini](https://huggingface.co/MBZUAI/LaMini)**: For offline capabilities and document handling.
- **[Text Extraction](https://github.com/tesseract-ocr/tesseract)**: Tesseract OCR for optical character recognition.
- **[Image Processing](https://pillow.readthedocs.io/en/stable/)**: PIL (Python Imaging Library).
- **[Backend](https://flask.palletsprojects.com/en/latest/)**: Flask (Python).
- **[Frontend](https://reactjs.org/docs/getting-started.html)**: React (JavaScript).
- **[Session Management](https://docs.chainlit.io/)**: Chainlit.
- **[Vector Store](https://docs.trychroma.com/)**: ChromaDB.


## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request with your changes. Follow the guidelines provided in each directory for specific contribution instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out to [Nabiel](mailto:msyednabiel@gmail.com).

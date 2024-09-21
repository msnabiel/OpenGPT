from graphviz import Digraph

# Create a Digraph object
dfd = Digraph(comment='Highly Detailed Data Flow Diagram for OpenGPT', format='png')

# Define the external entities
dfd.node('User', 'User')  # The external user who interacts with the chatbot
dfd.node('Flask', 'Flask Server')  # Flask server managing API requests
dfd.node('Chainlit', 'Chainlit Chatbot UI')  # Chainlit chatbot interface

# Define the processes (with more granularity)
dfd.node('P1', 'Process: Handle Message (Chainlit)')
dfd.node('P1a', 'Subprocess: Validate User Input')
dfd.node('P1b', 'Subprocess: Prepare Query')

dfd.node('P2', 'Process: Query ChromaDB')
dfd.node('P2a', 'Subprocess: Create Embedding Function')
dfd.node('P2b', 'Subprocess: Search ChromaDB for Context')
dfd.node('P2c', 'Subprocess: Retrieve Contextual Data')

dfd.node('P3', 'Process: Generate Response (OpenAI)')
dfd.node('P3a', 'Subprocess: Send Query to OpenAI API')
dfd.node('P3b', 'Subprocess: Receive Response from OpenAI')
dfd.node('P3c', 'Subprocess: Format OpenAI Response')

dfd.node('P4', 'Process: Load Documents (Flask)')
dfd.node('P4a', 'Subprocess: Fetch Files from Directory')
dfd.node('P4b', 'Subprocess: Extract Text from Documents')
dfd.node('P4c', 'Subprocess: Store Extracted Text in ChromaDB')

dfd.node('P5', 'Process: Extract Text from Files')
dfd.node('P5a', 'Subprocess: Extract from PDF')
dfd.node('P5b', 'Subprocess: Extract from PPT')
dfd.node('P5c', 'Subprocess: Extract from Images')

# Define the data stores
dfd.node('D1', 'ChromaDB (Document Embeddings)', shape='cylinder')
dfd.node('D2', 'Document Files Directory', shape='cylinder')
dfd.node('D3', 'User Session Storage', shape='cylinder')

# Define external services
dfd.node('OpenAI', 'OpenAI API', shape='box')

# External User Interaction Flow
dfd.edge('User', 'Chainlit', label='User Query (Text)')
dfd.edge('Chainlit', 'P1', label='Forward Query')

# Subprocesses of Handle Message
dfd.edge('P1', 'P1a', label='Validate User Input')
dfd.edge('P1a', 'P1b', label='Input Validated')
dfd.edge('P1b', 'P2', label='Prepare and Forward Query')

# Subprocesses of Query ChromaDB
dfd.edge('P2', 'P2a', label='Create Embedding Function')
dfd.edge('P2a', 'P2b', label='Embedding Function Created')
dfd.edge('P2b', 'D1', label='Search for Relevant Context')
dfd.edge('D1', 'P2c', label='Return Contextual Data')
dfd.edge('P2c', 'P3', label='Forward Context and Query')

# Generate Response from OpenAI
dfd.edge('P3', 'P3a', label='Send Query to OpenAI')
dfd.edge('P3a', 'OpenAI', label='Call OpenAI API')
dfd.edge('OpenAI', 'P3b', label='Receive OpenAI Response')
dfd.edge('P3b', 'P3c', label='Format Response')
dfd.edge('P3c', 'P1', label='Send Response to Chainlit')
dfd.edge('P1', 'Chainlit', label='Send Response to User')
dfd.edge('Chainlit', 'User', label='Return Response')

# Document Loading and Text Extraction
dfd.edge('Flask', 'P4', label='Trigger Document Loading')
dfd.edge('P4', 'P4a', label='Fetch Files from Directory')
dfd.edge('P4a', 'D2', label='Read Files')
dfd.edge('D2', 'P4b', label='Return Files')
dfd.edge('P4b', 'P4c', label='Extract Text')
dfd.edge('P4c', 'D1', label='Store Extracted Text in ChromaDB')

# Text Extraction from Specific File Types
dfd.edge('P4b', 'P5', label='Process Extracted Text')
dfd.edge('P5', 'P5a', label='Extract from PDF')
dfd.edge('P5', 'P5b', label='Extract from PPT')
dfd.edge('P5', 'P5c', label='Extract from Images')

# User ID Handling (Flask)
dfd.edge('User', 'Flask', label='Send POST Request (User ID)')
dfd.edge('Flask', 'P4', label='Check or Fetch User ID')
dfd.edge('Flask', 'D3', label='Store User ID Temporarily')
dfd.edge('D3', 'Flask', label='Fetch User ID if Needed')
dfd.edge('Flask', 'User', label='Return Chainlit Chat URL')
dfd.edge('Flask', 'Chainlit', label='Send User ID to Chainlit')
dfd.render("OPRNGPT_DFD")

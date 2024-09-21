from graphviz import Digraph

# Create a Digraph object
dfd = Digraph(comment='Highly Detailed Data Flow Diagram for OpenGPT', format='png')

# Define the external entities with color
dfd.node('User', 'User', style='filled', color='lightblue')  # The external user who interacts with the chatbot
dfd.node('Flask', 'Flask Server', style='filled', color='lightcoral')  # Flask server managing API requests
dfd.node('Chainlit', 'Chainlit Chatbot UI', style='filled', color='lightgreen')  # Chainlit chatbot interface

# Define the processes (with different colors for each major process)
dfd.node('P1', 'Process: Handle Message (Chainlit)', style='filled', color='yellow')
dfd.node('P1a', 'Subprocess: Validate User Input', style='filled', color='yellowgreen')
dfd.node('P1b', 'Subprocess: Prepare Query', style='filled', color='yellowgreen')

dfd.node('P2', 'Process: Query ChromaDB', style='filled', color='lightpink')
dfd.node('P2a', 'Subprocess: Create Embedding Function', style='filled', color='lightcoral')
dfd.node('P2b', 'Subprocess: Search ChromaDB for Context', style='filled', color='lightcoral')
dfd.node('P2c', 'Subprocess: Retrieve Contextual Data', style='filled', color='lightcoral')

dfd.node('P3', 'Process: Generate Response (OpenAI)', style='filled', color='lightyellow')
dfd.node('P3a', 'Subprocess: Send Query to OpenAI API', style='filled', color='khaki')
dfd.node('P3b', 'Subprocess: Receive Response from OpenAI', style='filled', color='khaki')
dfd.node('P3c', 'Subprocess: Format OpenAI Response', style='filled', color='khaki')

dfd.node('P4', 'Process: Load Documents (Flask)', style='filled', color='lightblue')
dfd.node('P4a', 'Subprocess: Fetch Files from Directory', style='filled', color='deepskyblue')
dfd.node('P4b', 'Subprocess: Extract Text from Documents', style='filled', color='deepskyblue')
dfd.node('P4c', 'Subprocess: Store Extracted Text in ChromaDB', style='filled', color='deepskyblue')

dfd.node('P5', 'Process: Extract Text from Files', style='filled', color='violet')
dfd.node('P5a', 'Subprocess: Extract from PDF', style='filled', color='orchid')
dfd.node('P5b', 'Subprocess: Extract from PPT', style='filled', color='orchid')
dfd.node('P5c', 'Subprocess: Extract from Images', style='filled', color='orchid')

# Define the data stores (using cylinder shape and a different color)
dfd.node('D1', 'ChromaDB (Document Embeddings)', shape='cylinder', style='filled', color='lightgray')
dfd.node('D2', 'Document Files Directory', shape='cylinder', style='filled', color='lightgray')
dfd.node('D3', 'User Session Storage', shape='cylinder', style='filled', color='lightgray')

# Define external services (in box shape and light orange)
dfd.node('OpenAI', 'OpenAI API', shape='box', style='filled', color='lightgoldenrod')

# External User Interaction Flow (using colored arrows)
dfd.edge('User', 'Chainlit', label='User Query (Text)', color='blue')
dfd.edge('Chainlit', 'P1', label='Forward Query', color='green')

# Subprocesses of Handle Message
dfd.edge('P1', 'P1a', label='Validate User Input', color='yellowgreen')
dfd.edge('P1a', 'P1b', label='Input Validated', color='yellowgreen')
dfd.edge('P1b', 'P2', label='Prepare and Forward Query', color='yellowgreen')

# Subprocesses of Query ChromaDB
dfd.edge('P2', 'P2a', label='Create Embedding Function', color='lightcoral')
dfd.edge('P2a', 'P2b', label='Embedding Function Created', color='lightcoral')
dfd.edge('P2b', 'D1', label='Search for Relevant Context', color='lightcoral')
dfd.edge('D1', 'P2c', label='Return Contextual Data', color='lightcoral')
dfd.edge('P2c', 'P3', label='Forward Context and Query', color='lightcoral')

# Generate Response from OpenAI
dfd.edge('P3', 'P3a', label='Send Query to OpenAI', color='khaki')
dfd.edge('P3a', 'OpenAI', label='Call OpenAI API', color='lightgoldenrod')
dfd.edge('OpenAI', 'P3b', label='Receive OpenAI Response', color='lightgoldenrod')
dfd.edge('P3b', 'P3c', label='Format Response', color='khaki')
dfd.edge('P3c', 'P1', label='Send Response to Chainlit', color='khaki')
dfd.edge('P1', 'Chainlit', label='Send Response to User', color='green')
dfd.edge('Chainlit', 'User', label='Return Response', color='blue')

# Document Loading and Text Extraction
dfd.edge('Flask', 'P4', label='Trigger Document Loading', color='deepskyblue')
dfd.edge('P4', 'P4a', label='Fetch Files from Directory', color='deepskyblue')
dfd.edge('P4a', 'D2', label='Read Files', color='deepskyblue')
dfd.edge('D2', 'P4b', label='Return Files', color='deepskyblue')
dfd.edge('P4b', 'P4c', label='Extract Text', color='deepskyblue')
dfd.edge('P4c', 'D1', label='Store Extracted Text in ChromaDB', color='deepskyblue')

# Text Extraction from Specific File Types
dfd.edge('P4b', 'P5', label='Process Extracted Text', color='violet')
dfd.edge('P5', 'P5a', label='Extract from PDF', color='orchid')
dfd.edge('P5', 'P5b', label='Extract from PPT', color='orchid')
dfd.edge('P5', 'P5c', label='Extract from Images', color='orchid')

# User ID Handling (Flask)
dfd.edge('User', 'Flask', label='Send POST Request (User ID)', color='lightcoral')
dfd.edge('Flask', 'P4', label='Check or Fetch User ID', color='lightcoral')
dfd.edge('Flask', 'D3', label='Store User ID Temporarily', color='lightgray')
dfd.edge('D3', 'Flask', label='Fetch User ID if Needed', color='lightgray')
dfd.edge('Flask', 'User', label='Return Chainlit Chat URL', color='lightcoral')
dfd.edge('Flask', 'Chainlit', label='Send User ID to Chainlit', color='lightgreen')

# Save the diagram
dfd.render('OpenGPT_DFD_colored')

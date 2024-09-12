# AthleanX AI Coach

## Description
AthleanX AI Coach is an intelligent chatbot powered by the fitness expertise of Jeff Cavaliere. This AI assistant provides personalized fitness advice, workout recommendations, and answers to your health and exercise questions.

## Live Demo
Try out the AthleanX AI Coach here: [\[Streamlit App Link\]](https://fitness-coach.streamlit.app/)

## Project Overview

The AthleanX AI Coach is an advanced fitness assistant that leverages cutting-edge AI technologies and a rich dataset of fitness content. Here's a high-level overview of the project's architecture and methodology:

1. **Data Collection**: 
   - Scraped approximately 1,500 videos from the AthleanX YouTube channel.
   - Extracted comprehensive metadata from each video.

2. **Data Processing**:
   - Conducted exploratory data analysis to determine optimal chunk sizes for text processing.
   - Carefully selected an embedding model to minimize data loss while maximizing semantic understanding.

3. **Database Implementation**:
   - Utilized Pinecone, a vector database, to efficiently store and query video embeddings.
   - This enables rapid retrieval of relevant fitness information based on user queries.

4. **AI Model Integration**:
   - Implemented a Retrieval-Augmented Generation (RAG) pipeline for enhanced response generation.
   - Leveraged Google's Gemini 1.5 Pro as the Large Language Model (LLM) for generating accurate and context-aware responses.

5. **User Interface**:
   - Developed a user-friendly chatbot interface using Streamlit for seamless interaction with the AI coach.

This architecture allows the AthleanX AI Coach to provide personalized, accurate, and relevant fitness advice by combining the vast knowledge base of AthleanX videos with state-of-the-art AI language models.


### Data Processing Pipeline
1. Video Scraping → Metadata Extraction → Text Chunking → Embedding Generation → Vector Database Storage

## Technology Stack
- Python
- Streamlit
- Pinecone (for vector database)
- Sentence Transformers (for embeddings)
- LangChain with Google Generative AI

## Installation and Local Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-username/Fitness-Coach.git
   ```
2. Navigate to the project directory:
   ```
   cd Fitness-Coach
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables (API keys, etc.) in a `.env` file.
   ```
   GOOGLE_API_KEY="your_google_api_key"
   PINECONE_API_KEY="your_pinecone_api_key"
   ```
5. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage
Simply type your fitness-related questions into the chat interface. You can ask about:
- Specific exercises and their proper form
- Workout routines for different goals
- Nutrition advice
- Injury prevention and recovery
- And much more!

## Current Developments and Future Improvements

The AthleanX AI Coach is under active development, with several key areas of focus:

### Performance Optimization
- **Latency Reduction**: Efforts are underway to reduce the response time significantly from the current ``` 8-second``` average.
- **LLM Output Streaming**: Implementation of streaming for the LLM output is in progress. This will provide a more responsive user experience, allowing users to see responses as they're generated.

### Enhanced AI Capabilities
- **LangChain Integration**: Active learning and implementation of advanced LangChain techniques are ongoing. This work aims to build more sophisticated GenAI applications, enabling more nuanced understanding of fitness queries and more accurate, context-aware responses.


## Contributing
Contributions to improve the AthleanX AI Coach are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments
- Jeff Cavaliere and the AthleanX team for their invaluable fitness content

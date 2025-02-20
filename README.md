# LawBot

LawBot is an AI-powered chatbot designed to assist users with legal inquiries. It leverages NLP models to provide relevant legal information, document analysis, and case law references based on user queries.

## Features

- **AI-Powered Responses**: Uses natural language processing (NLP) to understand and respond to legal queries.
- **Legal Document Analysis**: Can process and extract insights from legal documents.
- **Case Law Reference**: Provides references to relevant case laws based on user inputs.
- **User-Friendly Interface**: A simple and intuitive interface for seamless interactions.
- **Scalable and Secure**: Designed to handle multiple queries efficiently with security measures in place.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React.js with Tailwind CSS
- **Database**: MongoDB
- **Machine Learning**: NLP models (e.g., BERT, GPT-based models)
- **Authentication**: JWT (JSON Web Tokens)

## Installation

### Prerequisites
- Python 3.8+
- Node.js & npm
- MongoDB

### Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/shubham8work/Lawbot.git
   cd Lawbot
   ```

2. **Setup Backend**
   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python app.py
   ```

3. **Setup Frontend**
   ```sh
   cd frontend
   npm install
   npm start
   ```

4. **Setup Database**
   - Ensure MongoDB is running locally or provide a cloud database connection.

## Usage
- Start the backend and frontend services.
- Navigate to `http://localhost:3000` in your browser.
- Enter legal queries and interact with LawBot.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve LawBot.

## License
This project is licensed under the MIT License.

## Contact
For queries, reach out to **[Shubham](https://github.com/shubham8work)**.


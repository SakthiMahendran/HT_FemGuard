from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory

class AIHandler:
    """
    Handles AI operations using ChatGroq and ConversationBufferMemory.
    """
    def __init__(self, model_name: str = "llama3-70b-8192", temperature: float = 0.7):
        """
        Initialize the ChatGroq model and conversation memory.
        
        :param model_name: Name of the Groq model to use.
        :param temperature: Sampling temperature for response generation.
        """
        self.chat_model = ChatGroq(model=model_name, temperature=temperature, api_key="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")
        self.memory = ConversationBufferMemory()

    def process_prompt(self, prompt: str) -> str:
        """
        Process a user prompt and generate a response using ChatGroq.
        
        :param prompt: The user's input prompt.
        :return: The AI-generated response.
        """
        # Add user message to memory
        self.memory.chat_memory.add_user_message(prompt)

        # Prepare messages for the chat model
        messages = self.memory.chat_memory.messages

        # Generate AI response
        response = self.chat_model.invoke(messages)

        # Add AI response to memory
        self.memory.chat_memory.add_ai_message(response.content)

        return response.content


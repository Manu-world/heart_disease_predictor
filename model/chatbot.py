from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,HumanMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
import os 
from dotenv import load_dotenv

load_dotenv()


model =  ChatOpenAI(
        api_key= os.getenv("OPENAI-API_KEY"),
        temperature=0.2,
        model='gpt-3.5-turbo-1106'
    )

prompt = ChatPromptTemplate.from_messages(
    [
    
             (
            "system",
            """You are a cardiologist, provide accurate answers based on a patient's vitals and heart disease status provided as context. if they don't ask any question just say "Hi"
            context:  {context}  
            make your answers as short as posible. Don't say based on the context provided, just be straightforward with your answers. Also don't ask them to go and see a health expert""",
        ),
            
        MessagesPlaceholder(variable_name="chathistory"),
        HumanMessagePromptTemplate.from_template(
            "{input}"
        ),
    ]
)
# prompt = ChatPromptTemplate.from_messages(
#     [
    
#              (
#             "system",
#             """You are a ceo assistant.you give project summary to project name asked at the end, using the template below. 
#             ```project summary template:  {context}  ```
#             """,
#         ),
            
#         MessagesPlaceholder(variable_name="chathistory"),
#         HumanMessagePromptTemplate.from_template(
#             "{input}"
#         ),
#     ]
# )





chain = prompt | model


conversation = RunnableWithMessageHistory(
    chain,
    lambda session_id: MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=os.getenv("connection_string"),
        database_name=os.getenv("db_name"),
        collection_name=os.getenv("collection"), ),
    input_messages_key="input",
    history_messages_key="chathistory",
)


def get_response(context, message, session_id):
    response = conversation.invoke(
        {"context": context, "input": message},
        config={"configurable": {"session_id": session_id}},
    )

    return response.content

# context = "prediction: you have heart disease"

# print(get_response(context=context, message="what is my status", session_id=345))


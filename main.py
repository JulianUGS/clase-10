from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory, ChatMessageHistory, ConversationBufferWindowMemory
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools import YouTubeSearchTool
from langchain_core.tools import tool

#cargamos variables de entorno
load_dotenv()

#Definimos funcion de embeddings
embeddings_function = OpenAIEmbeddings()

#Instanciamos el modelo
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature= 0    
)

#Cargamos la db
db = Chroma(
    persist_directory = 'docs/Chroma',
    embedding_function = embeddings_function
)

retriever = db.as_retriever()

#Crear memoria para agente

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=4,
    return_messages=True,
    chat_memory=ChatMessageHistory()
)



#Tool1_Busqueda
busqueda_Hollow = create_retriever_tool(
    retriever=retriever,
    name='busqueda_hallownest',
    description="busca en una lista de hipervinculos informacion sobre Hollow Knight, accede al hipervinculo mas cercano a la query para obtener mas informacion sobre la busqueda, la query debe de estar en ingles"
)


#Tool2 videos
youtube_search_tool = YouTubeSearchTool()

@tool
def busqueda_videos_youtube(query: str):
    """busca videos en youtube sobre el tema especificado"""
    search_results = youtube_search_tool.run(query)
    return str(search_results)

tools = [busqueda_Hollow, busqueda_videos_youtube]

# Definir Prompt
prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.messages[0].prompt.template = 'eres un cazador serio e imponente llamado Cantharis, tu deber es ayudar al usuario a travez de informacion sobre Hollow Knight, debes actuar serio y superior en todo momento para que el usuario crea que eres un cazador imponente, no tienes que nombrar tu personalidad.'

#Creamos el agente
agent = create_openai_tools_agent(
    llm= llm,
    tools= tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

def chatbot(query:str, chat_history):
    response = agent_executor.invoke({'input': f'{query}', "chat_history":chat_history })['output']
    return response

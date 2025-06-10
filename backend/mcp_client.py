from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

server_params = StdioServerParameters(
    command="python",
    args=["mcp_pdf_server.py"],
)

#Class to handle mcp and agent interaction
class Chat:
    def __init__(self):
        self.messages = []
        self.system_prompt: str = """You are an AI agent that is under development"""

    async def process_query(self, session: ClientSession, query: str):
        self.messages.append({"type": "human", "content": query})

        #Load mcp tools and create AI agent
        tools = await load_mcp_tools(session)
        agent = create_react_agent(
            model="openai:o4-mini-2025-04-16", tools=tools, prompt=self.system_prompt
        )
        res = await agent.ainvoke({"messages": self.messages})

        outputmsg = []

        for key in res.keys():
            for msg in res[key]:
                if msg.type == "ai" and msg.content != "":
                    print("AI response\n", msg.content)
                    outputmsg.append(msg.content)
                # Debug prints
                elif msg.type == "tool":
                    print("Used tool\n", msg.name)
                elif msg.type == "human":
                    print("Human prompt\n", msg.content)
        return outputmsg

    #Testing function to run locally
    async def chat_loop(self, session: ClientSession):
        while True:
            query = input("\nQuery: ").strip()
            # self.messages.append(query)
            await self.process_query(session, query)
            
    #Testing function to run locally
    async def run(self):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                await self.chat_loop(session)


if __name__ == "__main__":
    chat = Chat()
    asyncio.run(chat.run())
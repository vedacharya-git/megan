from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

from modules.llm_ollama import LLMManager
from modules.logger import LoggerManager

# State definition
class ConversationState(BaseModel):
    input_text: str
    output_text: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

class MEGANGraph:
    def __init__(self):
        self.llm = LLMManager(enable_log=True)
        self.logger = LoggerManager().get_logger("MEGANGraph", master_log=True)
        self.graph = self._build_graph()

    def echo_node(self, state: ConversationState) -> ConversationState:
        self.logger.info(f"Processing input: {state.input_text}")
        
        response = self.llm.infer(state.input_text)
        
        state.output_text = response if response else "Sorry, I couldn't process that."
        self.logger.info(f"Generated response: {state.output_text}")
        
        return state

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ConversationState)
        
        graph.add_node("echo", self.echo_node)
        
        graph.set_entry_point("echo")
        graph.set_finish_point("echo")
        
        return graph.compile()

    def process_input(self, user_input: str) -> ConversationState:
        initial_state = ConversationState(input_text=user_input)
        
        final_state = self.graph.invoke(initial_state)
        
        return final_state

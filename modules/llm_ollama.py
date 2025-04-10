from langchain_ollama import OllamaLLM
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Union, Optional
from datetime import datetime

from modules.logger import LoggerManager

LLM_MODEL = "mistral-nemo"
MODEL_TEMP = 0.6
MODEL_STREAM = True
DEFAULT_LOGGING = False

class LLMManager:
    def __init__(
        self,
        model_name: str = LLM_MODEL,
        temperature: float = MODEL_TEMP,
        streaming: bool = MODEL_STREAM,
        enable_log: bool = DEFAULT_LOGGING
    ):
        self.logger = LoggerManager().get_logger("LLM", master_log=True)
        self.model_name = model_name
        self.temperature = temperature
        self.streaming = streaming
        self.log = enable_log
        self.llm = self._load_model()

    def _log(self, level: str, message: str):
        """
        Utility function to handle logging.
        
        Can be set via DEFAULT_LOGGING constant
        """
        if not self.log:
            return
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_msg = f"[{self.model_name.upper()}][{timestamp}] {message}"
        getattr(self.logger, level)(full_msg)

    def _load_model(self) -> OllamaLLM:
        try:
            self._log("debug", f"Initializing model with temperature={self.temperature}, streaming={self.streaming}")
            
            callbacks = CallbackManager([StreamingStdOutCallbackHandler()]) if self.streaming else None
            
            llm = OllamaLLM(
                model=self.model_name,
                temperature=self.temperature,
                callbacks=callbacks,
                verbose=True
            )

            self._log("info", f"{self.model_name} loaded successfully.")
            return llm

        except Exception as e:
            self._log("error", f"Failed to load {self.model_name}: {e}")
            raise e

    def infer(self, prompt: str, log_prompt: Optional[bool] = None) -> Union[str, None]:
        local_log = self.log if log_prompt is None else log_prompt

        if local_log:
            self._log("debug", f"Prompt sent: {prompt}")
        try:
            print("MEGAN: ", end="")
            response = self.llm.invoke(prompt)
            print()
            if local_log:
                self._log("debug", f"Response received")
            return response
        except Exception as e:
            self._log("error", f"Inference error: {e}")
            return None

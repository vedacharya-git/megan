import sys
from modules.langgraph_node import MEGANGraph
from modules.logger import LoggerManager

LoggerManager.PRINT_LOG = False

def main():
    logger = LoggerManager().get_logger("MAIN", master_log=True)
    logger.info("Starting MEGAN main loop...")
    
    try:
        megan = MEGANGraph()
        logger.info("MEGAN initialized with LangGraph")
        
        while True:
            user_input = input("\nUser:  ").strip()

            if user_input.lower() in {"exit", "quit"}:
                logger.info("User exited MEGAN")
                print("Exiting...")
                break

            if not user_input:
                continue

            logger.debug(f"Received input: {user_input}")
            
            # Process through graph - response will be streamed by LLMManager
            _ = megan.process_input(user_input)

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting MEGAN.")
        logger.warning("User terminated the loop with Ctrl+C.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("MEGAN terminated.")

if __name__ == "__main__":
    main()

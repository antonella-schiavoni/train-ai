import agenta as ag
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class AgentaService:
    """Agenta service. Used to fetch prompts from Agenta."""

    def __init__(self):
        logger.info("Initializing AgentaService")
        self._prompt = None

    async def get_prompt(self):
        """Get prompt from Agenta."""
        if self._prompt is None:
            logger.info("Fetching prompt from Agenta")
            try:
                config = ag.ConfigManager.get_from_registry(
                    app_slug="workout", environment_slug="development"
                )

                messages = config["prompt"]["messages"]
                logger.info("Successfully fetched prompt from Agenta")
                logger.debug(f"System prompt: {messages[0]['content']}")
                logger.debug(f"User prompt: {messages[1]['content']}")

                # Store the raw messages for chat API
                self._prompt = messages
                logger.debug(f"Stored messages: {self._prompt}")
            except Exception as e:
                logger.error(f"Failed to fetch prompt from Agenta: {e}")
                raise

        return self._prompt

    async def get_messages(self):
        """Get structured messages for chat API."""
        messages = await self.get_prompt()

        # Convert to proper chat format
        chat_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                chat_messages.append({"role": "system", "content": msg["content"]})
            elif msg.get("role") == "user":
                chat_messages.append({"role": "user", "content": msg["content"]})

        logger.debug(f"Chat messages: {chat_messages}")
        return chat_messages


agenta_service = AgentaService()

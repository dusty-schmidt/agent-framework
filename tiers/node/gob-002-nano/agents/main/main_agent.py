"""
Main chat agent that delegates tasks to specialist agents if required.
"""

import logging
from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability

logger = logging.getLogger('MainAgent')

class MainAgent(BaseAgent):
    """
    Main agent responsible for general interactions and task delegation.
    """

    def __init__(self):
        capabilities = [
            AgentCapability(
                name="General Interaction",
                description="Handles general user queries and tasks",
                keywords=["general", "chat", "question", "answer"],
                confidence_threshold=0.6
            )
        ]
        
        system_prompt = "You are the main chat agent, handling general queries and coordinating specialized tasks."

        super().__init__(
            agent_id="main",
            name="Main Agent",
            capabilities=capabilities,
            system_prompt=system_prompt
        )

    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """
        Determine if the main agent can handle the request or if it should delegate
        """
        if self.can_handle(request) > 0.7:
            return AgentResponse(
                request_id=request.id,
                content="This is a general response from the Main Agent.",
                agent_id=self.agent_id,
                confidence=0.7,
                reasoning="Processed as a general task."
            )
        else:
            return AgentResponse(
                request_id=request.id,
                content="I will delegate this to a specialized agent.",
                agent_id=self.agent_id,
                confidence=0.5,
                reasoning="Determined to be better suited for a specialized agent."
            )

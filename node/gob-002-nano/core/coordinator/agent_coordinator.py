"""
Agent Coordinator for routing requests to specialized agents with hierarchical prompts.
"""

import asyncio
import logging
from typing import List, Optional
from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability

logger = logging.getLogger('AgentCoordinator')

class AgentCoordinator:
    """
    Main Coordinator for handling user requests and delegating tasks to specific agents.
    Implements hierarchical context and prompt management.
    """

    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.priority_queue = asyncio.PriorityQueue()
        self.response_history = []

    async def route_request(self, user_input: str, context: Optional[str] = None) -> AgentResponse:
        logger.info(f"Routing request: {user_input[:50]}...")
        request = AgentRequest(id=None, user_input=user_input, context={}, priority=1)

        # Evaluate agents capable of handling the request
        agent_ranking = []
        for agent in self.agents:
            confidence = agent.can_handle(request)
            if confidence > 0.1:
                logger.debug(f"Agent {agent.name} can handle with confidence {confidence:.2f}")
                agent_ranking.append((confidence, agent))

        # Sort agents by their confidence in descending order
        agent_ranking.sort(reverse=True, key=lambda x: x[0])

        # Select the highest confidence agent for the task
        for confidence, agent in agent_ranking:
            hierarchical_prompt = agent.get_hierarchical_prompt(request, base_context=context)
            try:
                response = await agent.process_request(request)
                logger.info(f"Agent {agent.name} responded with confidence {confidence:.2f}")
                self.response_history.append(response)
                return response
            except Exception as e:
                logger.error(f"Agent {agent.name} failed to process request: {e}")

        return AgentResponse(
            request_id=request.id,
            content="I'm sorry, I couldn't process your request.",
            agent_id="Coordinator",
            confidence=0.0,
            reasoning="No agent was able to handle the request successfully.",
            success=False
        )

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    class ExampleAgent(BaseAgent):
        async def process_request(self, request: AgentRequest) -> AgentResponse:
            return AgentResponse(
                request_id=request.id,
                content="This is a response from ExampleAgent.",
                agent_id=self.agent_id,
                confidence=0.9,
                reasoning="Processed with basic logic."
            )

    example_agent = ExampleAgent(
        agent_id="example",
        name="Example Agent",
        capabilities=[AgentCapability(
            name="Example Task",
            description="Handles example tasks",
            keywords=["example", "sample", "test"]
        )],
        system_prompt="You are an example agent focused on sample tasks."
    )
    
    coordinator = AgentCoordinator(agents=[example_agent])
    asyncio.run(coordinator.route_request("This is an example request"))


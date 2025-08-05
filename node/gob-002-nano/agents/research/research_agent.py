"""
Research Agent - Specialized for information gathering, analysis, and research tasks
"""

import logging
import asyncio
from typing import Dict, List
from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability
from agents.simple_gemini_bot import GeminiProvider

logger = logging.getLogger('ResearchAgent')

class ResearchAgent(BaseAgent):
    """
    Specialized agent for research and information gathering tasks including:
    - Web research and fact-checking
    - Data analysis and interpretation
    - Literature reviews and summarization
    - Comparative analysis
    - Information synthesis
    """
    
    def __init__(self, gemini_provider: GeminiProvider):
        capabilities = [
            AgentCapability(
                name="Web Research",
                description="Conduct web research and gather information",
                keywords=["research", "find", "search", "investigate", "look up", "information"],
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="Data Analysis",
                description="Analyze and interpret data and trends",
                keywords=["analyze", "analysis", "data", "trends", "statistics", "interpret"],
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="Fact Checking",
                description="Verify facts and check information accuracy",
                keywords=["verify", "fact check", "confirm", "validate", "accuracy", "true"],
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="Summarization",
                description="Summarize complex information and documents",
                keywords=["summarize", "summary", "overview", "brief", "condensed", "key points"],
                confidence_threshold=0.7
            ),
            AgentCapability(
                name="Comparative Analysis",
                description="Compare and contrast different options or concepts",
                keywords=["compare", "contrast", "versus", "vs", "differences", "similarities"],
                confidence_threshold=0.7
            ),
            AgentCapability(
                name="Information Synthesis",
                description="Combine information from multiple sources",
                keywords=["synthesize", "combine", "integrate", "comprehensive", "holistic"],
                confidence_threshold=0.7
            )
        ]
        
        system_prompt = """You are a Research Agent specializing in information gathering, analysis, and synthesis.

Your core competencies include:
- Conducting thorough research on any topic
- Analyzing data and identifying patterns or trends
- Fact-checking and verifying information accuracy
- Summarizing complex information into digestible insights
- Performing comparative analysis between options
- Synthesizing information from multiple sources into comprehensive reports

Research Methodology:
- Always cite sources when making factual claims
- Distinguish between facts, opinions, and speculation
- Provide multiple perspectives on controversial topics
- Identify potential biases in sources
- Present information in a structured, logical format
- Include limitations and caveats where appropriate

Quality Standards:
- Prioritize authoritative and recent sources
- Cross-reference information when possible
- Acknowledge when information is incomplete or uncertain
- Provide actionable insights and recommendations
- Structure responses for maximum clarity and usefulness

Be thorough, objective, and analytical in all research tasks."""
        
        super().__init__(
            agent_id="research",
            name="Research Agent",
            capabilities=capabilities,
            system_prompt=system_prompt,
            memory_namespace="research"
        )
        
        self.gemini_provider = gemini_provider
        
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process research-related requests"""
        
        try:
            # Build hierarchical prompt with research context
            full_prompt = self.get_hierarchical_prompt(request)
            
            # Add research-specific instructions
            research_prompt = f"""
            {full_prompt}
            
            RESEARCH INSTRUCTIONS:
            - Provide well-structured, comprehensive information
            - Include relevant details and context
            - Cite sources or indicate when information should be verified
            - Organize information logically with clear sections
            - Highlight key findings and insights
            - Include limitations or areas for further investigation
            """
            
            # Get response from Gemini with research-focused context
            response_content = await self.gemini_provider.chat(research_prompt, [])
            
            # Determine confidence based on request type
            confidence = self._calculate_confidence(request)
            
            # Update metrics
            self.update_metrics(success=True, confidence=confidence)
            
            return AgentResponse(
                request_id=request.id,
                content=response_content,
                agent_id=self.agent_id,
                confidence=confidence,
                reasoning=f"Processed research request using specialized methodology",
                metadata={
                    'research_type': self._classify_research_task(request.user_input),
                    'information_depth': self._estimate_depth(request.user_input),
                    'sources_needed': self._estimate_sources_needed(request.user_input)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Research agent processing failed: {e}")
            self.update_metrics(success=False, confidence=0.1)
            
            return AgentResponse(
                request_id=request.id,
                content=f"I encountered an error processing your research request: {str(e)}",
                agent_id=self.agent_id,
                confidence=0.1,
                reasoning=f"Error during processing: {str(e)}",
                success=False
            )
    
    def _calculate_confidence(self, request: AgentRequest) -> float:
        """Calculate confidence based on request characteristics"""
        base_confidence = self.can_handle(request)
        
        # Boost confidence for specific research keywords
        high_confidence_keywords = [
            'study', 'report', 'analysis', 'findings', 'evidence',
            'academic', 'scientific', 'peer-reviewed', 'statistics',
            'market research', 'trend analysis', 'literature review'
        ]
        
        user_input_lower = request.user_input.lower()
        keyword_matches = sum(1 for keyword in high_confidence_keywords 
                             if keyword in user_input_lower)
        
        # Increase confidence based on keyword matches
        confidence_boost = min(keyword_matches * 0.1, 0.3)
        
        return min(base_confidence + confidence_boost, 1.0)
    
    def _classify_research_task(self, user_input: str) -> str:
        """Classify the type of research task"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['find', 'search', 'look up', 'information about']):
            return "information_gathering"
        elif any(word in user_input_lower for word in ['analyze', 'analysis', 'examine']):
            return "data_analysis"
        elif any(word in user_input_lower for word in ['compare', 'versus', 'vs', 'contrast']):
            return "comparative_analysis"
        elif any(word in user_input_lower for word in ['summarize', 'summary', 'overview']):
            return "summarization"
        elif any(word in user_input_lower for word in ['verify', 'fact check', 'confirm']):
            return "fact_checking"
        elif any(word in user_input_lower for word in ['synthesize', 'comprehensive', 'report']):
            return "synthesis"
        else:
            return "general_research"
    
    def _estimate_depth(self, user_input: str) -> str:
        """Estimate the depth of research required"""
        depth_indicators = {
            'surface': ['quick', 'brief', 'overview', 'basic', 'simple'],
            'moderate': ['detailed', 'thorough', 'comprehensive', 'in-depth'],
            'deep': ['exhaustive', 'complete', 'academic', 'scholarly', 'peer-reviewed']
        }
        
        user_input_lower = user_input.lower()
        
        for depth, indicators in depth_indicators.items():
            if any(indicator in user_input_lower for indicator in indicators):
                return depth
        
        # Default to moderate depth
        return "moderate"
    
    def _estimate_sources_needed(self, user_input: str) -> int:
        """Estimate the number of sources needed for the research"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['quick', 'brief', 'simple']):
            return 1  # Few sources needed
        elif any(word in user_input_lower for word in ['comprehensive', 'thorough', 'detailed']):
            return 5  # Multiple sources needed
        elif any(word in user_input_lower for word in ['academic', 'scholarly', 'exhaustive']):
            return 10  # Many sources needed
        else:
            return 3  # Moderate number of sources
    
    async def conduct_structured_research(self, request: AgentRequest) -> AgentResponse:
        """
        Conduct structured research following a systematic methodology.
        This implements advanced research capabilities.
        """
        
        research_plan = await self._create_research_plan(request)
        
        # Execute research phases
        phases = [
            "Initial Information Gathering",
            "Source Verification",
            "Analysis and Synthesis", 
            "Quality Review"
        ]
        
        research_results = {}
        
        for phase in phases:
            self.logger.info(f"Executing research phase: {phase}")
            phase_result = await self._execute_research_phase(phase, request, research_plan)
            research_results[phase] = phase_result
        
        # Compile final research report
        final_report = await self._compile_research_report(research_results, request)
        
        return AgentResponse(
            request_id=request.id,
            content=final_report,
            agent_id=self.agent_id,
            confidence=0.9,
            reasoning="Completed structured research using systematic methodology",
            metadata={
                'research_method': 'structured',
                'phases_completed': len(phases),
                'research_plan': research_plan
            }
        )
    
    async def _create_research_plan(self, request: AgentRequest) -> Dict:
        """Create a systematic research plan"""
        
        plan_prompt = f"""
        Create a research plan for this request: "{request.user_input}"
        
        Include:
        1. Key research questions to answer
        2. Types of sources to consult
        3. Information gaps to address
        4. Success criteria for the research
        
        Format as a structured plan.
        """
        
        plan_response = await self.gemini_provider.chat(plan_prompt, [])
        
        return {
            'query': request.user_input,
            'research_questions': self._extract_research_questions(plan_response),
            'source_types': self._extract_source_types(plan_response),
            'success_criteria': self._extract_success_criteria(plan_response)
        }
    
    def _extract_research_questions(self, plan_text: str) -> List[str]:
        """Extract research questions from the plan"""
        # Simplified extraction - in production, this would be more sophisticated
        lines = plan_text.split('\n')
        questions = []
        for line in lines:
            if '?' in line and any(word in line.lower() for word in ['what', 'how', 'why', 'when', 'where']):
                questions.append(line.strip())
        return questions[:5]  # Limit to 5 questions
    
    def _extract_source_types(self, plan_text: str) -> List[str]:
        """Extract source types from the plan"""
        # Simplified extraction
        source_types = ['academic papers', 'news articles', 'official reports', 'expert opinions']
        return source_types
    
    def _extract_success_criteria(self, plan_text: str) -> List[str]:
        """Extract success criteria from the plan"""
        # Simplified extraction
        criteria = ['comprehensive coverage', 'recent information', 'multiple perspectives', 'actionable insights']
        return criteria
    
    async def _execute_research_phase(self, phase: str, request: AgentRequest, plan: Dict) -> str:
        """Execute a specific phase of the research process"""
        
        phase_prompt = f"""
        Execute research phase: {phase}
        
        Original request: {request.user_input}
        Research questions: {', '.join(plan['research_questions'])}
        
        For this phase, focus on: {self._get_phase_focus(phase)}
        
        Provide structured results for this phase.
        """
        
        return await self.gemini_provider.chat(phase_prompt, [])
    
    def _get_phase_focus(self, phase: str) -> str:
        """Get the focus area for each research phase"""
        phase_focus = {
            "Initial Information Gathering": "collecting basic facts and overview information",
            "Source Verification": "checking accuracy and credibility of information",
            "Analysis and Synthesis": "analyzing patterns and synthesizing insights",
            "Quality Review": "ensuring completeness and identifying gaps"
        }
        return phase_focus.get(phase, "general research activities")
    
    async def _compile_research_report(self, results: Dict, request: AgentRequest) -> str:
        """Compile the final research report"""
        
        report_sections = []
        
        report_sections.append("# RESEARCH REPORT")
        report_sections.append(f"**Query:** {request.user_input}")
        report_sections.append(f"**Completed:** {len(results)} research phases")
        report_sections.append("")
        
        for phase, result in results.items():
            report_sections.append(f"## {phase}")
            report_sections.append(result)
            report_sections.append("")
        
        report_sections.append("## CONCLUSION")
        report_sections.append("Research completed using systematic methodology with multiple verification phases.")
        
        return "\n".join(report_sections)

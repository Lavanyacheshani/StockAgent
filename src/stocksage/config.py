PORTFOLIO_MANAGER_LLM = "openai/gpt-4o"
FACT_AGENT_LLM = "openai/gpt-4o-mini"
SENTIMENT_AGENT_LLM = "openai/gpt-4o-mini"
ANALYSIS_AGENT_LLM = "openai/gpt-4o-mini"
SYNTHESIZER_AGENT_LLM = "openai/gpt-4o-mini"
JUSTIFICATION_AGENT_LLM = "openai/gpt-4o-mini"
OPTIMIZATION_AGENT_LLM = "openai/gpt-4o-mini"
THESIS_AGENT_LLM = "openai/gpt-4o"
RECOMMENDATION_AGENT_LLM = "openai/gpt-4o-mini"
CHAT_LLM = "openai/gpt-4o"
FUNCTION_CALLING_LLM = "openai/gpt-4o-mini"

AGENT_META_CONFIG = {"timeout": 300, "retry": True}
VERBOSE = True
TASK_DELEGATION_CONFIG = {
    "use_task_output": True,
    "stringify_task_and_context": True,
    "parallel_tasks_limit": 10,
    "error_handling": "continue_on_error",
}
MEMORY = False  # Disabled due to Windows path length limitations
CACHE = True

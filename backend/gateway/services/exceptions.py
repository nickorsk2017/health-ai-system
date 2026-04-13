class AgentConnectionError(Exception):
    """Raised when an MCP agent is unreachable or returns an unexpected response."""


class NoDataFoundError(Exception):
    """Raised when an agent returns an empty result for a valid request."""

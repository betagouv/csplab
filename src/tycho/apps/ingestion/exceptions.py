"""Infrastructure exceptions for ingestion module."""

from infrastructure.exceptions import InfrastructureError


class InvalidLoadOperationError(InfrastructureError):
    """Invalid load operation type provided."""

    def __init__(self, operation_type: str):
        """Initialize with operation type."""
        super().__init__(f"Invalid load operation type: {operation_type}")


class MissingOperationParameterError(InfrastructureError):
    """Required parameter missing for operation."""

    def __init__(self, parameter: str, operation: str):
        """Initialize with parameter and operation."""
        super().__init__(
            f"Parameter '{parameter}' is required for {operation} operation"
        )


class LoadStrategyError(InfrastructureError):
    """Strategy execution failed."""

    def __init__(self, strategy_name: str, message: str):
        """Initialize with strategy name and error message."""
        super().__init__(f"Strategy {strategy_name} failed: {message}")

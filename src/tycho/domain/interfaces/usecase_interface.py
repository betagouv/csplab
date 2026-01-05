"""Use case interface definitions."""

from typing import Generic, Protocol, TypeVar

# generic types for query or commands inputs and DTOs output
InputType_contra = TypeVar("InputType_contra", contravariant=True)
OutputType_co = TypeVar("OutputType_co", covariant=True)


class IUseCase(Protocol, Generic[InputType_contra, OutputType_co]):
    """Interface for use cases."""

    def execute(self, input_data: InputType_contra) -> OutputType_co:
        """Execute the use case with input data."""
        ...

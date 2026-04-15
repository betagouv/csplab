from typing import Generic, Protocol, TypeVar

InputType_contra = TypeVar("InputType_contra", contravariant=True)
OutputType_co = TypeVar("OutputType_co", covariant=True)


class IAsyncUseCase(Protocol, Generic[InputType_contra, OutputType_co]):
    async def execute(self, input_data: InputType_contra) -> OutputType_co: ...

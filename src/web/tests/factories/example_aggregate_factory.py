from tests.domain.example_aggregate import ExampleAggregate


class ExampleAggregateFactory:
    @staticmethod
    def build(name: str = "Example") -> ExampleAggregate:
        return ExampleAggregate.build(name=name)

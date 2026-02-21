from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        ...

    def validate(self, data: Any) -> bool:
        ...

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            for num in data:
                num.is_integer
        except (AttributeError, TypeError):
            print("Not list of numbers")
            return False
        print("Validation: Numeric data verified")
        return True

    def process(self, data: Any) -> str:
        return (
            f"Processed {len(data)} numeric values "
            f", sum={sum(data)}, avg={sum(data) / len(data)}"
        )


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            data.capitalize()
        except (AttributeError, TypeError):
            print("Not a string")
            return False
        print("Validation: Text data verified")
        return True

    def process(self, data: Any) -> str:
        return f"Processed text: {len(data)}, {len(data.split())} words"


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            if data.find("ERROR") > -1 or data.find("INFO") > -1:
                print("Validation: Log entry verified")
                return True
        except (AttributeError, TypeError):
            print("Not a log entry")
            return False
        return False

    def process(self, data: Any) -> str:
        output: str = ""
        if data.find("ERROR") > -1:
            output = "[ALERT] ERROR level detected: " + data[7:]
        elif data.find("INFO") > -1:
            output = "[INFO] INFO level detected: " + data[6:]
        return output

    def format_output(self, result: str) -> str:
        return "Overiden log:" + result


def main() -> None:
    print("Initializing Numeric Processor...")
    print("Processing data: [1, 2, 3, 4, 5]")
    lst: list[int] = [1, 2, 3, 4, 5]
    processor = NumericProcessor()
    if processor.validate(data=lst):
        print(processor.process(data=lst))
    # Just to check
    print("\nError check:")
    processor.validate("Hi!")

    print("")
    print("Initializing Text Processor...")
    print('Processing data: "Hello Nexus World"')
    processor = TextProcessor()
    if processor.validate("Hello Nexus World"):
        print(processor.process("Hello Nexus World"))
    # Just to check
    print("\nError check:")
    processor.validate(45)

    print("")
    print("Initializing Log Processor...")
    print('Processing data: "ERROR: Connection timeout"')
    processor = LogProcessor()
    if processor.validate("ERROR: Connection timeout"):
        print(processor.process("ERROR: Connection timeout"))
    # Just to check
    print("\nError check:")
    processor.validate(45)

    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    polimorph: list[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]

    print("Result 1: ", polimorph[0].process([6, 0, 0]))
    print("Result 2: ", polimorph[1].process("ABCDEF ABCDE"))
    print("Result 3: ", polimorph[2].process("INFO: System ready"))

    print("\n=== OVerride Demo ===")
    print("Result 1: ", polimorph[0].format_output("For numbers"))
    print("Result 2: ", polimorph[1].format_output("For texts"))
    print("Result 3: ", polimorph[2].format_output("For Log"))


if __name__ == "__main__":
    main()

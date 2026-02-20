from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.processed_count: int = 0
        self.stream_id: str = stream_id
        self.type: str = ""

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, str | int | float]:
        return {
            "stream_id": self.stream_id,
            "processed_count": self.processed_count
        }


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Environmental Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            average = sum(data_batch) / len(data_batch)
        except (TypeError, ZeroDivisionError):
            return f"[{self.stream_id}] Invalid sensor data"

        self.processed_count += len(data_batch)

        return (
            f"[{self.stream_id}] "
            f"{len(data_batch)} readings processed, avg: {average:.2f}"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:

        if criteria is None:
            return data_batch
        if criteria == "high":
            return [data for data in data_batch if data > 30]
        if criteria == "standard":
            return [data for data in data_batch if data <= 30]
        return data_batch


class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Transaction Stream"

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            total = sum(data_batch)
        except TypeError:
            return f"[{self.stream_id}] Invalid transaction data"

        self.processed_count += len(data_batch)

        return (
            f"[{self.stream_id}] "
            f"{len(data_batch)} operations processed, net flow: {total}"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:

        if criteria is None:
            return data_batch
        if criteria == "positive":
            return [data for data in data_batch if data >= 0]
        if criteria == "negative":
            return [data for data in data_batch if data < 0]
        return data_batch


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Event Stream"

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            total = len(data_batch)
            error_count = sum(
                1 for event in data_batch
                if isinstance(event, str) and "error" in event
            )
        except TypeError:
            return f"[{self.stream_id}] Invalid event data"

        self.processed_count += total

        return (
            f"[{self.stream_id}] "
            f"{total} events processed, {error_count} error(s)"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:

        if criteria is None:
            return data_batch
        if criteria == "error":
            return [data for data in data_batch if "error" in data]
        if criteria == "info":
            return [data for data in data_batch if "error" not in data]
        return data_batch


class StreamProcessor:

    def __init__(self, streams: List[DataStream]) -> None:
        self.streams: List[DataStream] = streams

    def process_streams(
        self,
        data_map: Dict[str, List[Any]]) -> None:

        for stream in self.streams:
            batch = data_map.get(stream.stream_id, [])
            try:
                result = stream.process_batch(batch)
                print(result)
            except Exception as e:
                print(f"Processing error in {stream.stream_id}: {e}")

    def filter_streams(
        self,
        data_map: Dict[str, List[Any]],
        criteria_map: Dict[str, str]) -> None:
        for stream in self.streams:
            batch = data_map.get(stream.stream_id, [])
            criteria = criteria_map.get(stream.stream_id)
            try:
                filtered = stream.filter_data(batch, criteria)
                print(
                    f"{stream.stream_id}: "
                    f"{len(filtered)} filtered item(s)"
                )
            except Exception as e:
                print(f"Filtering error in {stream.stream_id}: {e}")


def main() -> None:

    data_streams: List[DataStream] = [
        SensorStream("SENSOR_001"),
        TransactionStream("TRANS_001"),
        EventStream("EVENT_001")
    ]

    data_lists: Dict[str, List[Any]] = {
        "SENSOR_001": [22.5, 50, 21.8],
        "TRANS_001": [100, 150, -75],
        "EVENT_001": ["login", "error", "logout"]
    }

    processor = StreamProcessor(data_streams)

    print("=== Batch Processing ===")
    processor.process_streams(data_lists)

    print("\n=== Filtering ===")

    filter_criteria: Dict[str, str] = {
        "SENSOR_001": "high",
        "TRANS_001": "negative",
        "EVENT_001": "error"
    }

    processor.filter_streams(data_lists, filter_criteria)

    print("\n=== Stream Statistics ===")
    for stream in data_streams:
        print(stream.get_stats())


if __name__ == "__main__":
    main()
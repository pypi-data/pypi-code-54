from mlagents_envs.side_channel import SideChannel, IncomingMessage
import uuid
from typing import Dict, Tuple
from enum import Enum


# Determines the behavior of how multiple stats within the same summary period are combined.
class StatsAggregationMethod(Enum):
    # Values within the summary period are averaged before reporting.
    AVERAGE = 0

    # Only the most recent value is reported.
    MOST_RECENT = 1


class StatsSideChannel(SideChannel):
    """
    Side channel that receives (string, float) pairs from the environment, so that they can eventually
    be passed to a StatsReporter.
    """

    def __init__(self) -> None:
        # >>> uuid.uuid5(uuid.NAMESPACE_URL, "com.unity.ml-agents/StatsSideChannel")
        # UUID('a1d8f7b7-cec8-50f9-b78b-d3e165a78520')
        super().__init__(uuid.UUID("a1d8f7b7-cec8-50f9-b78b-d3e165a78520"))

        self.stats: Dict[str, Tuple[float, StatsAggregationMethod]] = {}

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Receive the message from the environment, and save it for later retrieval.
        :param msg:
        :return:
        """
        key = msg.read_string()
        val = msg.read_float32()
        agg_type = StatsAggregationMethod(msg.read_int32())

        self.stats[key] = (val, agg_type)

    def get_and_reset_stats(self) -> Dict[str, Tuple[float, StatsAggregationMethod]]:
        """
        Returns the current stats, and resets the internal storage of the stats.
        :return:
        """
        s = self.stats
        self.stats = {}
        return s

from src.core.subprocess.types import ProtocolTracer


class NodeTracer(ProtocolTracer):
    def fault_detected(self) -> bool:
        """Check if the process failed.
        Failed if capture exit status > 0, ERROR logs or stderr pipe.

        :return: If process failed True is returned otherwise False.
        :rtype: bool
        """

        ...

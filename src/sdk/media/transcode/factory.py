@contextmanager
def streaming(_format: FormatID, **kwargs: Any) -> Iterator[Streaming]:
    """Resolve protocol handler from protocol id

    :param _format: input format to transcode
    :return: Streaming type based on protocol
    :rtype: Streaming
    :raises InvalidStreamingProtocol
    """

    protocols: Dict[FormatID, Type[Streaming]] = {
        FormatID.Webm: DASH,
        FormatID.Mp4: HLS,
    }

    if _format not in protocols:
        raise InvalidStreamingProtocol()

    protocol_class = protocols.get(_format, HLS)
    yield protocol_class(**kwargs)

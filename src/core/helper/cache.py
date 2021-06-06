def retrieve(db, _filter=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :return:
    """
    current_filter = _filter or {}
    return db.movies.find(
        current_filter, no_cursor_timeout=True
    ).batch_size(1000)

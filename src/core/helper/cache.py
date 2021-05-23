def retrieve(db, _filter=None):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :param _filter:
    :return:
    """
    return db.movies.find({
        _filter or {}
    }, no_cursor_timeout=True).batch_size(1000)


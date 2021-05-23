def retrieve_not_processed(db):
    """
    Return available and not processed entries
    from cache tmp db
    :param db:
    :return:
    """
    return db.movies.find({
        "updated": {'$exists': False}
    }, no_cursor_timeout=True).batch_size(1000)

def retrieve(db):
    """
    Return all resolved entries
    from cache tmp db
    :param db: tmp_db
    :return:
    """
    return db.movies.find({
        # All entries in db
    }, no_cursor_timeout=True).batch_size(1000)


def retrieve_not_processed(db):
    """
    Return available and not processed entries
    from cache tmp db
    :param db: tmp_db
    :return:
    """
    return db.movies.find({
        "updated": {'$exists': False}
    }, no_cursor_timeout=True).batch_size(1000)

import click, resolvers
import src.core.mongo as mongo
import src.core.scheme as scheme
from src.core import logger
from src.core import helper


@click.command()
def resolve():
    """
    Run resolvers to get metadata
    """

    # Force refresh or resolve tmp db empty
    resolvers_list = resolvers.load()

    # Process each resolver and merge it
    logger.warning(f"Running resolvers")
    resolvers_result = map(helper.runtime.trigger_resolver, resolvers_list)

    # Merge results from migrations
    merged_data = scheme.merge.reduce_gens(resolvers_result)
    logger.notice(f"Data merge complete")

    # Check for valid scheme
    scheme.validator.check(merged_data, many=True)
    logger.success(f"Validated scheme")

    # Start to write obtained entries from src
    logger.notice(f"Inserting entries in mongo")
    helper.cache.rewrite(mongo.temp_db, merged_data)  # Add data to helper db
    logger.success(f"Entries indexed: {len(merged_data)}")

import click
import resolvers
import src.core.mongo as mongo
import src.core.scheme as scheme
from src.core import logger, cache, runtime


@click.command()
def resolve():
    """
    Run resolvers to get metadata
    """

    # Force refresh or resolve tmp db empty
    resolvers_list = resolvers.load()

    # Process each resolver and merge it
    logger.log.warning("Running resolvers")
    resolvers_result = map(runtime.trigger_resolver, resolvers_list)

    # Merge results from migrations
    merged_data = scheme.merge.reduce_gens(resolvers_result)
    logger.log.notice("Data merge complete")

    # Check for valid scheme
    scheme.validator.check(merged_data, many=True)
    logger.log.success("Validated scheme")

    # Start to write obtained entries from src
    logger.log.notice("Inserting entries in mongo")
    cache.rewrite(mongo.temp_db, merged_data)  # Add data to helper db
    logger.log.success(f"Entries indexed: {len(merged_data)}")

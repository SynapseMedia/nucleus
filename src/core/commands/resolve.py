import click, resolvers
import src.core.mongo as mongo
import src.core.scheme as scheme
from src.core import logger, Log
from src.core import helper


@click.command()
def resolve():
    """
    Run resolvers to get metadata and store it in `tmp db`
    """

    # Force refresh or resolve tmp db empty
    logger.info('Rewriting...')
    resolvers_list = resolvers.load()

    # Process each resolver and merge it
    logger.warning(f"{Log.WARNING}Running resolvers{Log.ENDC}")
    resolvers_result = map(helper.runtime.results_generator, resolvers_list)

    # Merge results from migrations
    logger.warning(f"{Log.WARNING}Starting merge{Log.ENDC}")
    merged_data = scheme.merge.reduce_gens(resolvers_result)
    logger.info(f"{Log.OKGREEN}Data merge complete{Log.ENDC}")

    # Check for valid scheme
    scheme.validator.check(merged_data, many=True)
    logger.info(f"{Log.OKGREEN}Valid scheme{Log.ENDC}")

    # Start to write obtained entries from src
    logger.info(f"{Log.OKGREEN}Inserting entries in mongo{Log.ENDC}")
    helper.runtime.rewrite_entries(mongo.temp_db, merged_data)  # Add data to helper db
    logger.info(f"{Log.UNDERLINE}Entries indexed: {len(merged_data)}{Log.ENDC}")

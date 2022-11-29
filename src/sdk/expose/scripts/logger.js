process.env.FORCE_COLOR = 1
const chalk = require('chalk')
const logger = require('pino')({prettyPrint: true});

module.exports = {
    success: (msg) => logger.info(chalk.green(msg)),
    info: (msg) => logger.info(chalk.cyan(msg)),
    warn: (msg) => logger.warn(chalk.yellow(msg)),
    err: (msg) => logger.err(chalk.red(msg)),
};
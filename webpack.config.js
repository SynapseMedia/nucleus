require("dotenv").config();

const Dotenv = require('dotenv-webpack');
const path = require("path");

const nodeExternals = require('webpack-node-externals');
const webpack = require("webpack");

const Settings = require("./package.json");

module.exports = function (env) {
    //Handle environment
    const ENV = `development` in env && `development` || `production`;
    process.env[`NODE_ENV`] = ENV;

    //Default plugin for usage
    let defaultPlugin = [
        new Dotenv(),
        new webpack.ProvidePlugin(Settings.manifest.plugins),
    ];

    return {
        mode: ENV,
        entry: ['@babel/polyfill', './src/index.js'],
        output: {
            path: path.resolve(__dirname, './dist'),
            filename: 'index.bundle.js'
        },
        watchOptions: {
            ignored: /node_modules/,
            poll: 200 // Check for changes every second
        },
        target: 'node',
        node: {
            // Need this when working with express, otherwise the build fails
            __dirname: false,   // if you don't put this is, __dirname
            __filename: false,  // and __filename return blank or /
        },
        externals: [nodeExternals()], // Need this to avoid error when working with Express
        resolve: {
            extensions: [`.js`, `.jsx`],
            modules: [
                path.resolve(`./src`),
                path.resolve(`./node_modules`)
            ]
        },
        plugins: defaultPlugin,
    };
};

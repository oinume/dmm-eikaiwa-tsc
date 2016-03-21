module.exports = {
    entry: "./src/hello.js",
    output: {
        path: __dirname,
        filename: "static/built/bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: "babel-loader", // "babel-loader" is also a legal name to reference
                query: {
                    presets: ["es2015"]
                }
            }
        ]
    }
};

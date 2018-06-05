module.exports = {

  context: __dirname,
  devtool: 'source-map', // create source map so you can easily debug minified js files

  entry: {
    test: ["babel-polyfill", __dirname + "/js-src/test.js"],
    gateway: ["babel-polyfill", __dirname + "/js-src/gateway.js"],
  },

  output: {
    path:__dirname + "/static/dist",
    filename: "[name].js",
    sourceMapFilename: "[name].map"
  },

  module: {
    rules: [
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        }
      }
    ]
  },

}

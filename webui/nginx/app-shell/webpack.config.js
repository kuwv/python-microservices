const glob = require('glob');
const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = env => ({
  devServer: {
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
    disableHostCheck: true,
    historyApiFallback: true
  },
  devtool: "sourcemap",
  module: {
    rules: [
      { parser: { system: false } },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: [{ loader: "babel-loader" }]
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      inject: false,
      template: "src/index.ejs",
      templateParameters: {
        public_protocol: process.env.PUBLIC_PROTOCOL || 'http',
        public_hostname: process.env.PUBLIC_HOSTNAME || 'localhost'
      }
    }),
    new CleanWebpackPlugin()
  ],
  entry: {
    auth: path.resolve(__dirname, "src/plugins/auth"),
    rest: path.resolve(__dirname, "src/plugins/rest")
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "dist"),
    libraryTarget: "system"
  },
  externals: ["single-spa", "vue", "vue-router", /^@vue-mf\/.+$/]
});

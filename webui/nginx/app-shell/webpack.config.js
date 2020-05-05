const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = env => ({
  entry: path.resolve(__dirname, "src/vue-mf-root-config"),
  output: {
    filename: "vue-mf-root-config.js",
    libraryTarget: "system",
    path: path.resolve(__dirname, "dist")
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
  devServer: {
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
    disableHostCheck: true,
    historyApiFallback: true
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
  externals: ["single-spa", "vue", "vue-router", /^@vue-mf\/.+$/]
});

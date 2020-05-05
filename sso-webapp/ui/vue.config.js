module.exports = {
  lintOnSave: true,
  configureWebpack: {
    devServer: {
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      disableHostCheck: true,
      host: '0.0.0.0',
      port: 3000
    },
    externals: ['vue', 'vue-router', /^@vue-mf\/.+/]
  },
  outputDir: '../static',
  filenameHashing: false
};

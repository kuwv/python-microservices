module.exports = {
  lintOnSave: true,
  configureWebpack: {
    devServer: {
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      disableHostCheck: true,
      sockPort: 3000,
      sockHost: '0.0.0.0'
    },
    externals: ['vue', 'vue-router', /^@vue-mf\/.+/]
  },
  outputDir: '../static',
  filenameHashing: false
};

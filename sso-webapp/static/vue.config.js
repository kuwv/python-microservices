module.exports = {
  publicPath: process.env.WEBAPP_URI_PREFIX !== 'undefined'
    ? process.env.WEBAPP_URI_PREFIX
    : '/'
}

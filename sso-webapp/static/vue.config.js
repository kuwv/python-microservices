module.exports = {
  publicPath: process.env.WEBAPP_URI_STATIC !== 'undefined'
    ? process.env.WEBAPP_URI_STATIC
    : ''
}

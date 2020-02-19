import gulp from 'gulp';
const {protractor, webdriver_update }  = require('gulp-protractor');

import { CLIOptions } from 'aurelia-cli';
import { default as runAppServer, shutdownAppServer } from './run';


function runApp(cb) {
  if (CLIOptions.hasFlag('start')) {
    runAppServer();
  }
  cb();
}

function runProtractor(cb) {
  gulp.src('test/e2e/**/*.e2e.js')
    .pipe(protractor({ configFile: 'protractor.conf.js', args: process.argv.slice(3) }))
    .on('end', () => {
      shutdownAppServer();
      cb();
    })
    .on('error', err => {
      shutdownAppServer();
      cb(err);
    });
}

// Setting up the test task
export default gulp.series(
  runApp,
  webdriver_update,
  runProtractor
);


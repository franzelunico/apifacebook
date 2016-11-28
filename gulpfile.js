'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    exec = require('child_process').exec,
    browserSync = require('browser-sync').create();

gulp.task('runserver', function() {
  var child = exec('tail -f configs/sites-enabled/access.log  configs/sites-enabled/error.log');
  child.stdout.pipe(process.stdout);
  child.stderr.pipe(process.stderr);

});

gulp.task('styles', function () {
   gulp.src('./static/sass/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./static/css'))
    .pipe(browserSync.reload({stream: true}));
});

gulp.task('serve', ['runserver'], function() {
	browserSync.init({
		notify: false,
		port: 8000,
		domain: 'local.fl.code.bo'
    });
    gulp.watch('./static/sass/*.scss', ['styles']);
    gulp.watch('./static/css/*.css').on('change', browserSync.reload);
    gulp.watch('./gettoken/templates/gettoken/*.html').on('change', browserSync.reload);
});

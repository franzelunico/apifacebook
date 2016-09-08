'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    exec = require('child_process').exec,
    browserSync = require('browser-sync').create();

gulp.task('runserver', function() {
  exec('python manage.py runserver 127.0.0.1:8001');
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

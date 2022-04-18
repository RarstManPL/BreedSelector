;(function($) {
	$.fn.preloadinator = function(options) {
		'use strict';

		var settings = $.extend({
			minTime: 0,
			permanently: false,
			animation: 'fadeOut',
			animationDuration: 500,
		}, options),
		preloader = this,
		start = new Date().getTime();

		$.fn.preloadinator.removePreloader = function() {
			$(preloader)[settings.animation](settings.animationDuration);
		    $('body').css('overflow', 'auto');
		}

		$.fn.preloadinator.minTimeElapsed = function() {
			var now = new Date().getTime(),
			elapsed = now - start;

			if(elapsed >= settings.minTime) {
				return true;
			}
			else {
				return false;
			}
		}

		if(settings.permanently) {
		    return true;
		}

		$(window).on('load', function() {
			if($.fn.preloadinator.minTimeElapsed()) {
				$.fn.preloadinator.removePreloader();
			}
			else {
				var now = new Date().getTime(),
				elapsed = now - start;

				setTimeout($.fn.preloadinator.removePreloader, settings.minTime - elapsed);
			}
		});

	    return this;
	}
}(jQuery));
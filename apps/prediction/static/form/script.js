var current_fs, next_fs, previous_fs;
var animating;

$("#progressbar li").css("width", (100/$("#progressbar li").length) + "%");

$(".next").click(function(){
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent().parent();
	next_fs = $(this).parent().parent().next();

	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    next_fs.removeClass('d-none');

	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
		    current_fs.addClass('d-none');
			next_fs.css({'left': (now * 5)+"%", 'opacity': 1 - now});
		},
		duration: 300,
		complete: function(){
			animating = false;
		},
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent().parent();
	previous_fs = $(this).parent().parent().prev();

	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    previous_fs.removeClass('d-none');

	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
		    current_fs.addClass('d-none');
			previous_fs.css({'opacity': 1 - now, 'right': (now * 5)+"%"});
		},
		duration: 300,
		complete: function(){
			animating = false;
		},
		easing: 'easeInOutBack'
	});
});


/** custom.js **/

(function($){
    $(document).ready(function(){


        /*======= For parallex bg =================== */
        // jQuery.each( jQuery('.testimonials'), function(){
        //    jQuery('.bg', this).parallax("50%", 0.4);
        // });


        /*=======  For Scroll to top  =================== */
        try
        {
            $('.top-arrow a').click(function(event) {
                event.preventDefault();
                var liIndex = $(this).index();
                var contentPosTop = $('html').eq(liIndex).position().top;

                $('html, body').stop().animate({
                    scrollTop : contentPosTop
                }, 1500);
            });
        }
        catch (someException)
        {
        }

        /*=================== onScroll Animation =======================*/
        try
        {
            $(window).scroll(function(){

                /* Why choose us animation*/
                // if  (isScrolledIntoView($(".about-block"))){
                //   $(".middle .ol-circle li").addClass('animated');
                //}

                /*  Recent work */
                if  (isScrolledIntoView($(".recent-work"))){
                    $(".recent-item").addClass('animated');
                }

            });
        }
        catch (someException)
        {
        }

        function isScrolledIntoView(elem)
        {
            try
            {
                var eleoffset= 100;
                var docViewTop = $(window).scrollTop();
                var docViewBottom = docViewTop + $(window).height() ;

                var elemTop = $(elem).offset().top  ;
                var elemBottom = elemTop + $(elem).height() - eleoffset;

                return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
            }
            catch (someException)
            {
            }
        }

        function isScrolledIntoViewhide(elem)
        {
            try
            {
                var eleoffset= 200;
                var docViewTop = $(window).scrollTop();
                var docViewBottom = docViewTop + $(window).height() ;

                var elemTop = $(elem).offset().top + eleoffset;
                var elemBottom = elemTop + $(elem).height() - eleoffset;

                return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
            }
            catch (someException)
            {
            }
        }

        /*=================== End onScroll Animation =======================*/

    });
})(jQuery);

/*Back to Top */
(function($) {
	$(document).ready(function() {
		// Show or hide the sticky footer button
		$(window).scroll(function() {
			if ($(this).scrollTop() > 200) {
				$('.go-top').fadeIn(200);
			} else {
				$('.go-top').fadeOut(200);
			}
		});

		// Animate the scroll to top
		$('.go-top').click(function(event) {
			event.preventDefault();

			$('html, body').animate({scrollTop: 0}, 300);
		});
	});
}) (jQuery);
/**
 * crypTool specific js
 * User: fs
 */
jQuery(document).ready(function(){
    !(function ($){

        var longIds = {
            'ctp': 'cryptool1',
            'ct1': 'cryptool1',
            'ct2': 'cryptool2',
            'jct': 'jcryptool',
            'cto': 'cryptool-online',
            'mtc': 'mystery-twister'

        };

        var downloads= {
            'cryptool1': '.item-494',
            'cryptool2': '.item-495',
            'jcryptool': '.item-497'
        };

        var pageType;

        var autoSlides = [];
        var currSlide = 0;
        var interval = null;

        /**
         * getPageType
         * @returns {string|string}
         */
        var getPageType = function() {
            return longIds[window.ioApp.pageId];
        };

        //----------------------------------------------------------------------
        // top slider
        //---------------------------------------------------------------------//

        var topSliderCtrl = function(pageType){

            var activateTopSlide = function(pageType){

                pageType = pageType.replace('en/','')
                                   .replace('de/','');

                console.log(pageType);

                // remove active states
                $('.slides').removeClass('active');
                $('.top-slider-ctrl li').removeClass('active');
                $('.downloads ul li').removeClass('active');

                // add active state
                if (pageType === 'mtc3') pageType = 'mystery-twister'; // fix inconsistency of mtc3
                $('#'+pageType).addClass('active');
                if (pageType === 'mystery-twister') pageType = 'mtc3'; // fix inconsistency of mtc3
                $($('.top-slider-ctrl li a[href="/'+pageType+'"]')).parent().addClass('active');
                if (downloads[pageType]){
                    $(downloads[pageType]).addClass('active');
                }
            }

            activateTopSlide(pageType);

            var startSlideShow = function(){
                activateTopSlide(autoSlides[currSlide]);
                interval = setInterval(function() {
                    currSlide++;
                    if (currSlide >= autoSlides.length) currSlide = 0;
                    activateTopSlide(autoSlides[currSlide]);
                }, 10000)
            }

            var stopSlideShow = function(){
                clearInterval(interval);
            }

            // event
            $('.top-slider-ctrl li').on('click', function(eve){
                window.location=$(this).children('a').attr('href');
                eve.preventDefault();
                return false;
            });
            // event
            $('.top-slider-ctrl li').on('mouseover', function(eve){
                var pt = $(this).children('a').attr('href').substring(1);
                stopSlideShow();
                activateTopSlide(pt);
            });
            $('.top-slider-ctrl li').on('mouseout', function(eve){
                if (pageType === 'cryptool'){
                    startSlideShow();
                } else {
                    activateTopSlide(pageType);
                }
            });

            // start slideshow on portal page
            if (ioApp.pageId === 'ctp' && ioApp.pageType === 'homePage'){
               for(var el in longIds){
                   autoSlides.push(longIds[el]);
               }
               autoSlides.splice(0,1); // remove first element to avoid double cryptool1
               startSlideShow();
            }
        };


        //shortCutClass = $('ul[id^="home-"]').attr('id').split('-')[1];
        // get page Type
        pageType = getPageType();
        // init slideshow
        topSliderCtrl(pageType);
        // set pageswitcher bottom active
        var suffix = ioApp.pageId === 'mtc' ? 'mtc3' : ioApp.pageId;
        $('a[class="cm-'+suffix+'"]').addClass('active');

    })(jQuery);

});
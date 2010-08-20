(function ($) {
  $.fn.ploneCarousel = function(options) {
    var opts = $.extend({}, $.fn.ploneCarousel.defaults, options);
    return this.each(function(){
      var carousel = $(this);
      var banners = carousel.find('.carousel-banner');
      // Set the dimensions of the carousel based on the dimensions
      // of the first banner.
      carousel.add(banners).height(opts.height).width(opts.width);
      banners.css({
        position: 'absolute'
      })
      var timer = setInterval(function () {
        // Rotate
      }, opts.delay)
    });
  };
  
  $.fn.ploneCarousel.defaults = {
    speed: 500,
    delay: 8000,
    height: 'auto',
    width: 'auto',
    transition: 'cross-fade'
  }
})(jQuery);

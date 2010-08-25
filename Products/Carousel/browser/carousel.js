(function ($) {
  function PloneCarousel(container, opts) {
    var carousel = this;
    this.container = $(container).find('.carousel-banners');
    this.banners = this.container.find('.carousel-banner');
    this.current_index = 0;
    this.animating = false;
    this.opts = opts;
    
    // Set the dimensions of the carousel.
    this.container.add(this.banners).height(opts.height).width(opts.width).css({
      position: 'relative',
      overflow: 'hidden'
    });
    this.banners.css({
      position: 'absolute'
    });
    
    this.shiftIndex = function (offset, old_index) {
      if (old_index == undefined) {
        old_index = this.current_index;
      }
      var max_index = this.banners.length - 1;
      var new_index = old_index + offset;
      if (new_index > max_index) {
        new_index -= this.banners.length;
      } else if (new_index < 0) {
        new_index += this.banners.length;
      }
      return new_index;
    };
    
    this.nextBanner = function () {
      var next_index = this.shiftIndex(1);
      this.animateTo(next_index);
    };
    
    this.prevBanner = function () {
      var prev_index = this.shiftIndex(-1);
      this.animateTo(prev_index);
    };
    
    this.animateTo = function (index, callback) {};
        
    this.play = function () {
      carousel.timer = setInterval(function () {
        carousel.nextBanner();
      }, carousel.opts.delay);
    };
    
    this.pause = function () {
      if (carousel.timer) {
        clearInterval(carousel.timer);
      }
    };
  };
  
  function FadingPloneCarousel(container, opts) {
    PloneCarousel.apply(this, [container, opts]);
    var carousel = this;
  
    this.animateTo = function (index, callback) {
      if (index == this.current_index) return;
      this.banners.not(':eq(' + index.toString() + ')').fadeOut(this.opts.speed, function () {
        carousel.current_index = index;
      });
      this.banners.eq(index).fadeIn(this.opts.speed, function () {
        carousel.current_index = index;
      });
    };
  };
  
  function SlidingPloneCarousel(container, opts) {
    PloneCarousel.apply(this, [container, opts]);
    var carousel = this;

    this.animateTo = function (index, callback) {
      if (index == this.current_index) return;
      this.banners.each(function (banner_index, banner) {
        var new_index = carousel.shiftIndex(banner_index, -carousel.current_index);
        $(banner).css('left', (new_index * 100).toString() + '%').show();
      });
      var shift = carousel.shiftIndex(index, -carousel.current_index);
      this.banners.animate({
        left: '-=' + (100 * shift)+ '%'
      }, function () {
        carousel.current_index = index;
      });
    };
  };
  
  $.fn.ploneCarousel = function(options) {
    var opts = $.extend({}, $.fn.ploneCarousel.defaults, options);
    return this.each(function(){
      var container = $(this).height(opts.height).width(opts.width);
      var carousel = new FadingPloneCarousel(container, opts);
      carousel.play();
      container.hover(carousel.pause, carousel.play);
      var pager_items = container.find('.carousel-pager-item');
      pager_items.click(function () {
        carousel.animateTo(pager_items.index($(this)));
      });
      
    });
  };
  
  $.fn.ploneCarousel.defaults = {
    speed: 500,
    delay: 4000,
    height: 'auto',
    width: 'auto',
    transition: 'cross-fade'
  }
})(jQuery);

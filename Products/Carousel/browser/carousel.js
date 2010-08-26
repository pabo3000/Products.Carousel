(function ($) {
  function PloneCarousel(container, opts) {
    var carousel = this;
    this.container = $(container).find('.carousel-banners');
    this.banners = this.container.find('.carousel-banner');
    this.current_index = 0;
    this.max_index = this.banners.length - 1;
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
      old_index = (old_index == undefined) ? this.current_index : old_index;
      var new_index = old_index + offset;
      if (new_index > this.max_index) {
        new_index -= this.banners.length;
      } else if (new_index < 0) {
        new_index += this.banners.length;
      }
      return new_index;
    };
    
    this.nextBanner = function () {
      this.animateTo(this.shiftIndex(1));
    };
    
    this.prevBanner = function () {
      this.animateTo(this.shiftIndex(-1));
    };
    
    this.animateTo = function (index) {};
        
    this.play = function () {
      if (carousel.timer) {
        clearInterval(carousel.timer);
      }
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
  
    this.animateTo = function (index) {
      if (index == this.current_index || this.animating) return;
      this.animating = true;
      this.banners.not(':eq(' + index.toString() + ')').fadeOut(this.opts.speed, function () {
        carousel.current_index = index;
      });
      this.banners.eq(index).fadeIn(this.opts.speed, function () {
        carousel.current_index = index;
        carousel.animating = false;
      });
    };
  };
  
  function SlidingPloneCarousel(container, opts) {
    PloneCarousel.apply(this, [container, opts]);
    var carousel = this;
    this.banners.wrapAll('<div class="carousel-slider" />');
    this.slider = this.container.find('.carousel-slider')
      .height(this.opts.height).width(this.opts.width * this.banners.length)
      .css({
        position: 'absolute',
        left: 0,
        top: 0
      });
          
    this.nextBanner = function () {
      this.animateTo(this.shiftIndex(1), 'left');
    };
    
    this.prevBanner = function () {
      this.animateTo(this.shiftIndex(-1), 'right');
    };

    this.animateTo = function (index, direction) {
      if (index == this.current_index || this.animating) return;
      this.animating = true;
            
      // Set the direction of animation if it isn't set explicitly.
      direction = (direction == undefined) ? 'left' : direction;
      
      // Figure out the shift.
      var shift = (direction == 'left') ? -carousel.current_index : carousel.max_index - carousel.current_index;
      
      // Position the banners on the slider.
      this.banners.each(function (banner_index, banner) {
        var new_index = carousel.shiftIndex(shift, banner_index);
        $(banner).css('left', (new_index * carousel.opts.width)).show();
      });
      
      // Position the slider.
      var start_left = (direction == 'left') ? 0 : -this.opts.width * this.max_index;
      this.slider.css('left', start_left);
      
      // Do the animation.
      var single_offset = (direction == 'left') ? this.opts.width : -this.opts.width;
      var index_offset = this.shiftIndex(shift, index);
      this.slider.animate({
        left: '-=' + (single_offset * index_offset).toString() + 'px'
      }, this.opts.speed, 'swing', function () {
        carousel.current_index = index;
        carousel.animating = false;
      });
    };
  };
  
  $.fn.ploneCarousel = function(options) {
    var opts = $.extend({}, $.fn.ploneCarousel.defaults, options);
    return this.each(function(){
      var container = $(this);
      if (opts.transition == 'fade') {
        var carousel = new FadingPloneCarousel(container, opts);
      } else {
        var carousel = new SlidingPloneCarousel(container, opts);
      }
      carousel.play();
      container.hover(carousel.pause, carousel.play);
      
      // Set up the pager.
      var pager_items = container.find('.carousel-pager-item');
      pager_items.filter(':first').addClass('carousel-pager-item-first');
      pager_items.filter(':last').addClass('carousel-pager-item-last');
      pager_items.click(function () {
        carousel.animateTo(pager_items.index($(this)));
        return false;
      });
      
      // Set up forward and back buttons.
      container.find('.carousel-pager-button-prev').click(function () {
        carousel.prevBanner();
        return false;
      });
      container.find('.carousel-pager-button-next').click(function () {
        carousel.nextBanner();
        return false;
      });
      
    });
  };
  
  $.fn.ploneCarousel.defaults = {
    speed: 500,
    delay: 8000,
    height: 0,
    width: 0,
    transition: 'fade'
  }

})(jQuery);

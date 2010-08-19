from Products.Five import BrowserView
from Products.Carousel.interfaces import ICarousel

class CarouselManager(BrowserView):
    
    def __call__(self):
        
        carousel = ICarousel(self.context)
        if not carousel.hasCarousel():
            carousel.addCarousel()
        else:
            carousel.editCarousel()

from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary

from Products.Carousel import CarouselMessageFactory as _

class ICarousel(Interface):
    """
    A rotating display of banners.
    """

    def getSettings():
        """
        Returns an object that provides ICarouselSettings.
        """

    def getBanners():
        """
        Returns a list of objects that provide ICarouselBanner.
        """

class ICarouselSettings(Interface):
    """
    Settings for a Carousel.
    """
    
    enabled = schema.Bool(
        title=_(u'Enabled'),
        description=_(u'This Carousel should be displayed.'),
        default=True,
    )
    
    banner_template = schema.Choice(
        title=_(u'Banner Template'),
        vocabulary='Products.Carousel.BannerTemplates',
    )
    
    banner_elements = schema.List(
        title=_('Banner Elements'),
        description=_(u'Select the elements that should be visible on the' 
            u' banner. Note that not all templates may provide all elements.'),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary.fromItems((
                (u'Title', u'title'), 
                (u'Text', u'text'),
                (u'Image', u'image'),
            )),
        ),
        default=[u'title', u'text', u'image'],
        required=False,
    )
    
    width = schema.Int(
        title=_(u'Banner Width'),
        description=_(u'Enter the width of the banner in pixels.'),
        required=False,
    )
    
    height = schema.Int(
        title=_(u'Banner Height'),
        description=_(u'Enter the height of the banner in pixels.'),
        required=False,
    )
    
    pager_template = schema.Choice(
        title=_(u'Pager Template'),
        vocabulary='Products.Carousel.PagerTemplates',
    )
    
    transition_type = schema.Choice(
        title=_(u'Transition'),
        vocabulary=SimpleVocabulary.fromItems((
            (u'Cross Fade', u'cross-fade'),
            (u'Slide Left', u'slide-left'),
            (u'Slide Right', u'slide-right'),
        )),
        default=u'cross-fade',
    )
    
    transition_speed = schema.Float(
        title=_(u'Transition Speed'),
        description=_(u'Enter the speed of the transition in seconds.'),
        default=0.5,
        min=0.0,
    )
    
    transition_delay = schema.Float(
        title=_(u'Transition Delay'),
        description=_(u'Enter the delay between transitions in seconds.'),
        default=8.0,
        min=0.0,
    )
    
    default_page_only = schema.Bool(
        title=_(u'Only display on the default item'),
        description=_(u'Only display the Carousel on the default item of this'
            ' folder. Otherwise, the Carousel appears on every item in'
            ' the folder.'),
        default=True,
    )
    
class ICarouselSettingsView(Interface):
    """
    Marker interface for the view that displays the Carousel settings form.
    """

class ICarouselFolder(Interface):
    """Marker for a folder that can hold Carousel banners."""

class ICarouselBanner(Interface):
    """A carousel banner which may include an image, text, and/or link."""
    
    def getSize(scale=None):
        """ Wraps the getSize method of the image field.
        """
    
    def tag(**kw):
        """ Wraps the tag method of the image field."""

class ICarouselBrowserLayer(Interface):
    """Marker applied to the request during traversal of sites that
       have Carousel installed
       
       Not used anymore, but here for BBB.
    """

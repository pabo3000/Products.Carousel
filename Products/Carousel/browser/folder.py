from persistent import Persistent
from zope.annotation import factory
from zope.component import adapts
from zope.interface import implements
from z3c.form import form, field
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget, \
    CheckBoxFieldWidget
from plone.app.z3cform.layout import FormWrapper
from Products.CMFCore.interfaces import IFolderish
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.Carousel.interfaces import ICarousel, ICarouselSettings, \
    ICarouselFolder, ICarouselSettingsView, ICarouselBanner

class Carousel(object):
    implements(ICarousel)
    adapts(ICarouselFolder)
    
    def __init__(self, context):
        self.context = context
        
    def getSettings(self):
        """
        Returns an object that provides ICarouselSettings.
        """
        
        return ICarouselSettings(self.context)

    def getBanners(self):
        """
        Returns a list of objects that provide ICarouselBanner.
        """
        
        banner_objects = []
        if IFolderish.providedBy(self.context):
            banner_objects = self.context.objectValues()
        elif IATTopic.providedBy(self.context):
            banner_objects = [brain.getObject() for brain \
                in self.context.queryCatalog()]
        
        return [b for b in banner_objects if ICarouselBanner.providedBy(b)]

class CarouselSettings(Persistent):
    """
    Settings for a Carousel instance.
    """
    
    implements(ICarouselSettings)
    adapts(ICarouselFolder)
    
    def __init__(self):
        self.enabled = True
        self.banner_template = u'@@banner-default'
        self.banner_elements = [u'title', u'text', u'image']
        self.width = None
        self.height = None
        self.pager_template = u'@@pager-numbers'
        self.transition_type = u'cross-fade'
        self.transition_speed = 0.5
        self.transition_delay = 8.0
        self.default_page_only = True
        
CarouselSettingsFactory = factory(CarouselSettings)

class CarouselSettingsForm(form.EditForm):
    """
    Form for editing Carousel settings.
    """

    fields = field.Fields(ICarouselSettings)
    fields['enabled'].widgetFactory = SingleCheckBoxFieldWidget
    fields['banner_elements'].widgetFactory = CheckBoxFieldWidget
    fields['default_page_only'].widgetFactory = SingleCheckBoxFieldWidget
    
    def getContent(self):
        return ICarouselSettings(self.context)
        
class CarouselSettingsView(FormWrapper):
    """
    View for searching and filtering ATResources.
    """
    
    implements(ICarouselSettingsView)

    form = CarouselSettingsForm
    
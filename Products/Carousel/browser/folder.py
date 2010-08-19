from Acquisition import aq_base, aq_parent
from persistent import Persistent
from zope.annotation import factory
from zope.component import adapts
from zope.interface import implements, alsoProvides
from z3c.form import form, field
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget, \
    CheckBoxFieldWidget
from plone.app.z3cform.layout import FormWrapper
from plone.memoize import instance
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.Carousel.interfaces import ICarousel, ICarouselSettings, \
    ICarouselFolder, ICarouselBanner, ICarouselSettingsView
from Products.Carousel.utils import addPermissionsForRole

CAROUSEL_ID = 'carousel'

class Carousel(object):
    implements(ICarousel)
    adapts(IFolderish)
    
    def __init__(self, context):
        self.context = context
        
    @instance.memoize
    def _carousel_folder(self):
        """
        Returns the Carousel folder or None if there isn't one.
        """
        
        if hasattr(aq_base(self.context), CAROUSEL_ID):
            return getattr(self.context, CAROUSEL_ID)
        return None
    
    def hasCarousel(self):
        """
        Returns True if the context has a Carousel.
        """
        
        return self._carousel_folder() is not None
        
    def addCarousel(self):
        """
        Adds a Carousel to this context.
        """
        
        pt = getToolByName(self.context, 'portal_types')
        newid = pt.constructContent('Folder', self.context, 'carousel',
            title='Carousel Banners', excludeFromNav=True)
        carousel = getattr(self.context, newid)
        
        # mark the new folder as a Carousel folder
        alsoProvides(carousel, ICarouselFolder)
        
        # make sure Carousel banners are addable within the new folder
        addPermissionsForRole(carousel, 'Manager', ('Carousel: Add Carousel Banner',))
        
        # make sure *only* Carousel banners are addable
        carousel.setConstrainTypesMode(1)
        carousel.setLocallyAllowedTypes(['Carousel Banner'])
        carousel.setImmediatelyAddableTypes(['Carousel Banner'])
        
        self.context.REQUEST.RESPONSE.redirect(
            carousel.absolute_url() + '/@@edit-carousel'
        )
        
    def editCarousel(self):
        """
        Edit the Carousel.
        """
                
        self.context.REQUEST.RESPONSE.redirect(
            self._carousel_folder().absolute_url() + '/@@edit-carousel'
        )
        
    def getSettings(self):
        """
        Returns an object that provides ICarouselSettings.
        """
        
        return ICarouselSettings(self.context)

    def getBanners(self):
        """
        Returns a list of objects that provide ICarouselBanner.
        """
        
        for banner in self.objectValues():
            if ICarouselBanner.providedBy(banner):
                yield banner

class CarouselSettings(Persistent):
    """
    Settings for a Carousel instance.
    """
    
    implements(ICarouselSettings)
    adapts(IFolderish)
    
    def __init__(self):
        self.enabled = True
        self.banner_template = None
        self.banner_elements = [u'title', u'text', u'image']
        self.width = None
        self.height = None
        self.pager_template = None
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
        return ICarousel(aq_parent(self.context)).getSettings()
        
class CarouselSettingsView(FormWrapper):
    """
    View for searching and filtering ATResources.
    """
    
    implements(ICarouselSettingsView)

    form = CarouselSettingsForm
    
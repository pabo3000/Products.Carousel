from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from Products.Carousel.interfaces import ICarousel

def getContext(context):
    """
    The context for the vocabulary could be an annotation, so we need
    this wrapper to get the real context.
    """
    
    if not hasattr(context, 'REQUEST') and hasattr(context, '__parent__'):
        return context.__parent__
    return context

def getBannerTemplates(context):
    context = getContext(context)
    menu = getUtility(IBrowserMenu, name='carousel_bannertemplates')
    items = menu.getMenuItems(ICarousel(context), context.REQUEST)
    return SimpleVocabulary.fromItems([(i['title'], i['action']) for i in items])
    
def getPagerTemplates(context):
    context = getContext(context)
    menu = getUtility(IBrowserMenu, name='carousel_pagertemplates')
    items = menu.getMenuItems(ICarousel(context), context.REQUEST)
    return SimpleVocabulary.fromItems([(i['title'], i['action']) for i in items])
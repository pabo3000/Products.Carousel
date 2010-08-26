from Products.CMFCore.utils import getToolByName
from Products.Carousel.interfaces import ICarouselBanner

def null_upgrade_step(setup_tool):
    """
    This is a null upgrade. Use it when nothing happens
    """
    pass
    
def upgrade_11_to_20a1(setup_tool):
    """
    Upgrade old Carousel banners by moving the description into the new
    body field.
    """
    
    catalog = getToolByName(setup_tool, 'portal_catalog')
    transforms = getToolByName(setup_tool, 'portal_transforms')
        
    banners = catalog.searchResults({
        'object_provides': ICarouselBanner.__identifier__,
    })
    
    for banner in banners:
        description = banner.Description
        if description:
            html = transforms.convertTo('text/html',
                description, mimetype='text/plain')
            banner.getObject().setText(html.getData(), mimetype='text/html')
            
    actions = getToolByName(setup_tool, 'portal_actions')
    obj_actions = actions.get('object', {})
    if 'carousel' in obj_actions.keys():
        obj_actions['carousel'].title = 'Banners'
    
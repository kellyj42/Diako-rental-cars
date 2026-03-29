from content.content import contact_info, nav_links


def contact_info_processor(request):
    return {
        "contact_info": contact_info,
        "nav_links": nav_links,
    }

from content.content import contact_info


def contact_info_processor(request):
    return {
        "contact_info": contact_info,
    }

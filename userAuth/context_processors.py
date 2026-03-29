from django.conf import settings


def google_oauth_processor(request):
    google_settings = settings.SOCIALACCOUNT_PROVIDERS.get("google", {})
    google_app = google_settings.get("APP", {})
    google_oauth_enabled = bool(
        google_app.get("client_id") and google_app.get("secret")
    )
    return {"google_oauth_enabled": google_oauth_enabled}

from django.contrib.admin import ModelAdmin


class URLShortenerModelAdmin(ModelAdmin):
    list_display  = ["url", "pk", "slug", "status"]
    list_filter   = ["created_at", "updated_at"]
    search_fields = ["url", "slug", "status"]
    fieldsets     = (
        ("SEO Information (Optional)", {
            "classes": ["collapse", "wide", "extrapretty"],
            "fields" : ["title", "description", "image"]
        }),
        ("User Data", {
            "classes": ["wide", "extrapretty"],
            "fields" : ["url", "slug"]
        }),
        ("Status", {
            "classes": ["wide", "extrapretty"],
            "fields" : [("status")]
        }),
    )

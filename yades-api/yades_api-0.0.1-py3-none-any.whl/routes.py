from yades_api import views


def setup(app):
    app.router.add_route('GET', r'/inbox', views.inbox_detail)
    app.router.add_route('POST', r'/inbox', views.inbox_create)
    app.router.add_route(
        'GET', r'/emails/{uuid:[\d\w\-]{36}}', views.inbox_email_detail
    )

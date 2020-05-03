import flaskblocks.auth.blueprints
import flaskblocks.auth.providers


def init(providers_config, app, onauthorized):
    providers = {}
    if "stub" in providers_config:
        providers["stub"] = flaskblocks.auth.providers.Stub(
            providers_config["stub"]["users"])

    if "google" in providers_config:
        providers["google"] = flaskblocks.auth.providers.GoogleOAuth2(
            providers_config["google"]["id"],
            providers_config["google"]["secret"],
            scheme=providers_config["google"]["scheme"])

    auth_blueprint = flaskblocks.auth.blueprints.create_auth(
        providers, onauthorized=onauthorized)

    app.register_blueprint(auth_blueprint)

    return providers, auth_blueprint

# this will contain the main code which wraps together all of the code

from flask import Flask

application = Flask(__name__)


@application.route("/healthcheck")
def health_check():
    """Hello word method."""
    return "I am ready to Split-a-bill!!"


# run the app.
if __name__ == "__main__":
    application.run()
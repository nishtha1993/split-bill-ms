from flask import Blueprint

admin_bp = Blueprint('admin', __name__)
@admin_bp.route("/health")
def health_check():
    """Hello word method."""
    return "I am ready to Split-a-bill!!"


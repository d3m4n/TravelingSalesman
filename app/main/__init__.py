__all__ = ['anneal']
from flask import Blueprint

main = Blueprint('main', __name__)

from . import controller


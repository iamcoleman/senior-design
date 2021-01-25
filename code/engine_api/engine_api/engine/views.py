# -*- coding: utf-8 -*-
"""Sentiment Analysis Engine endpoints"""
from flask import Blueprint

blueprint = Blueprint('engine', __name__, url_prefix='/engine')


@blueprint.route('/test', methods=['GET'])
def test():
    return 'It works!'

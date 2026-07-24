"""Helpers for consistent API error responses."""

from flask import jsonify, make_response


def error_response(message, status_code):
    return make_response(jsonify({"error": message}), status_code)

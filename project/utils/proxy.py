"""
A simple proxy server. Usage:
"""
from flask import current_app, Blueprint, request, abort, Response
import requests
import logging

from flask.helpers import url_for

__all__ = ["proxy"]

proxy = Blueprint('proxy', __name__)
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("proxy.py")


@proxy.route('/<path:url>')
def root(url):
    """Fetches the specified URL and streams it out to the client.
    If the request was referred by the proxy itself (e.g. this is an image fetch for
    a previously proxied HTML page), then the original Referer is passed."""
    response = get_source_rsp(url)
    LOG.info("Got %s response from %s", response.status_code, url)
    headers = dict(response.headers)

    def generate():
        for chunk in response.iter_content(current_app.config["CHUNK_SIZE"]):
            yield chunk

    return Response(response.content, headers=headers)


def get_source_rsp(url):
    url = '%s%s' % (current_app.config["REMOTE_URL"], url_for(".root", url=url))
    LOG.info("Fetching %s", url)
    # Ensure the URL is approved, else abort
    if not is_approved(url):
        LOG.warn("URL is not approved: %s", url)
        abort(403)
    # Pass original Referer for subsequent resource requests
    proxy_ref = proxy_ref_info(request)
    headers = {"Referer": "http://%s/%s" % (proxy_ref[0], proxy_ref[1])} if proxy_ref else {}
    # Fetch the URL, and stream it back
    LOG.info("Fetching with headers: %s, %s", url, headers)
    return requests.get(url, stream=True, params=request.args, headers=headers)


def is_approved(url):
    """Indicates whether the given URL is allowed to be fetched.  This
    prevents the server from becoming an open proxy"""
    host = split_url(url)[1]
    return host in current_app.config["APPROVED_HOSTS"]


def split_url(url):
    """Splits the given URL into a tuple of (protocol, host, uri)"""
    proto, rest = url.split(':', 1)
    rest = rest[2:].split('/', 1)
    host, uri = (rest[0], rest[1]) if len(rest) == 2 else (rest[0], "")
    return proto, host, uri


def proxy_ref_info(request_info):
    """Parses out Referer info indicating the request is from a previously proxied page.
    For example, if:
        Referer: http://localhost:8080/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")
    """
    ref = request_info.headers.get('referer')
    if ref:
        _, _, uri = split_url(ref)
        if uri.find("/") < 0:
            return None
        first, rest = uri.split("/", 1)
        if first in "pd":
            parts = rest.split("/", 1)
            r = (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")
            LOG.info("Referred by proxy host, uri: %s, %s", r[0], r[1])
            return r
    return None

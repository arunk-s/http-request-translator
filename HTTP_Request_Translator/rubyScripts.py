#!/usr/bin/python
from __future__ import print_function
from util import check_valid_url, get_url
import sys
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


def generate_script(header_dict, details_dict, searchString=None):
    """Generate the ruby script for the passed request.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :return: Empty
    """
    method = details_dict['method'].strip()
    url = get_url(header_dict['Host'])
    path = details_dict['path']

    if path != "":
        url += path

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'].strip() in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data

    if not check_valid_url(url):
        print("Please enter a valid URL with correct domain name and try again ")
        sys.exit(-1)

    skeleton_code = """
require 'net/http'
require 'uri'

uri = URI('%s')""" % (url)

    if method == "GET":
        skeleton_code += """
req = Net::HTTP::Get.new(uri.request_uri)\n%s %s %s """ % (generate_request_headers(header_dict), is_proxy(details_dict), is_https(url)) + """
response = http.request(req)
"""
    elif method == "POST":
        body = details_dict['data']
        skeleton_code += """
req = Net::HTTP::Post.new(uri.request_uri)\n%s """ % (generate_request_headers(header_dict)) + """
req.body = %s\n %s %s""" % (str(body), is_proxy(details_dict), is_https(url)) + """
response = http.request(req)
"""

    if searchString:
        skeleton_code += """
puts 'Response #{response.code} #{response.message}:'

begin
    require 'colorize'
rescue LoadError
    puts "search option will need colorize to work properly"
    puts "You can install it by gem install colorize"
end

matched = response.body.match /%s/""" % (searchString) + """

original = response.body
if matched then
    for i in 0..matched.length
        original.gsub! /#{matched[i]}/, "#{matched[i]}".green
    end
end
puts original
"""
    else:
        skeleton_code += """
puts "Response #{response.code} #{response.message}:
          #{response.body}"
"""
    print(skeleton_code)


def generate_request_headers(header_dict):
    """ Place the request headers in ruby script from header dictionary

        :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.

        :return: A string of ruby code which places headers in the request.
        :rtype:`str`
    """
    skeleton = ""
    for key, value in header_dict.items():
        skeleton += """req['%s'] = '%s' \n""" % (str(key), str(value))

    return skeleton


def is_https(url):
    """Checks if url is 'https' and returns appropriate ruby code

        :param str url: Url for the request

        :return: A string of ruby code
        :rtype:`str`
    """
    if url.startswith('https'):
        return "\nhttp.use_ssl=true"
    else:
        return ""


def is_proxy(details_dict):
    """Checks if proxy is provided and returns appropriate ruby code

        :param dict details_dict: Dictionary of request details containing proxy specific information.

        :return: A string of ruby code
        :rtype:`str`
    """
    if 'proxy' in details_dict:
        proxy = details_dict['proxy'].split(':')
        return """
proxy_host, proxy_port = '%s', '%s'""" % (proxy[0].strip(), proxy[1].strip()) + """'
http = Net::HTTP.new(uri.hostname, nil, proxy_host, proxy_port)
"""
    else:
        return """
http = Net::HTTP.new(uri.hostname, uri.port)
"""

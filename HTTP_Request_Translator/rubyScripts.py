#!/usr/bin/python

from util import check_valid_url, get_url
import sys
from urllib import quote


def generate_script(header_dict, details_dict, searchString=None):
    method = details_dict['method'].strip()
    url = get_url(header_dict['Host'])
    path = details_dict['path']

    if path != "":
        url += path

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'].strip()
                                 in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data

    if not check_valid_url(url):
        print(
            "Please enter a valid URL with correct domain name and try again ")
        sys.exit(0)

    skeleton_code = """
require 'net/http'
require 'uri'

uri = URI('""" + url + """')"""

    if method == "GET":
        skeleton_code += """
req = Net::HTTP::Get.new(uri.request_uri)\n""" + \
            generate_request_headers(header_dict) + is_proxy(details_dict) + is_https(url) + """
response = http.request(req)
"""
    elif method == "POST":
        body = details_dict['data']
        skeleton_code += """
req = Net::HTTP::Post.new(uri.request_uri)\n""" + \
            generate_request_headers(header_dict) + """
req.body = '""" + str(body) + """'\n""" + is_proxy(details_dict) + is_https(url) + """
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

matched = response.body.match /""" + searchString + """/

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
    print skeleton_code


def generate_request_headers(header_dict):
    skeleton = ""
    for key in header_dict.keys():
        skeleton += """req['""" + \
            str(key) + """'] = '""" + str(header_dict[key]) + "'\n"
    return skeleton


def is_https(url):
    protocol = url.split(':', 2)[0]
    if protocol == "https":
        return "\nhttp.use_ssl=true"
    else:
        return ""


def is_proxy(details_dict):
    if 'proxy' in details_dict:
        return """
proxy_host, proxy_port = '""" + details_dict['proxy'].split(':')[0].strip() +\
            """', '""" + details_dict['proxy'].split(':')[1].strip() + """'
http = Net::HTTP.new(uri.hostname, nil, proxy_host, proxy_port)
"""
    else:
        return """
http = Net::HTTP.new(uri.hostname, uri.port)
"""

code_begin = """
#!/usr/bin/python
from __future__ import print_function
import re
import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def main():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, '{url}')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPHEADER, {headers})
    # for verbosity
    c.setopt(c.VERBOSE, True)
    # Follow redirects
    c.setopt(c.FOLLOWLOCATION, True)
    # For older PycURL versions:
    #c.setopt(c.WRITEFUNCTION, buffer.write)
"""


code_proxy = """
    c.setopt(c.PROXY, '{proxy}')
"""


code_post = """
    # Sets request method to POST
    c.setopt(c.POSTFIELDS, "{data}")  #expects body to urlencoded
"""


code_https = """
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.SSL_VERIFYHOST, 2)
    # If providing updated certs
    # c.setopt(pycurl.CAINFO, "/path/to/updated-certificate-chain.crt")
"""


code_search = """
    try:
        c.perform()
    except pycurl.error, error:
        print('An error occurred: ', error)
    c.close()

    body = buffer.getvalue()
    # Body is a string on Python 2 and a byte string on Python 3.
    # If we know the encoding, we can always decode the body and
    # end up with a Unicode string.
    response = body.decode('iso-8859-1')

    match = re.findall(r"{search_string}", str(response))
    try:
        from termcolor import colored
        lib_available = True
    except ImportError:
        lib_available = False
    if match:
        for item in match:
            if lib_available:
                replace_string = colored(match[item], 'green')
                response = re.sub(match[item], replace_string, str(response))
            else:
                print("Matched item: ",item)

    print(response)


if __name__ == '__main__':
    main()
"""


code_nosearch = """
    try:
        c.perform()
    except pycurl.error, error:
        print('An error occurred: ', error)
    c.close()

    body = buffer.getvalue()
    # Body is a string on Python 2 and a byte string on Python 3.
    # If we know the encoding, we can always decode the body and
    # end up with a Unicode string.
    response = body.decode('iso-8859-1')

    print(response)


if __name__ == '__main__':
    main()
"""

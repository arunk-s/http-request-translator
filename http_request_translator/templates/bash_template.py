code_begin = """
#!/usr/bin/env bash
{transform}
curl"""


code_transform = """
PARAM1=$(echo '{transform_content}' | php -r 'echo {transform_name}(fgets(STDIN));')
"""

code_header = """ --header "{header}:{value}" """


code_proxy = " -x {proxy}"


code_post = """ --data "{data}" """


code_search = """ | egrep --color " {search_string} |$" """


code_nosearch = """ -v --request {method} {url} {headers} --include"""

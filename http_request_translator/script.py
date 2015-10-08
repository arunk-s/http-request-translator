"""

:synopsis: Define the specialize script classes that will generate the script code.

"""

from .base import AbstractScript
from .templates import bash_template, php_template, python_template, ruby_template


class BashScript(AbstractScript):
    """Extended `AbstractScript` class for Bash script code generation.
    Fills code variables for the request from `bash_template`.
    Overrides `_generate_request` method to generate bash specific code.
    """
    code_begin = bash_template.code_begin
    code_header = bash_template.code_header
    code_proxy = bash_template.code_proxy
    code_post = bash_template.code_post
    code_search = bash_template.code_search
    code_nosearch = bash_template.code_nosearch
    code_transform = bash_template.code_transform

    def _generate_begin(self):
        """Overrides the generation of the default beginning of the code.

        :return: Beginning of the code for bash script.
        :rtype: str
        """
        if 'transform' in self.details:
            self._apply_transform()
            return self.code_begin.format(transform=self._generate_transform())
        else:
            return self.code_begin.format(transform='')

    def _generate_request(self):
        code = self.code_nosearch.format(
            method=self.details.get('method', ''),
            url=self.url,
            headers=self._generate_headers())
        if self.search:
            code += self.code_search.format(search_string=self.search.replace('"', '\\"'))
        return code

    def _apply_transform(self):
        """Overrides the original one to apply the transform the url in bash specific way.

        :return: Nothing
        :rtype: `None`
        """
        if 'transform' in self.details:
            md5 = self.details['transform'].get('md5', '')
            self.url = self.url.replace(md5, '$PARAM1')


class PHPScript(AbstractScript):
    """Extended `AbstractScript` class for PHP script code generation.
    Fills code variables for the request from `php_template`.
    Overrides `_generate_begin` method to generate php specific code.
    """
    code_begin = php_template.code_begin
    code_header = php_template.code_header
    code_proxy = php_template.code_proxy
    code_post = php_template.code_post
    code_search = php_template.code_search
    code_nosearch = php_template.code_nosearch
    code_transform = php_template.code_transform

    def _apply_transform(self, var=None):
        """Overrides the original one to apply the transform the url in php specific way.

        :param str var: Variable name to be use to divide the url into

        :return str transform_url: Splitted url which appends appropriate transform variable
        :rtype: `str`
        """
        if 'transform' in self.details:
            md5 = self.details['transform'].get('md5', '')
            if var:
                self.url = self.url.replace(md5, var)
            splits = self.url.split(var)
            transform_url = splits[0] + "' . " + var
            if len(splits) == 2:
                transform_url += " . '" + splits[1]
            return transform_url

    def _generate_begin(self):
        if 'transform' in self.details:
            self.url = self._apply_transform('$transform')
            return self.code_begin.format(url=self.url,
                transform=self._generate_transform()) + self._generate_headers()
        else:
            return self.code_begin.format(url=self.url, transform='') + self._generate_headers()


class PythonScript(AbstractScript):
    """Extended `AbstractScript` class for Python script code generation.
    Fills code variables for the request from `python_template`.
    Overrides `_generate_begin` method to generate python specific code.
    """
    code_begin = python_template.code_begin
    code_proxy = python_template.code_proxy
    code_post = python_template.code_post
    code_https = python_template.code_https
    code_search = python_template.code_search
    code_nosearch = python_template.code_nosearch
    code_transform = python_template.code_transform

    def _generate_begin(self):
        if 'transform' in self.details:
            self.url = self._apply_transform('transform')
            return self.code_begin.format(url=self.url, headers=str(self.headers),
                transform=self._generate_transform())
        else:
            return self.code_begin.format(url=self.url, headers=str(self.headers), transform='')


class RubyScript(AbstractScript):
    """Extended `AbstractScript` class for Ruby script code generation.
    Fills code variables for the request from `ruby_template`.
    Overrides `_generate_begin` method to generate Ruby specific code.
    """
    code_begin = ruby_template.code_begin
    code_header = ruby_template.code_header
    code_proxy = ruby_template.code_proxy
    code_post = ruby_template.code_post
    code_search = ruby_template.code_search
    code_nosearch = ruby_template.code_nosearch
    code_transform = ruby_template.code_transform

    def _generate_begin(self):
        if 'transform' in self.details:
            self.url = self._apply_transform('transform')
            code = self.code_begin.format(url=self.url, method=self.details.get('method', '').strip().lower(),
                transform=self._generate_transform())
        else:
            code = self.code_begin.format(url=self.url, method=self.details.get('method', '').strip().lower(),
                transform='')
        code += ruby_template.code_headers.format(headers=self._generate_headers())
        return code

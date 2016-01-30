# coding=utf-8
import sys

from wopi_validator import validator
from click.testing import CliRunner


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

runner = CliRunner()
result = runner.invoke(validator.run, args=sys.argv)

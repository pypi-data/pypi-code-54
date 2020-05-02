
from epyk.core import Page
from epyk.core.css import Defaults

from epyk_bootstrap.interfaces import Comp
from epyk_bootstrap.core import BsStyles

# Remove the default layout in all the component done by Epyk Core
Defaults.DEFAULT_STYLE = None


MODULES_EXTS = {
  'bootstrap-datetimepicker': {
    'version': '4.17.47',
    'req': [{'alias': 'moment'}, {'alias': 'bootstrap', 'version': '3.4.1'}],
    'website': 'https://material.io/components',
    'register': {'alias': 'mdc', 'module': 'material-components-web.min', 'npm': 'mdc'},
    'modules': [
      {'script': 'bootstrap-datetimepicker.min.js', 'path': 'bootstrap-datetimepicker/%(version)s/js/'},
      {'script': 'bootstrap-datetimepicker.min.css', 'path': 'bootstrap-datetimepicker/%(version)s/css/'},
  ]},
}


class Report(Page.Report):

  ext_packages = MODULES_EXTS

  def __init__(self):
    super(Report, self).__init__()
    self._bs, self._bs_styles = None, None

  @property
  def styles(self):
    """

    """
    if self._bs_styles is None:
      self._bs_styles = BsStyles.BsStyles(self)
    return self._bs_styles

  @property
  def bootstrap(self):
    """
    Description:
    ------------
    Set the material components entry point.
    This will be available in the same way than ui is available for anything else in the core framework.

    Related Pages:

      https://material.io/develop/web/

    :rtype: :doc:`Components.Materials <report/ui>`

    :return: Python HTML object
    """
    self.jsImports.add("bootstrap")
    self.cssImport.add("bootstrap")
    if self._bs is None:
      self._bs = Comp.Bootstrap(self)
    return self._bs


# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import unittest
from backends.apertium import Apertium
from unittest.mock import patch, MagicMock


# See: https://stackoverflow.com/questions/32043035/python-3-urlopen-context-manager-mocking
class TestPagination(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_cm(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = bytes('{"responseData": {"translatedText": "Hauries d\'haver-hi rebut una c\u00f2pia"}, "responseDetails": null, "responseStatus": 200}', 'utf-8')
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
    
        apertium = Apertium('hola')
        translated = apertium.translate_text('You should have received a copy', 'eng|cat')
        self.assertEqual('Hauries d\'haver-hi rebut una còpia', translated)
        mock_urlopen.assert_called_with("https://www.apertium.org/apy/translate?langpair=eng|cat&markUnknown=no&q=You+should+have+received+a+copy")
        #with urllib.request.urlopen('http://foo') as response:
        #    self.assertEqual(response.getcode(), 200)
        #    self.assertEqual(response.read(), 'contents')   self.assertEquals(pagination.page, 2)


if __name__ == '__main__':
    unittest.main()

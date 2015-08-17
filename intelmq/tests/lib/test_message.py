# -*- coding: utf-8 -*-
"""
Testing the Message classes of intelmq.

Unicode is used for all tests.
Most tests are performed on Report, as it is formally the same as Message,
but has a valid Harmonization configuration.
"""
from __future__ import unicode_literals
import unittest

import intelmq.lib.message as message
import intelmq.lib.exceptions as exceptions


LOREM_BASE64 = 'bG9yZW0gaXBzdW0='
DOLOR_BASE64 = 'ZG9sb3Igc2l0IGFtZXQ='
FEED = {'feed.url': u'https://example.com/', 'feed.name': u'Lorem ipsum'}
URL_UNSANE = 'https://example.com/ \r\n'
URL_SANE = 'https://example.com/'
URL_INVALID = '/exampl\n'


class TestMessageFactory(unittest.TestCase):
    """
    Testing basic functionality of MessageFactory.
    """

    def add_report_examples(self, report):
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64)
        return report

    def add_event_examples(self, event):
        event.add('feed.name', 'Example')
        event.add('feed.url', URL_SANE)
        event.add('raw', LOREM_BASE64)
        event.add('time.observation', u'2015-01-01T13:37:00+00:00')
        return event

    def test_report_type(self):
        """ Test if MessageFactory returns a Report. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        self.assertEqual(type(report),
                         message.Report)

    def test_event_type(self):
        """ Test if MessageFactory returns a Event. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual(type(event),
                         message.Event)

    def test_report_subclass(self):
        """ Test if MessageFactory returns a Report subclassed from dict. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        self.assertTrue(isinstance(report, (message.Message, dict)))

    def test_event_subclass(self):
        """ Test if MessageFactory returns a Event subclassed from dict. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertTrue(isinstance(event, (message.Message, dict)))

    def test_invalid_type(self):
        """ Test if Message raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Message"}')

    def test_invalid_type2(self):
        """ Test if MessageFactory raises InvalidArgument for invalid type. """
        with self.assertRaises(exceptions.InvalidArgument):
            message.MessageFactory.unserialize('{"__type": "Invalid"}')

    def test_report_invalid_key(self):
        """ Test if report raises InvalidKey for invalid key in add(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidKey):
            report.add('invalid', 0)

    def test_report_add_raw(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertDictContainsSubset({'raw': LOREM_BASE64},
                                      report)

    def test_report_value(self):
        """ Test if report return value in value(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report.value('raw'))

    def test_report_get(self):
        """ Test if report return value in get(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report.get('raw'))

    def test_report_add_invalid(self):
        """ Test report add raises on invalid value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', '\r\n')

    def test_report_getitem(self):
        """ Test if report return value in __getitem__(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_setitem(self):
        """ Test if report sets value in __setitem__(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report['raw'] = LOREM_BASE64
        self.assertEqual(LOREM_BASE64, report['raw'])

    def test_report_ignore_none(self):
        """ Test if report ignores None. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', None)
        self.assertNotIn('feed.name', report)

    def test_report_ignore_empty(self):
        """ Test if report ignores empty string. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', "")
        self.assertNotIn('feed.name', report)

    def test_report_ignore_hyphen(self):
        """ Test if report ignores '-'. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', '-')
        self.assertNotIn('feed.name', report)

    def test_report_ignore_na(self):
        """ Test if report ignores 'N/A'. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'N/A')
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given(self):
        """ Test if report ignores given ignore value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'IGNORE_THIS', ignore=('IGNORE_THIS'))
        self.assertNotIn('feed.name', report)

    def test_report_ignore_given_invalid(self):
        """ Test if report ignores given ignore value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidArgument):
            report.add('feed.name', 'IGNORE_THIS', ignore=1337)

    def test_report_add_duplicate(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        with self.assertRaises(exceptions.KeyExists):
            report.add('raw', LOREM_BASE64)

    def test_report_add_duplicate_force(self):
        """ Test if report can add raw value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        report.add('raw', DOLOR_BASE64, force=True)
        self.assertDictContainsSubset({'raw': DOLOR_BASE64},
                                      report)

    def test_report_del_(self):
        """ Test if report can del a value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        del report['raw']
        self.assertNotIn('raw', report)

    def test_report_clear(self):
        """ Test if report can clear a value. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('raw', LOREM_BASE64)
        report.clear('raw')
        self.assertNotIn('raw', report)

    def test_report_asdict(self):
        """ Test if report compares as dictionary. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, report)

    def test_report_finditems(self):
        """ Test report finditems() generator. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertDictEqual(FEED, dict(report.finditems('feed.')))

    def test_report_items(self):
        """ Test if report returns all keys in list with items(). """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        for key, value in FEED.items():
            report.add(key, value)
        self.assertListEqual(list(FEED.items()), list(report.items()))

    def test_report_add_byte(self):
        """ Test if report rejects a byte string. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('raw', bytes(LOREM_BASE64))

    def test_report_sanitize_url(self):
        """ Test if report sanitizes an URL. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.url', URL_UNSANE, sanitize=True)
        self.assertEqual(URL_SANE, report['feed.url'])

    def test_report_invalid_url(self):
        """ Test if report sanitizes an invalid URL. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.url', URL_INVALID)

    def test_report_invalid_string(self):
        """ Test if report raises error when invalid after sanitize. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.InvalidValue):
            report.add('feed.name', u'\r\n', sanitize=True)

    def test_report_update(self):
        """ Test report value update function. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example 1')
        report.update('feed.name', 'Example 2')
        self.assertEqual('Example 2', report['feed.name'])

    def test_report_contains(self):
        """ Test report value contains function. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example 1')
        self.assertTrue(report.contains('feed.name'))

    def test_report_update_duplicate(self):
        """ Test report value update function, rejects duplicate. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        with self.assertRaises(exceptions.KeyNotExists):
            report.update('feed.name', 'Example')

    def test_factory_serialize(self):
        """ Test MessageFactory serialize method. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report.add('feed.name', 'Example')
        report.add('feed.url', URL_SANE)
        report.add('raw', LOREM_BASE64)
        self.assertEqual('{"raw": "bG9yZW0gaXBzdW0=", "__type": "Report",'
                         ' "feed.url": "https://example.com/", "feed.name":'
                         ' "Example"}',
                         message.MessageFactory.serialize(report))

    def test_report_unicode(self):  # TODO: Python 3
        """ Test Message __unicode__ function, pointing to serialize. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertEqual(report.serialize(),
                         unicode(report))

    def test_deep_copy_content(self):
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertListEqual(list(report.deep_copy().items()),
                             list(report.items()))

    def test_deep_copy_items(self):  # TODO: Sort by key
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertNotEqual(list(map(id, report.deep_copy())),
                            list(map(id, report)))

    def test_deep_copy_object(self):
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertIsNot(report.deep_copy(), report)

    def test_copy_content(self):
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertListEqual(list(report.copy().items()),
                             list(report.items()))

    def test_copy_items(self):  # TODO: Sort by key
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertListEqual(list(map(id, report.copy())),
                             list(map(id, report)))

    def test_copy_object(self):
        """ Test if depp_copy does not return the same object. """
        report = message.MessageFactory.unserialize('{"__type": "Report"}')
        report = self.add_report_examples(report)
        self.assertIsNot(report.copy(), report)

    def test_event_hash(self):
        """ Test Event __hash_,_ 'time.observation should be ignored. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event = self.add_event_examples(event)
        self.assertEqual(-6908124890214948902, hash(event))

    def test_event_dict(self):
        """ Test Event to_dict. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event = self.add_event_examples(event)
        self.assertDictEqual({'feed': {'name': 'Example',
                                       'url': 'https://example.com/'},
                              'raw': 'bG9yZW0gaXBzdW0=',
                              'time': {'observation': '2015-01-01T13:37:00+'
                                                      '00:00'}},
                             event.to_dict())

    def test_event_json(self):
        """ Test Event to_json. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        event = self.add_event_examples(event)
        self.assertEqual('{"feed": {"url": "https://example.com/", "name": '
                         '"Example"}, "raw": "bG9yZW0gaXBzdW0=", "time": '
                         '{"observation": "2015-01-01T13:37:00+00:00"}}',
                         event.to_json())

    def test_event_serialize(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

    def test_event_string(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual(b'{"__type": "Event"}',
                         event.serialize())

    def test_event_unicode(self):
        """ Test Event serialize. """
        event = message.MessageFactory.unserialize('{"__type": "Event"}')
        self.assertEqual('{"__type": "Event"}',
                         event.serialize())

if __name__ == '__main__':
    unittest.main()

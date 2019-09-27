#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unittest
import time
from easytimeout import Timeout, TimeoutError


class TestTimeout(unittest.TestCase):
    @staticmethod
    @Timeout(limit=5)
    def __test_nottimeout__(*args, **kwargs):
        return 'not timeout'

    def test_nottimeout(self):
        self.assertEqual('not timeout', self.__test_nottimeout__())

    @Timeout(limit=3)
    def __test_timeout_without_result__(self, *args, **kwargs):
        time.sleep(4)
        return 'timeout'

    def test_timeout_without_result(self):
        with self.assertRaises(TimeoutError):
            self.__test_timeout_without_result__()

    @Timeout(limit=3, timeout_result='timeout with not callable result')
    def __test_timeout_with_not_callable_result_(self, *args, **kwargs):
        time.sleep(4)
        return 'timeout'

    def test_timeout_with_not_callable_result(self):
        self.assertEqual('timeout with not callable result', self.__test_timeout_with_not_callable_result_())

    @Timeout(limit=3, timeout_result=lambda ins, *args, **kwargs: 'time out with callable result, args: {0}, kwargs: {1}'.format(args, kwargs))
    def __test_timeout_with_callable_result_(self, *args, **kwargs):
        time.sleep(4)
        return 'timeout'

    def test_timeout_with_callable_result(self):
        self.assertEqual(
            'time out with callable result, args: (3, 4), kwargs: {\'args1\': 5, \'args2\': 6}',
            self.__test_timeout_with_callable_result_(3, 4, args1=5, args2=6)
        )

    @Timeout(limit=3)
    def __test_raise_exception__(self, *args, **kwargs):
        raise Exception('test exception')

    def test_raise_exception(self):
        with self.assertRaisesRegexp(Exception, 'test exception'):
            self.__test_raise_exception__()


if __name__ == "__main__":
    unittest.main()


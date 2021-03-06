from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from caffe2.python import core, workspace
from caffe2.python.test_util import TestCase


class TestCounterOps(TestCase):
    def test_counter_ops(self):
        workspace.RunOperatorOnce(core.CreateOperator(
            'CreateCounter', [], ['c'], init_count=1))
        workspace.RunOperatorOnce(core.CreateOperator(
            'CountDown', ['c'], ['t1']))  # 1 -> 0
        assert not workspace.FetchBlob('t1')

        workspace.RunOperatorOnce(core.CreateOperator(
            'CountDown', ['c'], ['t2']))  # 0 -> 0
        assert workspace.FetchBlob('t2')

        workspace.RunOperatorOnce(core.CreateOperator(
            'ResetCounter', ['c'], [], init_count=1))  # -> 1
        workspace.RunOperatorOnce(core.CreateOperator(
            'CountDown', ['c'], ['t3']))  # 1 -> 0
        assert not workspace.FetchBlob('t3')

        workspace.RunOperatorOnce(core.CreateOperator(
            'ConstantBoolFill', [], ['t4'], value=0.0, shape=[]))
        assert workspace.FetchBlob('t4') == workspace.FetchBlob('t1')

        workspace.RunOperatorOnce(core.CreateOperator(
            'ConstantBoolFill', [], ['t5'], value=1.0, shape=[]))
        assert workspace.FetchBlob('t5') == workspace.FetchBlob('t2')

        assert workspace.RunOperatorOnce(core.CreateOperator(
            'And', ['t1', 't2'], ['t6']))
        assert not workspace.FetchBlob('t6')  # True && False

        assert workspace.RunOperatorOnce(core.CreateOperator(
            'And', ['t2', 't5'], ['t7']))
        assert workspace.FetchBlob('t7')  # True && True

import unittest
import sys, os, re
import forcebalance.objective
import forcebalance.target
import forcebalance
import abc
from __init__ import ForceBalanceTestCase

class TestImplemented(ForceBalanceTestCase):
    def test_implemented_targets_derived_from_target(self):
        for key in forcebalance.objective.Implemented_Targets.iterkeys():
            self.assertTrue(issubclass(forcebalance.objective.Implemented_Targets[key],forcebalance.target.Target))
    
    def test_no_unlisted_classes_derived_from_Target(self):
        """Check for classes derived from Target that are not listed in Implemented_Targets"""
        forcebalance_modules=[module[:-3] for module in os.listdir(forcebalance.__path__[0])
                     if re.compile(".*\.py$").match(module)
                     and module not in ["__init__.py"]]
        for module in forcebalance_modules:
            m = __import__('forcebalance.' + module)
            objects = dir(eval('m.' + module))
            for object in objects:
                object = eval('m.'+module+'.'+object)
                if type(object) == abc.ABCMeta:
                    implemented = [i for i in forcebalance.objective.Implemented_Targets.itervalues()]
                    # list of documented exceptions
                    exclude = ['Target',
                               'AbInitio',
                               'Interaction',
                               'Interaction_GMX',
                               'Liquid',
                               'BindingEnergy',
                               'LeastSquares',
                               'Vibration',
                               'Moments']
                    if object not in implemented and object.__name__ not in exclude:
                        self.fail("Found unlisted class '%s'" % object.__name__)

if __name__ == '__main__':           
    unittest.main()
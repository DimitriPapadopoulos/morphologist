import unittest

from morphologist.tests.test_study import TestStudy
from morphologist.tests.test_analysis import TestAnalysis

from morphologist.tests.test_intra_analysis import TestIntraAnalysis
from morphologist.tests.test_intra_analysis_study import TestBrainvisaTemplateStudy, TestDefaultTemplateStudy

if __name__=='__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStudy)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAnalysis))

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBrainvisaTemplateStudy))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDefaultTemplateStudy))

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntraAnalysis))

    unittest.TextTestRunner(verbosity=2).run(suite)



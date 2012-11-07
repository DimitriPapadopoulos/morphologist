import os
import unittest

from morphologist.steps import SpatialNormalization, BiasCorrection, HistogramAnalysis, BrainSegmentation, SplitBrain


class TestIntraAnalysisSteps(unittest.TestCase):

    def setUp(self):
        
        subject = "icbm101T"
        base_directory = "/volatile/laguitton/data/icbm/icbm/%s/t1mri/default_acquisition" % subject
  
        self.mri = os.path.join(base_directory, 
                                "%s.ima" % subject)
        self.commissure_coordinates = os.path.join(base_directory, 
                                      "%s.APC" % subject) 
        self.talairach_transform = os.path.join(base_directory, 
                                   "registration/RawT1-%s_default_acquisition_TO_Talairach-MNI.trm" % subject)
        self.hfiltered = os.path.join(base_directory, 
                         "default_analysis/hfiltered_%s.ima" % subject)
        self.white_ridges = os.path.join(base_directory, 
                            "default_analysis/whiteridge_%s.ima" % subject)
        self.edges = os.path.join(base_directory, 
                     "default_analysis/edges_%s.ima" % subject)
        self.mri_corrected = os.path.join(base_directory, 
                             "default_analysis/nobias_%s.ima" % subject)
        self.variance = os.path.join(base_directory, 
                        "default_analysis/variance_%s.ima" % subject)
        self.histo_analysis = os.path.join(base_directory, 
                              "default_analysis/nobias_%s.han" % subject)
        self.brain_mask = os.path.join(base_directory, 
                          "default_analysis/segmentation/brain_%s.ima" % subject)
        self.split_mask = os.path.join(base_directory, 
                          "default_analysis/segmentation/voronoi_%s.ima" % subject)

    def test_spatial_normalization(self):
        spatial_normalization = SpatialNormalization()

        spatial_normalization.mri = self.mri

        spatial_normalization.commissure_coordinates = self.commissure_coordinates
        spatial_normalization.talairach_transform = self.talairach_transform

        self.assert_(spatial_normalization.run() == 0)


    def test_bias_correction(self):
        bias_correction = BiasCorrection()

        bias_correction.mri = self.mri 
        bias_correction.commissure_coordinates = self.commissure_coordinates 

        bias_correction.hfiltered = self.hfiltered 
        bias_correction.white_ridges = self.white_ridges
        bias_correction.edges = self.edges 
        bias_correction.variance = self.variance 
        bias_correction.mri_corrected = self.mri_corrected 

        self.assert_(bias_correction.run() == 0)
    

    def test_histogram_analysis(self):
        histo_analysis = HistogramAnalysis()
        
        histo_analysis.mri_corrected = self.mri_corrected 
        histo_analysis.white_ridges = self.white_ridges 
        histo_analysis.hfiltered = self.hfiltered 

        histo_analysis.histo_analysis = self.histo_analysis
    
        self.assert_(histo_analysis.run() == 0)
    
    
    def test_brain_segmentation(self):
        brain_segmentation = BrainSegmentation()
    
        brain_segmentation.mri_corrected = self.mri_corrected
        brain_segmentation.commissure_coordinates = self.commissure_coordinates
        brain_segmentation.white_ridges = self.white_ridges
        brain_segmentation.edges = self.edges 
        brain_segmentation.variance = self.variance
        brain_segmentation.histo_analysis = self.histo_analysis

        brain_segmentation.brain_mask = self.brain_mask
    
        self.assert_(brain_segmentation.run() == 0)


    def test_split_brain(self):
        split_brain = SplitBrain()

        split_brain.mri_corrected = self.mri_corrected
        split_brain.brain_mask = self.brain_mask
        split_brain.white_ridges = self.white_ridges
        split_brain.histo_analysis = self.histo_analysis
        split_brain.commissure_coordinates = self.commissure_coordinates

        split_brain.split_mask = self.split_mask

        self.assert_(split_brain.run() == 0)


if __name__ == '__main__':

    unittest.main()

    #tests = []
    #tests.append('test_spatial_normalization')
    ##tests.append('test_bias_correction')
    ##tests.append('test_histogram_analysis')
    ##tests.append('test_brain_segmentation')
    ##tests.append('test_split_brain')

    #test_suite = unittest.TestSuite(map(TestIntraAnalysisSteps, tests))
    #unittest.TextTestRunner(verbosity=2).run(test_suite)

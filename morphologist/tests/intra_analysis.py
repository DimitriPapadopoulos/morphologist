import os
import getpass
import shutil

from morphologist.tests.mocks.intra_analysis import MockIntraAnalysis
from morphologist.intra_analysis import BrainvisaIntraAnalysisParameterTemplate 
from morphologist.intra_analysis import IntraAnalysis
from morphologist.tests.analysis import AnalysisTestCase


class IntraAnalysisTestCase(AnalysisTestCase):

    def __init__(self):
        super(IntraAnalysisTestCase, self).__init__()

    def create_analysis(self):
        self.analysis = IntraAnalysis()
        return self.analysis

    def analysis_cls(self):
        return IntraAnalysis

    def set_analysis_parameters(self):
        subject = "hyperion"
        outputdir = os.path.join('/neurospin', 'lnao', 'Panabase', 
                                      'cati-dev-prod', 'morphologist', 
                                      'output_dirs', getpass.getuser(), 
                                      IntraAnalysis.BRAINVISA_PARAM_TEMPLATE)
        print outputdir
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)
        os.makedirs(outputdir) # always starts with a clean state

        image_path = os.path.join('/neurospin', 'lnao', 'Panabase', 
                                'cati-dev-prod', 'morphologist', 'raw_irm', subject + ".nii")
         

        self.analysis.set_parameters(IntraAnalysis.BRAINVISA_PARAM_TEMPLATE,
                                     name="hyperion",
                                     image=image_path,
                                     outputdir=outputdir) 
        IntraAnalysis.create_outputdirs(IntraAnalysis.BRAINVISA_PARAM_TEMPLATE,
                                        subject,
                                        outputdir)
        self.analysis.clear_output_files() 
        

    def delete_some_parameter_values(self):
        self.analysis.output_params.edges = None
        self.analysis.input_params.mri = None


    def delete_some_input_files(self):
        parameter_names = ['mri']
        for name in parameter_names:
            file_name = self.analysis.input_params.get_value(name)
            os.rename(file_name, file_name + "hide_for_test") 


    def create_some_output_files(self):
        parameter_names = ['split_mask', 'variance']
        for name in parameter_names:
            file_name = self.analysis.output_params.get_value(name)
            f = open(file_name, "w")
            f.write("something\n")
            f.close() 


    def get_wrong_parameter_name(self):
        return "toto"

    def restore_input_files(self):
        parameter_names = ['mri']
        for name in parameter_names:
            file_name = self.analysis.input_params.get_value(name)
            if file_name != None and os.path.isfile(file_name + "hide_for_test"):
                os.rename(file_name + "hide_for_test", file_name) 


class MockIntraAnalysisTestCase(IntraAnalysisTestCase):

    def __init__(self):
        super(MockIntraAnalysisTestCase, self).__init__()

    def create_analysis(self):
        self.analysis = MockIntraAnalysis()
        return self.analysis

    def analysis_cls(self):
        return MockIntraAnalysis

    def set_analysis_parameters(self):
        subject = "icbm100T"
        outputdir = "/volatile/laguitton/data/icbm/icbm/"
        image_path = os.path.join(outputdir, 
                             subject, 
                             "t1mri", 
                             "default_acquisition",
                             "%s.ima" % subject) 

        input_params =  BrainvisaIntraAnalysisParameterTemplate.get_input_params(subject, 
                                                                                 image_path)
        output_params = BrainvisaIntraAnalysisParameterTemplate.get_output_params(subject, 
                                                                         "/tmp/output_study")
        self.analysis.input_params = input_params 
        self.analysis.output_params = output_params
        IntraAnalysis.create_outputdirs(IntraAnalysis.BRAINVISA_PARAM_TEMPLATE,
                                        subject,
                                        outputdir)
        self.analysis.clear_output_files() 

 

#!/usr/local/bin/python2.7
##
# OOIPLACEHOLDER
#
# Copyright 2014 Raytheon Co.
##
__author__ = 'dmergens'

import sys

from mi.core.log import get_logger
from mi.dataset.dataset_driver import DataSetDriver
from mi.dataset.parser.glider import GliderParser


class ParadMDriver:

    def __init__(self, base_python_code_path, source_file_path, particle_data_handler_object, config):
        
        self._basePythonCodePath = base_python_code_path
        self._sourceFilePath = source_file_path
        self._particleDataHdlrObj = particle_data_handler_object
        self._config = config

    def process(self):
    
        log = get_logger()

        with open(self._sourceFilePath, 'rb') as file_handle:

            def exception_callback(exception):
                log.debug('Exception: %s', exception)
                self._particleDataHdlrObj.setParticleDataCaptureFailure()

            parser = GliderParser(self._config,
                                  None,
                                  file_handle,
                                  lambda state, ingested: None,
                                  lambda data: None,
                                  exception_callback)

            driver = DataSetDriver(parser, self._particleDataHdlrObj)

            driver.processFileStream()

        return self._particleDataHdlrObj
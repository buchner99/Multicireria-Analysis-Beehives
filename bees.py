"""
Model exported as python.
Name : model_multicriteria
Group : 
With QGIS : 31612
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Model_multicriteria(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('disruption', 'disruption', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('dresdenborder', 'dresden_border', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hoehenmodell', 'hoehenmodell', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('osm', 'food', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('water', 'water', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('windbreak', 'windbreak', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Raster_calculator', 'raster_calculator', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(28, model_feedback)
        results = {}
        outputs = {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['disruption'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # dresden
        alg_params = {
            'INPUT': parameters['dresdenborder'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dresden'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['water'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['windbreak'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # water
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'MASK': outputs['Dresden']['OUTPUT'],
            'OPTIONS': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Water'] = processing.run('gdal:clipvectorbypolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hoehenmodell'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['osm'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # dem
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': outputs['Dresden']['OUTPUT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': None,
            'TARGET_CRS': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dem'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Slope
        alg_params = {
            'INPUT': outputs['Dem']['OUTPUT'],
            'Z_FACTOR': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Slope'] = processing.run('native:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # disruption
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'MASK': outputs['Dresden']['OUTPUT'],
            'OPTIONS': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Disruption'] = processing.run('gdal:clipvectorbypolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 1,
            'EXTENT': outputs['Dem']['OUTPUT'],
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 76.809356,
            'INIT': None,
            'INPUT': outputs['Disruption']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 76.809356,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Proximity (raster distance)
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,
            'EXTRA': '',
            'INPUT': outputs['RasterizeVectorToRaster']['OUTPUT'],
            'MAX_DISTANCE': 0,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,
            'VALUES': '1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximityRasterDistance'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # food
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'MASK': outputs['Dresden']['OUTPUT'],
            'OPTIONS': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Food'] = processing.run('gdal:clipvectorbypolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,
            'EXTENT': outputs['Dem']['OUTPUT'],
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 76.809356,
            'INIT': None,
            'INPUT': outputs['Water']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 76.809356,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['Slope']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [0,7,1,8,15,2,16,23,3,24,31,4,32,39,5,40,47,6,48,55,7,56,63,8,64,71,9,72,79,10,80,87,11,88,90,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['ProximityRasterDistance']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [0,200,1,201,400,2,401,600,3,601,800,4,801,1000,5,1001,1200,6,1201,1400,7,1401,1600,8,1601,1800,9,1801,2000,10,2001,4000,11,4001,10587,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,
            'EXTENT': outputs['Dem']['OUTPUT'],
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 76.809356,
            'INIT': None,
            'INPUT': outputs['Food']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 76.809356,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # windbreak
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'MASK': outputs['Dresden']['OUTPUT'],
            'OPTIONS': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Windbreak'] = processing.run('gdal:clipvectorbypolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Proximity (raster distance)
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,
            'EXTRA': '',
            'INPUT': outputs['RasterizeVectorToRaster']['OUTPUT'],
            'MAX_DISTANCE': 0,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,
            'VALUES': '1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximityRasterDistance'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Aspect
        alg_params = {
            'INPUT': outputs['Dem']['OUTPUT'],
            'Z_FACTOR': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Aspect'] = processing.run('native:aspect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['Aspect']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [361,135,1,0,30,2,331,360,3,31,60,4,301,330,5,61,90,6,271,300,7,91,120,8,241,270,9,121,150,10,211,240,11,151,180,12,181,210,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Proximity (raster distance)
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,
            'EXTRA': '',
            'INPUT': outputs['RasterizeVectorToRaster']['OUTPUT'],
            'MAX_DISTANCE': 0,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,
            'VALUES': '1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximityRasterDistance'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['ProximityRasterDistance']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [4001,9577,1,2001,4000,2,1801,2000,3,1601,1800,4,1401,1600,5,1201,1400,6,1001,1200,7,801,1000,8,601,800,9,401,600,10,201,400,11,0,200,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 1,
            'DATA_TYPE': 5,
            'EXTENT': outputs['Dem']['OUTPUT'],
            'EXTRA': '',
            'FIELD': '',
            'HEIGHT': 76.809356,
            'INIT': None,
            'INPUT': outputs['Windbreak']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 76.809356,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['ProximityRasterDistance']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [4001,9241,1,2001,4000,2,1801,2000,3,1601,1800,4,1401,1600,5,1201,1400,6,1001,1200,7,801,1000,8,601,800,9,401,600,10,201,400,11,0,200,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Proximity (raster distance)
        alg_params = {
            'BAND': 1,
            'DATA_TYPE': 5,
            'EXTRA': '',
            'INPUT': outputs['RasterizeVectorToRaster']['OUTPUT'],
            'MAX_DISTANCE': 0,
            'NODATA': 0,
            'OPTIONS': '',
            'REPLACE': 0,
            'UNITS': 0,
            'VALUES': '1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ProximityRasterDistance'] = processing.run('gdal:proximity', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Reclassify by table
        alg_params = {
            'DATA_TYPE': 5,
            'INPUT_RASTER': outputs['ProximityRasterDistance']['OUTPUT'],
            'NODATA_FOR_MISSING': False,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 0,
            'RASTER_BAND': 1,
            'TABLE': [4001,9391,1,2001,4000,2,1801,2000,3,1601,1800,4,1401,1600,5,1201,1400,6,1001,1200,7,801,1000,8,601,800,9,401,600,10,201,400,11,0,200,12],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReclassifyByTable'] = processing.run('native:reclassifybytable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': 1,
            'BAND_D': 1,
            'BAND_E': 1,
            'BAND_F': 1,
            'EXTRA': '',
            'FORMULA': '(A*1)+(B*1)+(C*1)+(D*1)+(E*1)+(F*1)',
            'INPUT_A': outputs['ReclassifyByTable']['OUTPUT'],
            'INPUT_B': outputs['ReclassifyByTable']['OUTPUT'],
            'INPUT_C': outputs['ReclassifyByTable']['OUTPUT'],
            'INPUT_D': outputs['ReclassifyByTable']['OUTPUT'],
            'INPUT_E': outputs['ReclassifyByTable']['OUTPUT'],
            'INPUT_F': outputs['ReclassifyByTable']['OUTPUT'],
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 1,
            'OUTPUT': parameters['Raster_calculator']
        }
        outputs['RasterCalculator'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Raster_calculator'] = outputs['RasterCalculator']['OUTPUT']
        return results

    def name(self):
        return 'model_multicriteria'

    def displayName(self):
        return 'model_multicriteria'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model_multicriteria()

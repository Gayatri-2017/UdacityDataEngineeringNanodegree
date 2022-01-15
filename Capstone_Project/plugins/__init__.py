# from __future__ import division, absolute_import, print_function

# import plugins.operators
import plugins.helpers

# Defining the plugin class
class UdacityPlugin():
    helpers = [
        helpers.SqlQueries,
        helpers.RedshiftHelper,
        helpers.PositionStack,
        helpers.GoogleAPI
    ]
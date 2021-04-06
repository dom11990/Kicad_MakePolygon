import traceback

try:    
    from .Polygonize_action import PolygonizePluginAction
    PolygonizePluginAction().register()
except Exception as e:
    print(traceback.format_exc())
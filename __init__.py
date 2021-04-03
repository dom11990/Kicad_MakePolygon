try:    
    import PolygonizePlugin
    PolygonizePlugin.PolygonizePlugin().register()
except Exception as e:
    print(e)

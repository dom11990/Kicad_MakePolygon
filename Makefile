ui : PolygonizeDialog.ui ExportFootprintDialog.ui
	pyuic5 -x PolygonizeDialog.ui -o PolygonizeDialog.py
	pyuic5 -x ExportFootprintDialog.ui -o ExportFootprintDialog.py

clean:
	rm -f PolygonizeDialog.py ExportFootprintDialog.py
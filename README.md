1. https://github.com/kohlik-blip/solar-system-analysis
2. There is no live app
3. An interactive solar-system explorer. A Flask API calculates each planet's density, surface gravity, and escape velocity from its mass and radius, then serves them as JSON to a page with a planet picker, sortable comparison table, and a finding on whether distance from the Sun predicts temperature (Venus breaks the trend).
4. Not applicable, the API is read-only, so all endpoints are GET.
5. None. The planetary data is hard-coded in planets_data.py, and everything else is computed on demand. 
6. pip install flask, then python app.py serves both the API and page at http://127.0.0.1:5000/. Planet photos need internet. Opening index.html alone also works, using an embedded snapshot of the analysis output.
7. API endpoints, the page, and analysis.py were all tested. Planet images need internet. Everything is working.
8. Data from NASA planetary fact sheets; images from Wikimedia Commons. Tools: Flask, HTML, CSS, and JavaScript.

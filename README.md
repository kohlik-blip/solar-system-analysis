This project is about data on planets in the solar system.

Solar System Analysis is a small Python project that turns raw planetary data into interpreted results instead of just displaying looked-up facts. A data module stores NASA fact-sheet measurements (mass, radius, distance from the Sun, temperature, orbital period, moons) for the eight planets, and an analysis layer computes real physics from them eg. density, surface gravity, and escape velocity are all calculated from each planet's mass and radius.

Planets are classified as terrestrial, ice giant, or gas giant, and a Pearson correlation tests whether distance from the Sun predicts temperature, flagging Venus as the trend-breaker (hotter than Mercury despite being farther out, thanks to its thick CO₂ atmosphere). 

A thin Flask API serves these results as JSON...per-planet lookups, rankings, summary statistics, and side-by-side comparisons

It has an nteractive web page with a planet picker, a sortable table that highlights the calculated columns, 

It has a dark mode, built in plain JavaScript with no frameworks. 

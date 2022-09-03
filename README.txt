This repository contains python programs to simulate planetary motion.

Currently the code is configured to shift into the "centre-of-mass" frame, and is optimised for simulating two-body systems.

INPUT PARAMETERS:

 - The timestep for the simulation should be set to 43200 seconds (i.e 12 hours or half a day).

 - "bodiesEarthMoon.txt" should be selected to simulate the motion of the Earth - Moon system.

 - "bodiesSplitEarth.txt" is an experiment in simulating the rotational motion of the Earth itself. It is advised not to select this file as the code needs further refinement to accomodate the smaller-distance scale involved.

 - "bodiesMarsPhobos.txt" should be selected to simulate the motion of the Mars - Phobos system.

 - "bodiesInnerSolarSystem.txt" should be selected to simulate the inner 4 planets of the solar system (the "Terrestrial Planets").

OUTPUT:

 - An animation of the motion will be produced

 - Energies are written to a text file for processing.

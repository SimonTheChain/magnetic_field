.. Magnetic Field Model documentation master file, created by
   sphinx-quickstart on Thu Mar 23 17:48:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Magnetic Field Model's documentation!
================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Predicting the intensity of the magnetic field experienced by satellites in Earth orbit
=======================================================================================

Objective
=========
To determine if the magnetic field experienced by satellites can be predicted from their altitude from Earth.


Hypothesis
==========
We can reasonably assume that the magnetic field will be less intense as the altitude increases.  However, because the Earth's geomagnetic field is not perfectly spherical but instead in the shape of a dipole, with anomalies and distortions from the pressure of the interplanetary magnetic field, the relationship between these two attributes might not be easily modeled.

Dataset
=======
MOST-268_HD209458_2014-268_HD209458_2014

A .tar file containing .fits files compressed as .tar files.

This dataset is available online: https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?Plane.position.bounds@Shape1Resolver.value=ALL&Observation.collection=MOST&Observation.instrument.name=Direct%20image&Observation.type=object#sortCol=caom2%3APlane.time.bounds.lower&sortDir=dsc&col_1=_checkbox_selector;;;&col_2=caom2%3AObservation.uri;;;&col_3=caom2%3APlane.productID;;;&col_4=caom2%3AObservation.target.name;;;&col_5=caom2%3APlane.position.bounds.cval1;;;&col_6=caom2%3APlane.position.bounds.cval2;;;&col_7=caom2%3APlane.time.bounds.lower;;;&col_8=caom2%3AObservation.instrument.name;;;&col_9=caom2%3APlane.time.exposure;;;&col_10=caom2%3AObservation.proposal.pi;;;&col_11=caom2%3AObservation.proposal.id;;;&col_12=caom2%3APlane.calibrationLevel;;;&col_13=caom2%3AObservation.observationID;;;

The data was recorded by the MOST satellite: http://www.asc-csa.gc.ca/fra/satellites/most/default.asp
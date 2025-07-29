
======
Atlite
======

|zenodo atlite-pc|

atlite-pc: atlite with added Photocatalysis (PC) Module

atlite-pc: is fork of the `atlite repository from PyPSA <https://github.com/PyPSA/atlite>`_  with added photocatalysis (PC) for hydrogen production.
It can be used especially in combination with the `customized PyPSA-Eur-PC model that includes photocatalytic hydrogen production in PyPSA-eur <https://github.com/w-tusche/pypsa-eur-pc>`_.

It diverges from the main branch of atlite shortly after atlite v0.2.12 with the last common commit: 195bc796 (06.05.2024)
The customized version atlite-pc is on the branch with the same name (default branch). The main project of atlite is in the main branch of this repository.

The model extension in this fork was done with contributions from:

* Wolfram Tuschewitzki
* Jelto Lange
* Leander Raudszus


More info under:

* For the original atlite documentation and installation please check `here <https://atlite.readthedocs.io/en/latest>`_.
* Major contributing authors can be found in the `AUTHORES.rst of atlite <https://github.com/PyPSA/atlite/blob/master/AUTHORS.rst>`_.
* To cite the original atlite please refer to the `CITATION.cff of atlite <https://github.com/PyPSA/atlite/blob/master/CITATION.cff>`_.

Related content to atlite-pc:

* `PyPSA-Eur-PC <https://github.com/w-tusche/pypsa-eur-pc>`_
* Analysis and plotting code for paper "Impacts of photocatalytic hydrogen production on the European energy system": `photocatalysis-europe <https://github.com/w-tusche/photocatalysis-europe.git>`_
* `Raw data of PC-0 and PC-50 cases for paper: Impacts of photocatalytic hydrogen production on the European energy system <https://doi.org/10.5281/zenodo.16360844>`_

Authors and Copyright
---------------------

Copyright (C) 2016 - 2025 The Atlite Authors.

See the original atlite `AUTHORES.rst <https://github.com/PyPSA/atlite/blob/master/AUTHORS.rst>`_ for details.

Licence
======================

This work is licensed under multiple licences:

-  All original source code is licensed under `MIT`_
-  Auxiliary code from SPHINX is licensed under `BSD-2-Clause`_.
-  The documentation is licensed under `CC-BY-4.0`_.
-  Configuration and data files are mostly licensed under `CC0-1.0`_.

See the individual files for license details.

.. _free software: http://www.gnu.org/philosophy/free-sw.en.html
.. _xarray: http://xarray.pydata.org/en/stable/

.. _conda-forge: https://anaconda.org/conda-forge/atlite
.. _pypi: https://pypi.org/project/atlite/%3E
.. _GitHub: https://github.com/pypsa/atlite

.. _MIT: LICENSES/MIT.txt
.. _BSD-2-Clause: LICENSES/BSD-2-Clause.txt
.. _CC-BY-4.0: LICENSES/CC-BY-4.0.txt
.. _CC0-1.0: LICENSES/CC0-1.0.txt


.. |zenodo atlite-pc| image:: https://zenodo.org/badge/1021476497.svg
    :target: https://doi.org/10.5281/zenodo.16566337

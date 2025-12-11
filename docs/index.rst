.. METIS Reaction Lights BLE Protocol Documentation
.. =================================================

.. *********************************************************************************
.. DISCLAIMER
.. *********************************************************************************

.. attention::
   **DISCLAIMER**

   This documentation is the result of **Reverse Engineering** of the Bluetooth Low Energy (BLE) protocol used by METIS Reaction Lights devices. It is intended strictly for **educational, analytical, and experimental purposes**.

   The author(s) of this documentation and the associated code are **not affiliated with, endorsed by, or sponsored by METIS** or its parent companies. Use of this information may violate the terms of service or warranty agreements of the original manufacturer. Proceed at your own risk.

METIS Reaction Lights: BLE Protocol Analysis
============================================

Welcome to the documentation for the reverse-engineered METIS Reaction Lights BLE Protocol.

The goal of this project is to fully document the Attribute Protocol (ATT) commands, Service UUIDs, and Characteristics necessary to communicate directly with the devices, enabling custom integration and independent application development beyond the official software.

Device Overview
---------------

The METIS Reaction Lights are portable, sensor-equipped training devices utilized primarily in sports performance and neuro-training contexts. They communicate wirelessly to coordinate drills involving light activation and touch/proximity detection.

This documentation will dissect the communication layers, focusing specifically on how the device handles:

* **Initial Discovery and Paring** (GAP)
* **Service and Characteristic Mapping** (GATT)
* **Command Encoding** (ATT Protocol)
* **Event Reporting** (Touch/Proximity Events, Status Updates)

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Documentation Sections

   hardware
   ble_protocol
   att_analysis
   tools
   implementation

Support and Contribution
------------------------

This is an open-source analytical effort. Contributions, corrections, and new findings are highly welcome!

Please refer to the :doc:`tools` section for information on how the data was captured and analyzed.

* `GitHub Repository <URL_DEL_TUO_REPO_QUI>`_
* `Report an Issue <URL_PER_SEGNALARE_UN_PROBLEMA>`_

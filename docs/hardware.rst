.. _hardware:

Hardware Architecture and Physical Details
==========================================

This chapter provides a contextual overview of the physical components and high-level architecture of the METIS Reaction Lights system. Understanding the device's hardware constraints and operational principles is crucial for interpreting the subsequent analysis of the BLE (Bluetooth Low Energy) protocol.

Physical Description
--------------------

The METIS Reaction Lights are robust, modular training pods designed for dynamic environments. Each unit functions as an independent node within a coordinated network.

Key physical features relevant to the protocol analysis include:

* **Modular Design:** Devices are designed to be freely placed and require dynamic network management.
* **Sensor Integration:** The core functionality relies on rapid and accurate detection via an integrated proximity/touch sensor.
* **Visual Feedback:** High-intensity RGB LEDs serve as the primary output, controlled directly via the BLE protocol.


.. toctree::
   :maxdepth: 1
   :caption: Hardware Content

   hardware_components
   network_flip_principle
   operational_status

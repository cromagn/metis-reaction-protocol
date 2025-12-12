.. _ble-protocol:

Bluetooth Low Energy (BLE) Protocol Analysis
=============================================

This chapter details the findings related to the Bluetooth Low Energy communication stack, moving from the low-level identification (GAP) to the high-level data structure (GATT) that governs command and event exchange.

1. Generic Access Profile (GAP) Analysis
----------------------------------------

The GAP defines how BLE devices make themselves available to be connected. Our analysis confirms the following identification patterns:

1.1. Device Naming and Identification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The devices broadcast their presence using standard **SCAN_RSP** (Scan Response) packets.

* **Identifiable Name:** All devices use a common prefix followed by a unique identifier.
    * **Pattern:** ``$react-X-`` (where X is a number, usually 1, 2, 3, etc.).
    * **Example Observed:** ``$react-1-`` and ``$react-2-``
    * **Purpose:** This naming convention simplifies the initial identification and selection process within the official mobile application.

1.2. MAC Addresses and Public Addressing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MAC addresses observed in the SCAN_RSP packets appear to be **Public Addresses** (non-randomized), which simplifies connection attempts, as the address remains static.

* **Example Address Observed (Device 1):** ``cc:03:01:ea:28:91``
* **Manufacturer:** The initial bytes of the MAC address (OUI) should be noted for verification of the hardware vendor.

1.3. The 'Flip' Principle in GAP Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As discussed in the :ref:`hardware-details` section, the METIS system uses a dynamic network. In the context of GAP, this means:

* All devices advertise initially, but the host application selects one device (e.g., ``$react-1-``) to initiate the **Central Role connection**.
* This first connected device (the **Controller**) then becomes responsible for establishing the proprietary mesh/network with the other **Node** devices.
* **Implication for Sniffing:** Only the **Controller** device maintains a direct, high-level GATT connection to the host application (phone/PC). The other devices communicate with the Controller using lower-level, non-GATT protocols or secondary advertising channels.

.. _ble-protocol:

Bluetooth Low Energy (BLE) Protocol Analysis
=============================================

This chapter details the findings related to the Bluetooth Low Energy communication stack, moving from the low-level identification (GAP) to the high-level data structure (GATT) that governs command and event exchange.

1. Generic Access Profile (GAP) Analysis
----------------------------------------

The Generic Access Profile (GAP) defines how the METIS Reaction Lights make themselves available for connection. Our analysis, performed using a BLE sniffer and Wireshark, confirms the following identification patterns during the advertising phase.

1.1. Device Naming and Identification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The devices broadcast their presence using standard **SCAN_RSP** (Scan Response) packets.

* **Identifiable Name:** All devices use a common prefix followed by a unique, numeric identifier, observed in the local name field (0x09) of the advertising payload.
    * **Pattern:** ``$react-X-`` (where X is the sequential device number).
    * **Examples Observed:** ``$react-1-`` and ``$react-2-``
    * **Purpose:** This consistent naming convention simplifies the initial identification and selection process within the official mobile application.

1.2. MAC Addresses and Public Addressing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MAC addresses observed in the SCAN_RSP packets appear to be **Public Addresses** (non-randomized), which suggests that the address remains static for each device and simplifies persistent connection attempts. 

* **MAC Addresses Observed:**
    * **Device $react-1- (Example):** ``7e:ad:07:91:53:e6``
    * **Device $react-2- (Example):** ``69:de:d6:c7:4c:71``
* **Manufacturer Identification:** The initial bytes of the MAC addresses (the Organizationally Unique Identifier - OUI) should be cross-referenced with the Bluetooth SIG database. This data can provide hints regarding the underlying BLE chip vendor (e.g., Nordic Semiconductor, Texas Instruments, etc.), which may suggest the type of BLE stack in use.

1.3. The 'Flip' Principle in GAP Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As discussed in the :ref:`hardware-details` section, the METIS system uses a dynamic network architecture. In the context of GAP, this implies:

* **Initial State:** All devices advertise initially.
* **Controller Selection:** The host application (phone/PC) selects one device (e.g., the device with MAC ``7e:ad:07:91:53:e6``) to initiate the **Central Role connection**. This first device becomes the **Controller** (Master).
* **Node Communication:** The remaining devices (the **Nodes**) do not maintain a direct GATT connection to the host. They communicate with the Controller using proprietary, lower-level, or mesh-like BLE protocols.
* **Implication for Sniffing:** To capture all proprietary commands, the sniffer must be configured to follow the GATT connection between the Host $\leftrightarrow$ **Controller**.

2. Generic Attribute Profile (GATT) Discovery
---------------------------------------------

The GATT defines the data structure and how attributes (Services, Characteristics) are exchanged. This is the layer where application commands are sent and received.

**(This section will be populated once Service and Characteristic UUIDs are identified)**

2.1. Standard Services (Known)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard services (e.g., Device Information Service 0x180A) are typically exposed.

2.2. Custom Command Service (Target)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary goal of the GATT discovery is to identify the custom **128-bit Service UUID** responsible for receiving commands and sending event notifications.

---

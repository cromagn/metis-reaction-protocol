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

I pacchetti SCAN_RSP forniscono i MAC Address che appaiono essere **Public Addresses** (non randomizzati), il che suggerisce che l'indirizzo rimane statico per ogni dispositivo.

* **MAC Address Osservati:**
    * **Device $react-1-:** ``7e:ad:07:91:53:e6``
    * **Device $react-2-:** ``69:de:d6:c7:4c:71``
* **Manufacturer:** I byte iniziali degli indirizzi MAC (Organizationally Unique Identifier - OUI) dovrebbero essere controllati per identificare potenzialmente il produttore del chip Bluetooth (es. Nordic, Texas Instruments, ecc.). Questo dato può fornire indizi sul tipo di stack BLE utilizzato.

1.3. The 'Flip' Principle in GAP Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As discussed in the :ref:`hardware-details` section, the METIS system uses a dynamic network. In the context of GAP, this means:

* All devices advertise initially, but the host application selects one device (e.g., ``$react-1-``) to initiate the **Central Role connection**.
* This first connected device (the **Controller**) then becomes responsible for establishing the proprietary mesh/network with the other **Node** devices.
* **Implication for Sniffing:** Only the **Controller** device maintains a direct, high-level GATT connection to the host application (phone/PC). The other devices communicate with the Controller using lower-level, non-GATT protocols or secondary advertising channels. 

---

**Prossimo Passaggio Critico (GATT):**

Ora che l'identificazione (GAP) è chiara, il passo successivo è l'**Attribute Discovery (GATT)**.

Se ti connetti a uno dei dispositivi (`7e:ad:07:91:53:e6`), quali **Service UUID** e **Characteristic UUID** espone? Questo è ciò che ti dirà dove inviare e ricevere i comandi.

Hai già catturato questi dati?
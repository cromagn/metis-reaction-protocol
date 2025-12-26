.. _tools:

How to sniff
============

Tools:
------

- `nRF Util <https://www.nordicsemi.com/Products/Development-tools/nRF-Util>`_

- `Wireshark <https://www.wireshark.org/>`_

- `Hardware <https://it.aliexpress.com/item/1005009621898979.html>`_


Step by step guide:
-------------------

1. Set the correct probe

.. image:: _static/Howto_0.jpg
   :alt: BLE Sniff Device
   :align: center
   :width: 75%
   
2. Choose the correct MAC

.. image:: _static/HowTo_1.jpg
   :alt: Set the correct MAC
   :align: center
   :width: 50%
   
3. Start sniffing (Play)

.. image:: _static/HowTo_2.jpg
   :alt: Play
   :align: center
   :width: 5%


4. Filter by:

:kbd:`_ws.col.protocol == "ATT"` to sniff the ATT command

:kbd:`frame contains "re"` to sniff the MAC using the name of the devices

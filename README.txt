README

2023-02-08 hb9pae

Files:	receiver.py
LorA Empfaenger
Bibliothek https://github.com/chandrawi/LoRaRF-Python/

Stand der Arbeiten:
- Setzen der Register OK
- Auslesen der Register OK
- Empfang LORA Paket 
	Der Empfang von LoRa Daten scheint zu funktionieren.
Allerdings kann ich die empfangenen Daten nicht decodieren.
Verschiedene Versuche mit Fomraten UTF-8, Byte, ASCII führen zu keinem Erfolg.
-------------

File hoperf.py
Lora Empfänger, auf Basis des C++ Codes HopeRF.cpp nachgebildet. 
Setzen der Register scheint zu funktionieren, 
Empfang von Daten noch nicht realisiert.
--------------

File rdRegister.py
Auslesen der Register aus dme chip RFM95, ausgabe in Hex.


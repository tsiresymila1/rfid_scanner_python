# Clone repository

```bash
     git clone https://github.com/tsiresymila16/rfid_scanner_python.git   
```
# install python dependancy

```bash 
    cd rfid_scanner_python
    python -m pip install pyserial
```

# upload arduino programme
In arduino programme use the code bellow to send rfid data to serian and to be get by python program<br>
**Arduino must be connected with pc with Serial cable**
```arduino 
    // SEND RFID TO SERIAL AND TO 
    Serial.println("AE A4 B7 DE")
```

# Start start mongodb and start scanner

```bash
    python app.py
```

# Tsiresy Milà

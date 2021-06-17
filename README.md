# Clone repository

```bash
     git clone https://github.com/tsiresymila16/rfid_scanner_python.git   
```
# Install python dependancy

```bash 
    cd rfid_scanner_python
    python -m pip install pyserial
```

# Upload arduino program
In arduino program use the code bellow to send **RFID** data to serial and to be get by python program <br>
**Arduino must be connected with pc with Serial cable (USB)**
```arduino 
    // SEND RFID TO SERIAL AND TO 
    Serial.println("AE A4 B7 DE")
```

# Start start mongodb and start scanner

```bash
    python app.py
```


### Tsiresy Milà
### tsiresymila@gmail.com

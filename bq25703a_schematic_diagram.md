# BQ25703A Detaylı Şematik Bağlantı Diyagramı

## Tam Devre Şeması

```
                                            BQ25703A 3S Li-ion Şarj Devresi
    ┌─────────────┐         ┌─────────────────────────────────────────────────────────────────────────┐
    │  USB Type-C │         │                                                                         │
    │    Port     │         │  ┌──────────────────────────────────────────────────┐                  │
    │             │         │  │                    BQ25703A                       │                  │
    │ VBUS ───────┼─────────┼──┼─> VBUS (23,24) ──┬──────────────────────────────┼──┐               │
    │             │    C1   │  │                  │                               │  │               │
    │ CC1 ────────┼─┐ 10µF  │  │                  │    ┌────── BTST1 (19) <───────┼──┼─ C3 (100nF)  │
    │ CC2 ────────┼─┼───────┼──┼─> VAC (21,22)   │    │                          │  │               │
    │             │ │       │  │                  │    │  Q1 (BSC030N08NS5)       │  │               │
    │ D+ ─────────┼─┼───────┼──┼─> D+ Detection  │    └──┤├──┬─── SW1 (17,18) ───┼──┼─── L1 ────┐  │
    │ D- ────────┼─┼───────┼──┼─> D- Detection  │          │                    │  │   3.3µH    │  │
    │             │ │       │  │                  │    Q2    │                    │  │            │  │
    │ GND ────────┼─┼───────┼──┼─> PGND          └─────┤├───┴─── PGND            │  │            │  │
    └─────────────┘ │       │  │                                                  │  │            │  │
                    │       │  │                       ┌────── BTST2 (11) <───────┼──┼─ C4        │  │
         CHK224     │       │  │                       │                          │  │ (100nF)    │  │
    ┌───────────────┴───┐   │  │                       │  Q3 (BSC030N08NS5)       │  │            │  │
    │  PD Controller    │   │  │                       └──┤├──┬─── SW2 (15,16) ───┼──┴────────────┴──┼─> VSYS
    │                   │   │  │                             │                    │                   │
    │ PD_5V ────────────┼───┼──┼─> To ESP32 GPIO            │                    │      R_AC (10mΩ) │
    │ PD_12V ───────────┼───┼──┼─> To ESP32 GPIO      Q4    │                    │         ┌────────┴────┐
    │                   │   │  │                       ┤├────┴─── PGND            │         │             │
    └───────────────────┘   │  │                                                  │      To Battery Pack │
                            │  │  SDA (6) <───────────────────────────────────────┼─────────┼─────────────┼─> (+)
                            │  │  SCL (7) <───────────────────────────────────────┼─── I2C  │             │
                            │  │                                                  │   Bus   │   ┌─────────┼─> Cell3+
                            │  │  CHRG_OK (5) ───> LED ──R_LED(1k)──┐            │         │   │         │
                            │  │  PROCHOT (4) ───> To ESP32         │            │         │   │ R_CELL3 │
                            │  │  CE (3) <──────── From ESP32       ─            │         │   │  10kΩ   │
                            │  │                                                  │         │   │         │
                            │  │  SRP (9) <───────────┬──────────────────────────┼─────────┼───┼─────────┼─> Cell3-/
                            │  │  SRN (10) <──────────┼─────────┬────────────────┼─────────┼───┼─────────┼─> Cell2+
                            │  │                      │ R_SR    │                │         │   │         │
                            │  │                      │ 10mΩ    │                │         │   │ R_CELL2 │
                            │  │                      └─────────┘                │         │   │  10kΩ   │
                            │  │                                                  │         │   │         │
                            │  │  ACP (1) <───────────┬──────────────────────────┼─────────┘   │         │
                            │  │  ACN (2) <───────────┼─────────┬────────────────┼─────────────┼─────────┼─> Cell2-/
                            │  │                      │         │                │             │         │   Cell1+
                            │  │                      └─────────┘                │             │ R_CELL1 │
                            │  │                                                  │             │  10kΩ   │
                            │  │  CELL3 (31) <───────────────────────────────────┼─────────────┘         │
                            │  │  CELL2 (32) <───────────────────────────────────┼───────────────────────┼─> Cell1-/
                            │  │  CELL1 (33) <───────────────────────────────────┼─────────────┬─────────┘   GND
                            │  │                                                  │             │ R_GND
                            │  │  ILIM (27) <──── R_ILIM (40.2kΩ) ──── GND       │             │ 3.3kΩ
                            │  │  IOUT (25) <──── R_IOUT (13.3kΩ) ──── GND       │             │
                            │  │                                                  │             ─
                            │  │  TS (35) <────── RT1 (10kΩ NTC) ───── GND       │
                            │  │                                                  │      BQ34Z100-G1
                            │  │  REGN (8) ────┬─── C_REGN (10µF)                │    ┌────────────┐
                            │  │               │                                  │    │  Battery   │
                            │  │  PMID (12) ───┼─── C_PMID (10µF)                └────┤  Gauge IC  │
                            │  │               │                                       │            │
                            │  └───────────────┼──────────────────────────────────────┤ BAT        │
                            │                  │                                       │ VC1 ───────┼─> Cell1+
                            │                  │      C2 (47µF)                        │ VC2 ───────┼─> Cell2+
                            │                  └──────┤├──── GND                       │ SDA ───────┼─> I2C
                            │                                                          │ SCL ───────┼─> I2C
                            │                                                          └────────────┘
                            │
                            │         ESP32-WROOM-32
                            │       ┌─────────────────┐
                            │       │                 │
                            └───────┤ GPIO32 (PD_DET) │
                                    │ GPIO25 (CE)     │
                                    │ GPIO21 (SDA)    │
                                    │ GPIO22 (SCL)    │
                                    │ GPIO26 (PROCHOT)│
                                    │ GPIO27 (INT)    │
                                    │                 │
                                    └─────────────────┘

```

## Kritik Bağlantı Notları

### 1. Güç Yolu Bağlantıları
- **VBUS** ve **VAC** pinleri kısa devre edilmeli
- **SW1** ve **SW2** düğümleri arasındaki indüktör mümkün olduğunca kısa tutulmalı
- **PGND** bağlantıları tek noktada birleştirilmeli (star ground)

### 2. MOSFET Gate Sürücü Bağlantıları
```
BTST1 ──┬── C_BOOT1 (100nF) ──┬── SW1
        │                      │
        └── Internal Driver ───┴── Q1 Gate

BTST2 ──┬── C_BOOT2 (100nF) ──┬── SW2
        │                      │
        └── Internal Driver ───┴── Q3 Gate
```

### 3. Akım Algılama (Kelvin Bağlantısı)
```
        ┌─── SRP (sense+)
        │
Battery ├─── R_SR (10mΩ) ─── Load
        │
        └─── SRN (sense-)
```

### 4. Hücre Gerilim Algılama Bölücü
```
Cell3+ (12.6V) ──┬── R_CELL3 (10kΩ) ──┬── CELL3 pin
                 │                      │
Cell2+ (8.4V) ───┼── R_CELL2 (10kΩ) ──┼── CELL2 pin
                 │                      │
Cell1+ (4.2V) ───┼── R_CELL1 (10kΩ) ──┼── CELL1 pin
                 │                      │
GND ─────────────┴── R_GND (3.3kΩ) ───┴── GND
```

## Register Ayarları (I2C)

### Başlangıç Konfigürasyonu
```c
// Charge Option 0 (0x00)
// EN_LEARN = 0, EN_OOA = 1, CHRG_INHIBIT = 0
writeRegister16(0x00, 0x020E);

// Charge Current Register (0x02)
// 1200mA = 0x04B0
writeRegister16(0x02, 0x04B0);

// Max Charge Voltage (0x04)
// 12.6V = 0x3138 (12600 mV)
writeRegister16(0x04, 0x3138);

// OTG Voltage (0x06)
// 5V = 0x1388 (5000 mV)
writeRegister16(0x06, 0x1388);

// OTG Current (0x08)
// 1A = 0x0400 (1024 mA)
writeRegister16(0x08, 0x0400);

// Input Voltage (0x0A)
// 4.5V minimum = 0x1194
writeRegister16(0x0A, 0x1194);

// Minimum System Voltage (0x0C)
// 9V = 0x2328
writeRegister16(0x0C, 0x2328);

// Input Current (0x0E)
// Host controlled via ILIM pin
```

### Durum Okuma Registerleri
```c
// ChargeStatus (0x20)
// Bit 15: AC_STAT (adaptör var mı)
// Bit 14: ICO_DONE
// Bit 13-12: Charge Status (00=Not charging, 01=Pre-charge, 10=Fast charge, 11=Done)
// Bit 11: SYSOVP_STAT
// Bit 8: IN_FCHRG (Fast charge modunda mı)

// ADCVBUS/PSYS (0x22)
// VBUS voltage and System power

// ADCIBAT (0x24)
// Battery charge/discharge current

// ADCVSYS/VBAT (0x2C)
// System voltage and Battery voltage
```

## Güvenlik ve Koruma Özellikleri

1. **Giriş Koruması**
   - ACOV: 22V
   - ACUV: 3.5V
   - Ters polarite koruması

2. **Batarya Koruması**
   - Hücre OVP: 4.35V/hücre
   - Batarya OVP: 13.05V (3S)
   - Şarj akımı limiti: Donanım + yazılım

3. **Termal Koruma**
   - PROCHOT çıkışı
   - Termal shutdown: 150°C
   - Termal regulation: 120°C

4. **Sistem Koruması**
   - VSYS regülasyonu
   - Dinamik güç yönetimi (DPM)
   - Giriş akım limiti
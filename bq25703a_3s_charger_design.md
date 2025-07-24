# BQ25703A ile 3S Li-ion Batarya Şarj Devresi Tasarımı

## Sistem Özeti
- **IC**: BQ25703A (NVDC Buck-Boost Battery Charge Controller)
- **Batarya**: 3S Li-ion (3x18650)
- **Giriş**: USB Type-C PD (5V-20V)
- **Şarj Akımı**: 1.2A @ 13V, 0.45A @ 5V
- **Çıkış**: 12.6V max (3S tam dolu)

## BQ25703A'nın Avantajları
- 1S-4S batarya desteği
- USB Type-C PD native desteği
- Buck-boost topoloji (geniş giriş/çıkış aralığı)
- I2C/SMBus kontrolü
- Dahili güç yolu yönetimi (NVDC)
- OTG desteği

## Devre Tasarımı - Temel Bağlantılar

### 1. Güç Girişi (VBUS)
```
USB Type-C → VBUS (Pin 23,24)
           → VAC (Pin 21,22) 
```

### 2. Buck-Boost Güç Katı
```
VBUS → Q1 (High-side 1) → SW1 → L1 → SW2 → Q3 (High-side 2) → VSYS
       ↓                                      ↓
       Q2 (Low-side 1)                       Q4 (Low-side 2)
       ↓                                      ↓
      PGND                                   PGND
```

### 3. Batarya Bağlantısı
```
VSYS → Current Sense (RAC) → Battery Pack (+)
                            → Cell 1 (+)
                            → Cell 2 (+)  
                            → Cell 3 (+)
                            → Cell 3 (-) = Battery Pack (-)
```

## JLCPCB Komponent Listesi

### Ana IC
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| U1 | BQ25703ARSNR | C2678129 | Buck-Boost Şarj Kontrolcüsü |

### MOSFET'ler (Güç Katı)
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| Q1,Q3 | BSC030N08NS5 | C696830 | 80V N-Ch, 3mΩ, SON-8 |
| Q2,Q4 | BSC030N08NS5 | C696830 | 80V N-Ch, 3mΩ, SON-8 |

### Pasif Komponentler
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| L1 | 3.3µH/8A | C408417 | TDK SPM6530T-3R3M |
| C_IN | 22µF/25V | C59461 | Seramik, 1206, X5R |
| C_OUT | 47µF/16V | C310843 | Seramik, 1210, X5R |
| C_BOOT1,2 | 100nF/25V | C49678 | Seramik, 0603, X7R |
| R_AC | 10mΩ/1% | C163065 | 2512, 1W |
| R_SR | 10mΩ/1% | C163065 | 2512, 1W |

### Gerilim Ayar Dirençleri
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| R_CELL3 | 10kΩ | C22975 | 0603, %1 |
| R_CELL2 | 10kΩ | C22975 | 0603, %1 |
| R_CELL1 | 10kΩ | C22975 | 0603, %1 |
| R_GND | 3.3kΩ | C22978 | 0603, %1 |

### Akım Limiti Ayarları
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| R_ILIM | 40.2kΩ | C25804 | 0603, %1 (3A limit) |
| R_IOUT | 13.3kΩ | C22976 | 0603, %1 (1.5A şarj) |

### Diğer Komponentler
| Parça | Değer | JLCPCB Part # | Açıklama |
|-------|-------|---------------|----------|
| RT1 | 10kΩ NTC | C123378 | 0603, B=3950K |
| C_REGN | 10µF/6.3V | C19702 | Seramik, 0805 |
| C_PMID | 10µF/25V | C15850 | Seramik, 0805 |
| D_CHRG | LED Yeşil | C72043 | 0603, Şarj göstergesi |
| R_LED | 1kΩ | C21190 | 0603, LED direnci |

## Pin Bağlantıları Detayı

### Güç Pinleri
```
VBUS (23,24) ← USB giriş (5-20V)
VAC (21,22)  ← Adaptör algılama
SW1 (17,18)  → Buck düğümü
SW2 (15,16)  → Boost düğümü
VSYS (13,14) → Sistem çıkışı
BTST1 (19)   → Bootstrap 1
BTST2 (11)   → Bootstrap 2
```

### Kontrol Pinleri
```
SDA (6)      ↔ ESP32 I2C Data
SCL (7)      ↔ ESP32 I2C Clock
PROCHOT (4)  → Termal uyarı
CHRG_OK (5)  → Şarj durumu
CE (3)       ← Şarj enable
```

### Algılama Pinleri
```
SRP (9)      ← Akım sense +
SRN (10)     ← Akım sense -
ACP (1)      ← AC akım sense +
ACN (2)      ← AC akım sense -
```

### Batarya Gerilim Algılama
```
CELL3 (31)   ← Cell 3 gerilimi (12.6V)
CELL2 (32)   ← Cell 2 gerilimi (8.4V)
CELL1 (33)   ← Cell 1 gerilimi (4.2V)
```

## ESP32 Kontrol Kodu

```c
#include <Wire.h>

#define BQ25703A_ADDR    0x6B
#define CHK224_PD_DET    GPIO_NUM_32

// Register adresleri
#define REG_CHARGE_OPTION_0   0x00
#define REG_CHARGE_CURRENT    0x02
#define REG_MAX_CHARGE_VOLTAGE 0x04
#define REG_CHARGE_STATUS     0x20

// Konfigürasyon
void configureBQ25703A() {
    // Şarj voltajı: 12.6V (3S)
    writeRegister16(REG_MAX_CHARGE_VOLTAGE, 12600); // mV
    
    // PD algılama ve akım ayarı
    if (digitalRead(CHK224_PD_DET) == HIGH) {
        // 12V PD - 1.2A şarj
        writeRegister16(REG_CHARGE_CURRENT, 1200); // mA
    } else {
        // 5V USB - 450mA şarj
        writeRegister16(REG_CHARGE_CURRENT, 450); // mA
    }
    
    // Şarjı etkinleştir
    uint16_t option = readRegister16(REG_CHARGE_OPTION_0);
    option |= (1 << 4); // CHRG_INHIBIT = 0
    writeRegister16(REG_CHARGE_OPTION_0, option);
}

// Durum okuma
void readChargeStatus() {
    uint16_t status = readRegister16(REG_CHARGE_STATUS);
    
    bool inCharge = (status >> 8) & 0x01;
    bool inPrecharge = (status >> 11) & 0x01;
    bool inFastCharge = (status >> 12) & 0x01;
    bool chargeDone = (status >> 13) & 0x01;
    
    Serial.print("Şarj Durumu: ");
    if (chargeDone) Serial.println("Tamamlandı");
    else if (inFastCharge) Serial.println("Hızlı Şarj");
    else if (inPrecharge) Serial.println("Ön Şarj");
    else Serial.println("Beklemede");
}

// I2C yardımcı fonksiyonlar
void writeRegister16(uint8_t reg, uint16_t value) {
    Wire.beginTransmission(BQ25703A_ADDR);
    Wire.write(reg);
    Wire.write(value & 0xFF);
    Wire.write((value >> 8) & 0xFF);
    Wire.endTransmission();
}

uint16_t readRegister16(uint8_t reg) {
    Wire.beginTransmission(BQ25703A_ADDR);
    Wire.write(reg);
    Wire.endTransmission(false);
    
    Wire.requestFrom(BQ25703A_ADDR, 2);
    uint16_t value = Wire.read();
    value |= (Wire.read() << 8);
    return value;
}
```

## PCB Tasarım Önerileri

### 1. Güç Yolu Layout
- SW1 ve SW2 düğümleri minimum alan
- MOSFET'ler arası mesafe < 5mm
- Güç yolları 2oz bakır, min 3mm genişlik

### 2. Termal Yönetim
- IC altına termal via'lar (min 9 adet)
- MOSFET'ler için bakır döküm alan
- Termal pad bağlantısı zorunlu

### 3. Sinyal Yönlendirme
- I2C hatları diğer sinyallerden uzak
- Akım algılama Kelvin bağlantısı
- Bootstrap kapasitörleri IC'ye yakın

### 4. EMI Önlemleri
- Giriş/çıkış filtre kapasitörleri
- Anahtarlama düğümleri etrafında GND guard ring
- 4 katmanlı PCB önerisi

## Test ve Doğrulama

1. **Giriş Testi**
   - 5V USB: 450mA şarj akımı
   - 12V PD: 1.2A şarj akımı
   - 20V PD: Sistem kararlılığı

2. **Şarj Profili**
   - CC fazı: 1.2A sabit
   - CV fazı: 12.6V'a yaklaşırken akım düşüşü
   - Sonlandırma: <120mA'da durma

3. **Koruma Testleri**
   - OVP: 13V'da kesme
   - OCP: 1.5A'da limit
   - OTP: 60°C'de güç azaltma

## Maliyet Tahmini (JLCPCB)
- BQ25703A: ~$3.50
- MOSFET'ler (4x): ~$2.00
- Pasifler: ~$2.00
- PCB (4 katman): ~$5.00
- **Toplam**: ~$12.50/adet (100 adet için)
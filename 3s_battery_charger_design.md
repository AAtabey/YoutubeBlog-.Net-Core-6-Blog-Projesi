# 3S Li-ion Batarya Şarj Sistemi Tasarımı

## Sistem Özellikleri
- **Batarya Konfigürasyonu**: 3S (3x18650) Li-ion
- **Nominal Gerilim**: 11.1V (3.7V x 3)
- **Maksimum Gerilim**: 12.6V (4.2V x 3)
- **Çalışma Gerilimi**: 12V
- **Şarj Akımı**: 13V'da 1.2A, 5V'da 0.45A
- **Kontrol**: ESP32 MCU

## Önerilen Entegre Değişikliği

### BQ24610 Yerine: BQ24618 veya BQ25703A

**BQ25703A Avantajları:**
- USB Type-C PD 3.0 desteği
- 1S-4S batarya desteği
- Dahili buck-boost dönüştürücü
- I2C/SMBus kontrolü
- Otomatik giriş gerilimi algılama

## Devre Tasarımı

### 1. USB Type-C PD Girişi
```
USB Type-C Port
    |
    ├── CC1/CC2 ──────> CHK224
    ├── VBUS ─────────> TPS43061 Girişi
    └── D+/D- ────────> ESP32 (USB algılama)

CHK224 Çıkışları:
- PD_5V: 5V algılama sinyali
- PD_12V: 12V algılama sinyali → ESP32 GPIO
```

### 2. Güç Dönüştürücü (TPS43061)
```
TPS43061 Bağlantıları:
- VIN: USB VBUS (5V-20V)
- VOUT: 13V sabit çıkış
- EN: ESP32 kontrolü
- FB: Gerilim geri besleme (13V için ayarla)

Komponent Değerleri:
- L1: 10µH, 3A inductor
- C_IN: 22µF, 25V seramik
- C_OUT: 47µF, 16V seramik
- R_FB1: 100kΩ
- R_FB2: 8.45kΩ (13V çıkış için)
```

### 3. Şarj Kontrolcüsü (BQ25703A Önerisi)
```
BQ25703A Temel Bağlantılar:

Güç Girişi:
- VBUS: TPS43061 çıkışı (13V) veya USB 5V
- VAC: Adaptör algılama

Batarya Bağlantısı:
- BAT: 3S batarya paketi (+)
- SRP/SRN: Akım algılama direnci (10mΩ)

Kontrol:
- SDA/SCL: ESP32 I2C
- CHRG_OK: Şarj durumu → ESP32 GPIO
- PROCHOT: Termal koruma

Konfigürasyon:
- ILIM_HIZ: Giriş akım limiti (1.5A için 63.4kΩ)
- IOUT: Şarj akımı ayarı (register ile)
```

### 4. Batarya Yönetimi (BQ34Z100-G1)
```
BQ34Z100-G1 Bağlantılar:

Batarya Hücreleri:
- BAT: Pack pozitif
- VC1: Hücre 1-2 arası
- VC2: Hücre 2-3 arası
- VSS: Pack negatif

Akım Algılama:
- SRP/SRN: 10mΩ sense direnci

Kontrol:
- SDA/SCL: ESP32 I2C (adres: 0x55)
- GPIO: Alarm çıkışı → ESP32

Sıcaklık:
- TS1: 10kΩ NTC termistör
```

### 5. ESP32 Kontrol Yazılımı

```c
// I2C Adresleri
#define BQ25703A_ADDR   0x6B
#define BQ34Z100_ADDR   0x55
#define CHK224_GPIO     GPIO_NUM_XX

// Şarj Kontrol Fonksiyonu
void configureCharging() {
    if (gpio_get_level(CHK224_GPIO) == HIGH) {
        // 12V PD algılandı
        setBQ25703AInputLimit(1500);  // 1.5A limit
        setBQ25703AChargeCurrent(1200); // 1.2A şarj
    } else {
        // 5V USB algılandı
        setBQ25703AInputLimit(500);   // 500mA limit
        setBQ25703AChargeCurrent(450); // 450mA şarj
    }
}

// Batarya Durumu Okuma
void readBatteryStatus() {
    uint16_t voltage = readBQ34Z100Voltage();
    int16_t current = readBQ34Z100Current();
    uint8_t soc = readBQ34Z100SOC();
    int16_t temp = readBQ34Z100Temperature();
    
    printf("Batarya: %.2fV, %.2fA, %d%%, %.1f°C\n", 
           voltage/1000.0, current/1000.0, soc, temp/10.0);
}
```

## PCB Tasarım Önerileri

1. **Güç Yolları**: En az 2oz bakır kullanın
2. **Termal Yönetim**: Şarj IC'leri için termal pad ve via'lar
3. **EMI Koruma**: Buck-boost bölgesini faraday kafesi ile çevirin
4. **Akım Algılama**: Kelvin bağlantısı kullanın

## Komponent Listesi

| Komponent | Değer | Açıklama |
|-----------|-------|----------|
| U1 | CHK224 | USB Type-C PD kontrolcü |
| U2 | TPS43061 | Buck-boost dönüştürücü |
| U3 | BQ25703A | Şarj kontrolcüsü |
| U4 | BQ34Z100-G1 | Batarya gauge IC |
| U5 | ESP32-WROOM | MCU |
| R_SENSE | 10mΩ, 1% | Akım algılama |
| L1 | 10µH, 3A | Buck-boost inductor |
| NTC | 10kΩ @ 25°C | Sıcaklık sensörü |

## Güvenlik Özellikleri

1. **Aşırı Gerilim Koruması**: 13.5V üzerinde şarj durdurma
2. **Aşırı Akım Koruması**: 1.5A giriş limiti
3. **Sıcaklık Koruması**: 0°C - 45°C şarj aralığı
4. **Hücre Dengeleme**: Pasif dengeleme (opsiyonel)
5. **Kısa Devre Koruması**: Otomatik kesme

## Test ve Doğrulama

1. USB 5V girişte 450mA şarj akımı
2. USB PD 12V girişte 1.2A şarj akımı
3. Batarya doluluk testi (12.6V'da kesme)
4. Sıcaklık koruması testi
5. ESP32 kontrol doğrulaması
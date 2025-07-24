# BQ24610 ile 3S Li-ion Şarj Devresi Tasarımı

## BQ24610 Hakkında Önemli Notlar

BQ24610 bir şarj kontrolcüsü değil, sadece PWM kontrolcüsüdür. Tam bir şarj devresi için harici komponentler gerekir:
- Harici N-kanal MOSFET'ler (High-side ve Low-side)
- Gate sürücü devresi
- Akım algılama direnci
- Kompanzasyon komponenetleri

## BQ24610 ile Devre Tasarımı

### 1. Güç Katı Bağlantıları

```
                     ┌─────────────────┐
    13V Giriş ──────►│     BQ24610     │
         │           │                 │
         │           │ BTST      PH    │
         │           └──┬──────────┬───┘
         │              │          │
         │   C_BOOT    │          │
         │   0.1µF     │          │  Q1 (High-side)
         ├─────────────┤          ├──┤├─┐ CSD19536KTT
         │             │          │     │
         │             └──────────┘     │
         │                              │
         │                              ├──── L1 ──┬──► Batarya+
         │                              │    10µH   │
         │              Q2 (Low-side)   │          │
         └──────────────┤├──────────────┘          │
                   CSD19536KTT                     │
                        │                       C_OUT
                        │                       47µF
                        ┴ GND                      ┴
```

### 2. Pin Bağlantıları ve Fonksiyonları

| Pin | Fonksiyon | Bağlantı |
|-----|-----------|----------|
| VCC | Besleme | 13V giriş |
| REGN | 6V LDO çıkış | 10µF kapasitör |
| BTST | Bootstrap | High-side gate sürücü |
| PH | Faz düğümü | MOSFET bağlantı noktası |
| LODRV | Low-side gate | Q2 gate |
| HIDRV | High-side gate | Q1 gate |
| SRP/SRN | Akım algılama | 10mΩ sense direnci |
| FB | Gerilim geri besleme | Gerilim bölücü |
| ISET | Şarj akımı ayarı | Direnç ile GND'ye |
| ACDRV | Adaptör kontrolü | Opsiyonel |
| CE | Şarj enable | ESP32 kontrolü |
| STAT1/2 | Durum çıkışı | LED veya ESP32 |
| TS | Sıcaklık sensörü | 10kΩ NTC |

### 3. Kritik Komponent Hesaplamaları

#### Şarj Akımı Ayarı (ISET):
```
I_CHARGE = V_REF / (20 × R_SENSE × R_ISET/64kΩ)

1.2A için:
R_ISET = (2.5V × 64kΩ) / (20 × 0.01Ω × 1.2A)
R_ISET = 66.7kΩ (68kΩ standart değer)
```

#### Çıkış Gerilimi Ayarı (FB):
```
V_OUT = 2.1V × (1 + R1/R2)

12.6V için:
R1 = 100kΩ
R2 = 20kΩ
```

#### Giriş Akım Limiti:
```
I_AC_LIM = K_ACILIM / R_ACILIM
K_ACILIM = 1800

1.5A için:
R_ACILIM = 1800 / 1.5 = 1.2kΩ
```

### 4. ESP32 Kontrol Arayüzü

```c
// GPIO Tanımlamaları
#define BQ24610_CE_PIN      GPIO_NUM_25
#define BQ24610_STAT1_PIN   GPIO_NUM_26
#define BQ24610_STAT2_PIN   GPIO_NUM_27
#define PD_DETECT_PIN       GPIO_NUM_32

// Şarj Durumu Okuma
typedef enum {
    CHARGE_READY = 0,
    CHARGE_IN_PROGRESS,
    CHARGE_DONE,
    CHARGE_FAULT
} charge_status_t;

charge_status_t readChargeStatus() {
    uint8_t stat1 = gpio_get_level(BQ24610_STAT1_PIN);
    uint8_t stat2 = gpio_get_level(BQ24610_STAT2_PIN);
    
    if (stat1 == 0 && stat2 == 0) return CHARGE_READY;
    if (stat1 == 1 && stat2 == 0) return CHARGE_IN_PROGRESS;
    if (stat1 == 0 && stat2 == 1) return CHARGE_DONE;
    return CHARGE_FAULT;
}

// Dinamik Şarj Kontrolü
void controlCharging() {
    if (gpio_get_level(PD_DETECT_PIN) == HIGH) {
        // 12V PD algılandı - Tam hızda şarj
        gpio_set_level(BQ24610_CE_PIN, LOW);  // Şarjı etkinleştir
    } else {
        // 5V USB - Düşük güçte şarj için harici devre gerekli
        // BQ24610 minimum 5V'un üzerinde çalışır
        gpio_set_level(BQ24610_CE_PIN, HIGH); // Şarjı devre dışı bırak
    }
}
```

### 5. Güvenlik ve Koruma Devreleri

```
Sıcaklık Koruması:
                 VCC (3.3V)
                  │
                  R1 (10kΩ)
                  │
    TS Pin ──────┼──── NTC (10kΩ @ 25°C)
                  │
                  R2 (3.24kΩ)
                  │
                 GND

Şarj Penceresi: 0°C - 45°C
```

### 6. PCB Layout Önerileri

1. **MOSFET Yerleşimi**: Q1 ve Q2'yi mümkün olduğunca yakın yerleştirin
2. **Akım Yolları**: Yüksek akım yollarını kısa ve geniş tutun (min 3mm)
3. **Termal Yönetim**: MOSFET'ler için soğutucu veya bakır alan
4. **EMI**: Anahtarlama düğümünü (PH) küçük tutun
5. **Sense Hatları**: Kelvin bağlantısı kullanın

## Alternatif: Daha Basit Çözüm

Eğer BQ24610'un karmaşıklığı fazla geliyorsa, önerilen alternatifler:

### 1. BQ24650 (Solar Uyumlu)
- Dahili MOSFET sürücüleri
- MPPT desteği
- Daha basit tasarım

### 2. BQ25703A (Modern Çözüm)
- USB PD desteği
- I2C kontrolü
- Dahili güç yolu yönetimi
- Otomatik giriş algılama

### 3. MP2759A (Kompakt)
- Buck-boost topoloji
- Geniş giriş aralığı
- Dahili kompanzasyon

## Sonuç ve Öneriler

BQ24610 kullanımı:
- ✅ Yüksek verimlilik (%95+)
- ✅ Esnek tasarım
- ❌ Karmaşık devre
- ❌ Fazla harici komponent
- ❌ 5V desteği yok

**Tavsiyem**: Projeniz için BQ25703A veya benzeri modern bir şarj IC'si kullanın. Daha az komponent, daha kolay tasarım ve USB PD desteği sağlar.
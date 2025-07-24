# BQ25703A 3S Batarya Şarj Devresi Optimizasyon Rehberi

## Sizin İhtiyaçlarınıza Göre Optimizasyon

### Sistem Parametreleri
- **Batarya**: 3S Li-ion (3x18650)
- **Maksimum Gerilim**: 12.6V (4.2V x 3)
- **Çalışma Gerilimi**: 12V
- **Hedef Şarj Akımı**: 1.2A @ 13V giriş, 0.45A @ 5V giriş
- **Kontrol**: ESP32 + CHK224 PD kontrolcü

## Kritik Komponent Değişiklikleri

### 1. Akım Algılama Dirençleri
```
Orijinal: R_AC = R_SR = 10mΩ
Optimizasyon için:
- Düşük akım hassasiyeti için: R_AC = R_SR = 20mΩ
- Daha düşük güç kaybı istiyorsanız: R_AC = R_SR = 5mΩ
```

**Hesaplama**:
- Güç kaybı = I² × R
- 10mΩ'da 1.2A için: P = 1.2² × 0.01 = 14.4mW
- 20mΩ'da 1.2A için: P = 1.2² × 0.02 = 28.8mW
- 5mΩ'da 1.2A için: P = 1.2² × 0.005 = 7.2mW

### 2. Şarj Akımı Ayarları

#### Register Tabanlı Ayar:
```c
// Charge Current Register (0x02)
// 1.2A için:
uint16_t charge_current_mA = 1200;
uint16_t reg_value = (charge_current_mA / 64) << 6;
writeRegister16(0x02, reg_value);

// 0.45A için:
charge_current_mA = 450;
reg_value = (charge_current_mA / 64) << 6;
writeRegister16(0x02, reg_value);
```

#### IOUT Pini ile Hardware Ayar:
```
IOUT direnci hesaplama:
I_CHG = (KIOUT × VREF) / (R_IOUT × R_SENSE)

Değerler:
- KIOUT = 40 (sabit)
- VREF = 1.2V (sabit)
- R_SENSE = 10mΩ

1.2A için:
R_IOUT = (40 × 1.2) / (1.2 × 0.01) = 4000Ω = 4kΩ

0.45A için:
R_IOUT = (40 × 1.2) / (0.45 × 0.01) = 10.67kΩ ≈ 10.7kΩ
```

### 3. Giriş Akım Limiti Optimizasyonu

#### ILIM Pini Ayarı:
```
ILIM direnci hesaplama:
I_ILIM = KILIM / R_ILIM

Değerler:
- KILIM = 1360 (tipik)

13V giriş için 1.5A limit:
R_ILIM = 1360 / 1.5 = 906Ω ≈ 910Ω

5V giriş için 500mA limit:
R_ILIM = 1360 / 0.5 = 2720Ω ≈ 2.7kΩ
```

**Dinamik Limit için**: I2C üzerinden ayarlayın

### 4. Batarya Gerilim Algılama Optimizasyonu

Orijinal değerler:
- R_CELL1 = R_CELL2 = R_CELL3 = 10kΩ
- R_GND = 3.3kΩ

**Daha hassas okuma için**:
```
R_CELL1 = R_CELL2 = R_CELL3 = 100kΩ
R_GND = 33kΩ
```

Bu değişiklik:
- Daha düşük güç tüketimi
- Daha az batarya yükü
- Aynı bölme oranı

### 5. Güç Katı MOSFET Seçimi

**Yüksek Verimlilik için Alternatifler**:

| MOSFET | RDS(on) | JLCPCB Part | Fiyat |
|--------|---------|-------------|--------|
| BSC030N08NS5 | 3.0mΩ | C696830 | $0.45 |
| FDMS86255 | 2.5mΩ | C2835435 | $0.55 |
| CSD17585F5 | 2.2mΩ | C2762446 | $0.65 |

**Verimlilik Hesabı**:
```
P_loss = I² × RDS(on) × 4 (4 MOSFET)
3.0mΩ için: P = 1.2² × 0.003 × 4 = 17.3mW
2.2mΩ için: P = 1.2² × 0.0022 × 4 = 12.7mW
```

### 6. İndüktör Optimizasyonu

**Orijinal**: 3.3µH/8A

**Alternatifler**:
```
Düşük ripple için: 4.7µH
Yüksek verim için: 2.2µH
Dengeli: 3.3µH (orijinal)
```

**Ripple akımı hesabı**:
```
ΔI = (VIN - VOUT) × D / (L × f)
f = 600kHz (tipik)

3.3µH için: ΔI ≈ 0.3A
4.7µH için: ΔI ≈ 0.21A
2.2µH için: ΔI ≈ 0.45A
```

## ESP32 Kontrol Optimizasyonu

### Dinamik Güç Yönetimi
```c
void optimizeCharging() {
    float vbus = readVBUS();
    float vbat = readVBAT();
    float temp = readTemperature();
    
    // Sıcaklık bazlı akım azaltma
    if (temp > 40) {
        setChargeCurrent(800); // 40°C üzerinde azalt
    } else if (temp > 45) {
        setChargeCurrent(400); // 45°C üzerinde daha da azalt
    }
    
    // Giriş gerilimi bazlı optimizasyon
    if (vbus < 5.5) {
        // 5V USB - düşük güç modu
        setChargeCurrent(450);
        setInputCurrentLimit(500);
    } else if (vbus > 11.5) {
        // 12V PD - yüksek güç modu
        setChargeCurrent(1200);
        setInputCurrentLimit(1500);
    }
    
    // Batarya durumu optimizasyonu
    if (vbat > 12.4) {
        // CV fazına yakın, akımı azalt
        setChargeCurrent(600);
    }
}
```

### Güvenlik Optimizasyonu
```c
// Aşırı gerilim koruması
writeRegister16(0x04, 12650); // 12.65V max (12.6V + %0.4)

// Minimum sistem gerilimi
writeRegister16(0x0C, 9000); // 9V minimum

// Termal koruma
if (readRegister16(0x20) & 0x8000) { // TSHUT flag
    setChargeCurrent(0); // Şarjı durdur
    activateCooling(); // Soğutma fanı
}
```

## PCB Layout Optimizasyonları

### 1. Termal Yönetim
```
- MOSFET'ler için termal pad: min 4cm²
- Via sayısı: 25 adet (0.3mm çap)
- Bakır döküm: Top ve bottom katmanda
```

### 2. EMI Azaltma
```
- SW1/SW2 trace uzunluğu: < 10mm
- Snubber devresi: 10Ω + 100pF (SW düğümlerine)
- Giriş filtresi: 0.1µF || 10µF || 47µF
```

### 3. Akım Yolu Optimizasyonu
```
- Güç yolu genişliği: 4mm (2oz bakır)
- Via boyutu: 0.5mm (güç), 0.3mm (sinyal)
- Star ground bağlantısı
```

## Maliyet Optimizasyonu

### Komponent Alternatifleri

| Komponent | Premium | Standart | Ekonomik |
|-----------|---------|----------|----------|
| MOSFET | CSD17585F5 | BSC030N08NS5 | AON6414A |
| İndüktör | Würth 744373330033 | TDK SPM6530T | Generic 3.3µH |
| Kapasitör | Murata GRM | Samsung CL | Generic X5R |

### Toplam Maliyet (100 adet)
- Premium: ~$15/adet
- Standart: ~$12/adet (önerilen)
- Ekonomik: ~$9/adet

## Test ve Doğrulama Kontrol Listesi

### 1. Güç Testi
- [ ] 5V giriş @ 450mA şarj
- [ ] 12V giriş @ 1.2A şarj
- [ ] Geçiş testi (5V ↔ 12V)

### 2. Koruma Testleri
- [ ] OVP testi (13.5V giriş)
- [ ] OCP testi (1.5A üzeri)
- [ ] OTP testi (60°C)
- [ ] Kısa devre testi

### 3. Verimlilik Ölçümleri
- [ ] 5V giriş verimi (hedef: >85%)
- [ ] 12V giriş verimi (hedef: >92%)
- [ ] Termal görüntüleme

### 4. EMC Testleri
- [ ] Conducted emissions
- [ ] Radiated emissions
- [ ] ESD testi (±8kV)

## Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

1. **Şarj başlamıyor**
   - CE pini kontrolü (LOW olmalı)
   - ILIM direnci kontrolü
   - I2C haberleşme kontrolü

2. **Düşük şarj akımı**
   - Giriş akım limiti kontrolü
   - Termal throttling kontrolü
   - IOUT direnci ölçümü

3. **Yüksek ısınma**
   - MOSFET RDS(on) kontrolü
   - PCB termal tasarım incelemesi
   - Anahtarlama frekansı kontrolü

4. **EMI sorunları**
   - Snubber devresi ekleme
   - Layout optimizasyonu
   - Giriş filtresi güçlendirme
# BQ25703A Komponent Değişiklikleri - 3S Li-ion Şarj Devresi

## Değiştirilmesi Gereken Komponentler

### 1. MOSFET'ler (Q1, Q2, Q3, Q4)
**Orijinal**: Datasheet'te belirtilmemiş
**Yeni Değer**: BSC030N08NS5 (JLCPCB: C696830)
- 80V, 3mΩ RDS(on)
- 4 adet kullanılacak

### 2. Ana İndüktör (L1)
**Orijinal**: 1.5µH (tipik değer)
**Yeni Değer**: 3.3µH, 8A (JLCPCB: C408417)
- Daha düşük ripple için

### 3. Akım Algılama Dirençleri

#### RAC (AC Akım Algılama)
**Orijinal**: 5mΩ
**Yeni Değer**: 10mΩ, 1%, 2512 package (JLCPCB: C163065)

#### RSR (Batarya Akım Algılama)
**Orijinal**: 5mΩ
**Yeni Değer**: 10mΩ, 1%, 2512 package (JLCPCB: C163065)

### 4. Şarj Akımı Ayar Direnci (RIOUT)
**Orijinal**: Yok veya farklı değer
**Yeni Değer**: 
- 13V giriş için: 4.0kΩ, 1% (JLCPCB: C25917) → 1.2A şarj
- 5V giriş için: 10.7kΩ, 1% (JLCPCB: C25850) → 0.45A şarj

**Not**: ESP32 ile dinamik kontrol için bu direnç kullanılmayabilir

### 5. Giriş Akım Limiti Direnci (RILIM)
**Orijinal**: 40.2kΩ
**Yeni Değer**: 910Ω, 1% (JLCPCB: C22847)
- 1.5A giriş limiti için

### 6. Batarya Gerilim Algılama Dirençleri

#### RCELL3
**Orijinal**: 10kΩ
**Değişiklik Yok**: 10kΩ, 1% (JLCPCB: C22975)

#### RCELL2
**Orijinal**: 10kΩ
**Değişiklik Yok**: 10kΩ, 1% (JLCPCB: C22975)

#### RCELL1
**Orijinal**: 10kΩ
**Değişiklik Yok**: 10kΩ, 1% (JLCPCB: C22975)

#### RGND
**Orijinal**: 3.3kΩ
**Değişiklik Yok**: 3.3kΩ, 1% (JLCPCB: C22978)

### 7. Bootstrap Kapasitörleri

#### CBOOT1 (BTST1 - SW1 arası)
**Orijinal**: 100nF
**Değişiklik Yok**: 100nF, 25V, X7R (JLCPCB: C49678)

#### CBOOT2 (BTST2 - SW2 arası)
**Orijinal**: 100nF
**Değişiklik Yok**: 100nF, 25V, X7R (JLCPCB: C49678)

### 8. Giriş Kapasitörleri

#### CIN1
**Orijinal**: 10µF
**Yeni Değer**: 22µF, 25V, X5R, 1206 (JLCPCB: C59461)

#### CIN2
**Orijinal**: 0.1µF
**Yeni Değer**: 0.1µF + 22µF paralel
- 0.1µF (JLCPCB: C49678)
- 22µF (JLCPCB: C59461)

### 9. Çıkış Kapasitörleri

#### COUT1
**Orijinal**: 10µF
**Yeni Değer**: 47µF, 16V, X5R, 1210 (JLCPCB: C310843)

#### COUT2
**Orijinal**: 0.1µF
**Yeni Değer**: 0.1µF + 47µF paralel
- 0.1µF (JLCPCB: C49678)
- 47µF (JLCPCB: C310843)

### 10. REGN Kapasitörü (CREGN)
**Orijinal**: 1µF
**Yeni Değer**: 10µF, 6.3V, X5R (JLCPCB: C19702)

### 11. PMID Kapasitörü (CPMID)
**Orijinal**: 10µF
**Değişiklik Yok**: 10µF, 25V, X5R (JLCPCB: C15850)

### 12. Sıcaklık Sensörü (RT)
**Orijinal**: Belirtilmemiş
**Yeni Değer**: 10kΩ NTC, B=3950K (JLCPCB: C123378)

### 13. TS Pin Dirençleri (Opsiyonel)
Eğer NTC kullanmıyorsanız:
- RTS1: 5.6kΩ (üst direnç)
- RTS2: 10kΩ (alt direnç)

### 14. I2C Pull-up Dirençleri
**Orijinal**: Belirtilmemiş
**Yeni Değer**: 
- RSDA: 10kΩ (JLCPCB: C22975)
- RSCL: 10kΩ (JLCPCB: C22975)

### 15. Durum LED'i ve Direnci
**Yeni Ekleme**:
- DLED: Yeşil LED (JLCPCB: C72043)
- RLED: 1kΩ (JLCPCB: C21190)

## Kritik Değişiklik Özeti

| Komponent | Eski Değer | Yeni Değer | Sebep |
|-----------|------------|------------|--------|
| RAC/RSR | 5mΩ | 10mΩ | Daha iyi akım algılama hassasiyeti |
| L1 | 1.5µH | 3.3µH | Düşük ripple, 3S batarya için uygun |
| RIOUT | - | 4.0kΩ/10.7kΩ | Şarj akımı ayarı |
| RILIM | 40.2kΩ | 910Ω | 1.5A giriş limiti |
| CIN | 10µF | 2x22µF | Daha iyi giriş filtreleme |
| COUT | 10µF | 2x47µF | Daha kararlı çıkış |

## ESP32 ile Dinamik Kontrol İçin Register Ayarları

```c
// Başlangıç ayarları
void initBQ25703A() {
    // Charge Option 0
    writeRegister16(0x00, 0x020E);
    
    // Charge Current - 1.2A için
    writeRegister16(0x02, 0x04B0);
    
    // Max Charge Voltage - 12.6V (3S)
    writeRegister16(0x04, 0x3138);
    
    // Input Current Limit
    writeRegister16(0x0E, 0x05DC); // 1500mA
    
    // Minimum System Voltage - 9V
    writeRegister16(0x0C, 0x2328);
}
```

## PCB Layout Kriterleri
1. RAC ve RSR dirençleri için Kelvin bağlantısı
2. SW1 ve SW2 düğümleri minimum alan
3. MOSFET'ler IC'ye yakın
4. Güç yolları en az 3mm genişlik
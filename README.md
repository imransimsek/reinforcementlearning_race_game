# F1 Yarış Simülasyonu & Yapay Zeka  
# F1 Racing Simulation & Artificial Intelligence

![Project Banner](docs/banner.png)

## İçindekiler / Table of Contents
- [Genel Bakış / Overview](#genel-bakış--overview)  
- [Özellikler / Features](#özellikler--features)  
- [Kurulum / Installation](#kurulum--installation)  
- [Kullanım / Usage](#kullanım--usage)  
  - [Manuel Mod / Manual Mode](#manuel-mod--manual-mode)  
  - [Eğitim Modu (Genetik Algoritma) / Training Mode (Genetic Algorithm)](#eğitim-modu-genetik-algoritma--training-mode-genetic-algorithm)  
  - [Geliştirilmiş AI Modu (Sinir Ağı) / Advanced AI Mode (Neural Network)](#geliştirilmiş-ai-modu-sinir-ağı--advanced-ai-mode-neural-network)  
- [Proje Yapısı / Project Structure](#proje-yapısı--project-structure)  
- [Katkıda Bulunma / Contributing](#katkıda-bulunma--contributing)  
- [Lisans / License](#lisans--license)  

---

## Genel Bakış / Overview
**Türkçe:**  
Bu proje, Pygame ile çizilmiş bir F1 pisti üzerinde otomobil kontrolü simülasyonu sunar.  
- Manuel klavye kontrollü sürüş  
- Popülasyon temelli Genetik Algoritma ile evrimsel öğrenme  
- TensorFlow/Keras tabanlı basit Sinir Ağı  

**English:**  
This project provides a car-control simulation on a Bézier-curve F1 track using Pygame.  
- Manual keyboard-driven driving  
- Evolutionary learning via population-based Genetic Algorithm  
- Simple Neural Network powered by TensorFlow/Keras  

---

## Özellikler / Features
- **Türkçe:** Piste bağlı Bézier eğrileri, beş açılı mesafe sensörleri, canlı hız/tur/fitness metrikleri  
- **English:** Realistic Bézier-curve track, five-angle distance sensors, live speed/lap/fitness metrics  

---

## Kurulum / Installation
1. **Türkçe:** Depoyu klonlayın ve dizine geçin  
   ```bash
   git clone https://github.com/kullanici/proje-adi.git
   cd proje-adi
   ```
2. **English:** Clone the repo and enter the directory  
   ```bash
   git clone https://github.com/youruser/project-name.git
   cd project-name
   ```
3. **Türkçe:** (İsteğe bağlı) Sanal ortam oluşturun ve etkinleştirin  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   .\venv\Scripts\activate     # Windows
   ```
4. **English:** (Optional) Create and activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   .\venv\Scripts\activate     # Windows
   ```
5. **Türkçe:** Gerekli paketleri yükleyin  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. **English:** Install dependencies  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Kullanım / Usage

### Manuel Mod / Manual Mode
**Türkçe:**  
```bash
python main.py
```  
- Ok tuşlarıyla yönlendirin, boşluk ile yeniden başlatın, ESC ile çıkın.  
- `S` tuşuyla eğitim moduna geçiş yapabilirsiniz.

**English:**  
Run:
```bash
python main.py
```  
- Control with arrow keys, restart with SPACE, quit with ESC.  
- Press `S` to toggle training mode.

---

### Eğitim Modu (Genetik Algoritma) / Training Mode (Genetic Algorithm)
- **Türkçe:** `main.py` içindeyken `S` tuşuna bastığınızda genetik algoritma başlar.  
  Ekranda jenerasyon, hayatta kalan araç sayısı ve en iyi fitness gösterilir.  
- **English:** Press `S` in `main.py` to start the genetic algorithm.  
  You'll see generation count, alive cars and best fitness on screen.

---

### Geliştirilmiş AI Modu (Sinir Ağı) / Advanced AI Mode (Neural Network)
**Türkçe:**  
```bash
python ai_enhanced.py
```  
- TensorFlow/Keras tabanlı sinir ağı öğrenmesi.  
- Her jenerasyonda konsolda fitness istatistikleri ve grafik oluşturma imkânı.

**English:**  
Run:
```bash
python ai_enhanced.py
```  
- Neural network learning with TensorFlow/Keras.  
- Fitness stats printed per generation and optional plotting with matplotlib.

---

## Proje Yapısı / Project Structure
    ├── ai_enhanced.py      # Gelişmiş sinir ağı simülasyonu / Advanced neural network simulation
    ├── ai_simulation.py    # Basit genetik algoritma simülasyonu / Simple genetic algorithm simulation
    ├── game.py             # Pygame pist & araç çizim fonksiyonları / Track & car rendering functions
    ├── main.py             # Ana uygulama (manuel + GA modu) / Main application (manual & GA mode)
    ├── requirements.txt    # Proje bağımlılıkları / Project dependencies
    ├── README.md           # İkilidilli kullanım kılavuzu / Bilingual usage guide
    └── test.py             # Bağımlılık ve import testleri / Dependency & import tests

## Katkıda Bulunma / Contributing
- **Türkçe:** Fork'layın, yeni branch açın, değişiklik yapın, PR oluşturun.  
- **English:** Fork the repo, create a branch, commit your changes, open a pull request.

---

## Lisans / License
**Türkçe:** Bu proje MIT Lisansı ile lisanslanmıştır.  
**English:** This project is licensed under the MIT License.  

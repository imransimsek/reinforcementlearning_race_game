import pygame
import math
import numpy as np
from game import *
import json
import os
from datetime import datetime

class YapayOyuncu:
    def __init__(self):
        self.x = 300
        self.y = 400
        self.aci = 0
        self.hiz = 0
        self.tur_sayisi = 0
        self.yasam_suresi = 0
        self.son_checkpoint_zamani = 0
        self.fitness = 0
        self.aktif = True
        self.beyin = np.random.uniform(-1, 1, (5, 3))  # 5 input, 3 output (ileri, sol, sağ)
        self.son_gecis = False
        self.sensor_mesafeler = [0] * 5  # 5 sensör
        
    def sensor_guncelle(self, pist_noktalari):
        # 5 farklı açıda sensör
        sensor_acilar = [-90, -45, 0, 45, 90]
        for i, aci_fark in enumerate(sensor_acilar):
            sensor_aci = math.radians(self.aci + aci_fark)
            self.sensor_mesafeler[i] = self.mesafe_olc(sensor_aci, pist_noktalari)
    
    def mesafe_olc(self, sensor_aci, pist_noktalari):
        # Sensör ışını ile duvar arasındaki mesafeyi ölç
        max_mesafe = 200
        sensor_x = self.x
        sensor_y = self.y
        
        for _ in range(max_mesafe):
            sensor_x += math.cos(sensor_aci)
            sensor_y -= math.sin(sensor_aci)
            
            if not pistte_mi(sensor_x, sensor_y):
                return math.sqrt((self.x - sensor_x)**2 + (self.y - sensor_y)**2)
        
        return max_mesafe
    
    def karar_ver(self):
        # Sensör verilerini normalize et
        inputs = np.array(self.sensor_mesafeler) / 200.0
        
        # Neural network çıktısı
        outputs = np.dot(inputs, self.beyin)
        outputs = 1 / (1 + np.exp(-outputs))  # sigmoid
        
        return outputs > 0.5  # [ileri, sol, sağ]
    
    def fitness_hesapla(self):
        # Fitness = (tur_sayisi * 10000) + yasam_suresi + (toplam_mesafe / 100)
        self.fitness = (self.tur_sayisi * 10000) + self.yasam_suresi

class Jenerasyon:
    def __init__(self, populasyon_sayisi=100):
        self.populasyon_sayisi = populasyon_sayisi
        self.oyuncular = [YapayOyuncu() for _ in range(populasyon_sayisi)]
        self.jenerasyon_no = 1
        self.en_iyi_fitness = 0
        self.aktif_oyuncu_sayisi = populasyon_sayisi
    
    def yeni_jenerasyon_olustur(self):
        # Fitness değerlerine göre sırala
        self.oyuncular.sort(key=lambda x: x.fitness, reverse=True)
        
        # En iyi fitness'ı güncelle
        if self.oyuncular[0].fitness > self.en_iyi_fitness:
            self.en_iyi_fitness = self.oyuncular[0].fitness
        
        # Yeni jenerasyon için en iyi oyuncuları seç
        yeni_oyuncular = []
        
        # En iyi %10'u direkt aktar
        elit_sayisi = self.populasyon_sayisi // 10
        yeni_oyuncular.extend([self.oyuncu_kopyala(oyuncu) for oyuncu in self.oyuncular[:elit_sayisi]])
        
        # Geri kalanı mutasyon ve çaprazlama ile oluştur
        while len(yeni_oyuncular) < self.populasyon_sayisi:
            ebeveyn1 = self.secim_yap()
            ebeveyn2 = self.secim_yap()
            cocuk = self.caprazla(ebeveyn1, ebeveyn2)
            self.mutasyon_uygula(cocuk)
            yeni_oyuncular.append(cocuk)
        
        self.oyuncular = yeni_oyuncular
        self.jenerasyon_no += 1
        self.aktif_oyuncu_sayisi = self.populasyon_sayisi
        
        # Jenerasyon verilerini kaydet
        self.jenerasyon_kaydet()
    
    def secim_yap(self):
        # Turnuva seçimi
        turnuva_boyutu = 5
        turnuva = np.random.choice(self.oyuncular, turnuva_boyutu)
        return max(turnuva, key=lambda x: x.fitness)
    
    def caprazla(self, ebeveyn1, ebeveyn2):
        cocuk = YapayOyuncu()
        # Uniform çaprazlama
        maske = np.random.random(ebeveyn1.beyin.shape) < 0.5
        cocuk.beyin = np.where(maske, ebeveyn1.beyin, ebeveyn2.beyin)
        return cocuk
    
    def mutasyon_uygula(self, oyuncu, mutasyon_orani=0.1):
        mutasyon_maske = np.random.random(oyuncu.beyin.shape) < mutasyon_orani
        oyuncu.beyin[mutasyon_maske] += np.random.normal(0, 0.1, size=np.sum(mutasyon_maske))
    
    def oyuncu_kopyala(self, oyuncu):
        yeni_oyuncu = YapayOyuncu()
        yeni_oyuncu.beyin = oyuncu.beyin.copy()
        return yeni_oyuncu
    
    def jenerasyon_kaydet(self):
        veri = {
            'jenerasyon_no': self.jenerasyon_no,
            'en_iyi_fitness': self.en_iyi_fitness,
            'en_iyi_beyin': self.oyuncular[0].beyin.tolist(),
            'ortalama_fitness': np.mean([o.fitness for o in self.oyuncular]),
            'tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        dosya_adi = f'jenerasyon_{self.jenerasyon_no}.json'
        with open(dosya_adi, 'w') as f:
            json.dump(veri, f)

def simulasyon_baslat():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    clock = pygame.time.Clock()
    
    jenerasyon = Jenerasyon(100)
    max_yasam_suresi = 1000  # Her oyuncu için maksimum yaşam süresi
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        
        # Ekranı temizle
        ekran.fill(YESIL)
        pist_ciz(ekran)
        start_cizgisi_ciz(ekran)
        
        # Her aktif oyuncuyu güncelle
        for oyuncu in jenerasyon.oyuncular:
            if not oyuncu.aktif:
                continue
            
            # Sensörleri güncelle
            oyuncu.sensor_guncelle(pist_noktalari_olustur())
            
            # Yapay zeka kararı
            kararlar = oyuncu.karar_ver()
            
            # Kararları uygula
            if kararlar[0]:  # İleri
                oyuncu.hiz = min(oyuncu.hiz + ivmelenme, max_hiz)
            else:
                oyuncu.hiz = max(0, oyuncu.hiz - sürtünme)
            
            if kararlar[1]:  # Sol
                oyuncu.aci += hesapla_donme_hizi(oyuncu.hiz, max_hiz)
            if kararlar[2]:  # Sağ
                oyuncu.aci -= hesapla_donme_hizi(oyuncu.hiz, max_hiz)
            
            # Pozisyon güncelle
            yeni_x = oyuncu.x + math.cos(math.radians(oyuncu.aci)) * oyuncu.hiz
            yeni_y = oyuncu.y - math.sin(math.radians(oyuncu.aci)) * oyuncu.hiz
            
            # Pist kontrolü
            if pistte_mi(yeni_x, yeni_y):
                oyuncu.x = yeni_x
                oyuncu.y = yeni_y
                
                # Tur kontrolü
                if start_cizgisinden_gecti(yeni_x, yeni_y, oyuncu.x, oyuncu.y):
                    if not oyuncu.son_gecis:
                        oyuncu.tur_sayisi += 1
                        oyuncu.son_checkpoint_zamani = oyuncu.yasam_suresi
                    oyuncu.son_gecis = True
                else:
                    oyuncu.son_gecis = False
            else:
                oyuncu.aktif = False
                jenerasyon.aktif_oyuncu_sayisi -= 1
            
            # Yaşam süresini güncelle
            oyuncu.yasam_suresi += 1
            
            # Maksimum süre kontrolü
            if oyuncu.yasam_suresi >= max_yasam_suresi:
                oyuncu.aktif = False
                jenerasyon.aktif_oyuncu_sayisi -= 1
            
            # Oyuncuyu çiz
            araba_ciz(ekran, oyuncu.x, oyuncu.y, oyuncu.aci)
        
        # Jenerasyon bilgilerini göster
        font = pygame.font.Font(None, 36)
        gen_text = font.render(f'Jenerasyon: {jenerasyon.jenerasyon_no}', True, SIYAH)
        aktif_text = font.render(f'Aktif: {jenerasyon.aktif_oyuncu_sayisi}', True, SIYAH)
        best_text = font.render(f'En İyi Fitness: {jenerasyon.en_iyi_fitness}', True, SIYAH)
        
        ekran.blit(gen_text, (10, 10))
        ekran.blit(aktif_text, (10, 40))
        ekran.blit(best_text, (10, 70))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Jenerasyon bitti mi kontrol et
        if jenerasyon.aktif_oyuncu_sayisi == 0:
            # Fitness değerlerini hesapla
            for oyuncu in jenerasyon.oyuncular:
                oyuncu.fitness_hesapla()
            
            # Yeni jenerasyon oluştur
            jenerasyon.yeni_jenerasyon_olustur()

if __name__ == "__main__":
    simulasyon_baslat() 
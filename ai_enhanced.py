import pygame
import math
import numpy as np
from game import *
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from tensorflow import keras
import seaborn as sns

def hesapla_donme_hizi(hiz, max_hiz):
    """Hıza bağlı dönüş hızını hesaplar"""
    min_donme = 0.8
    max_donme = 2.0
    hiz_orani = hiz / max_hiz
    return max_donme - (hiz_orani * (max_donme - min_donme))

def start_cizgisinden_gecti(x, y, eski_x, eski_y):
    """Start çizgisinden geçişi kontrol eder"""

    if 375 <= y <= 425:  
        if eski_x < 300 and x >= 300:  
            return True
    return False

# Sabitler
max_hiz = 10
min_hiz = 0.2  
ivmelenme = 0.2
sürtünme = 0.05

# Basit sinir ağı implementasyonu
class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.1
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.1
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def predict(self, inputs):
        hidden = self.sigmoid(np.dot(inputs, self.weights1))
        return self.sigmoid(np.dot(hidden, self.weights2))

class GelistirilmisYapayOyuncu:
    def __init__(self):
        self.x = 300
        self.y = 400
        self.aci = 0
        self.hiz = min_hiz  
        self.tur_sayisi = 0
        self.yasam_suresi = 0
        self.fitness = 0
        self.aktif = True
        self.son_gecis = False
        self.hareket_etmeme_sayaci = 0  
        self.son_konum = (self.x, self.y)
        self.sensor_sayisi = 5
        self.sensor_mesafeler = [0] * self.sensor_sayisi
        self.son_pozisyonlar = []
        
        # Neural network
        self.brain = SimpleNeuralNetwork(7, 6, 4)
    
    def sensor_guncelle(self, pist_noktalari):
        sensor_acilar = [-90, -45, 0, 45, 90]
        for i, aci_fark in enumerate(sensor_acilar):
            sensor_aci = math.radians(self.aci + aci_fark)
            self.sensor_mesafeler[i] = self.mesafe_olc(sensor_aci, pist_noktalari)
    
    def mesafe_olc(self, sensor_aci, pist_noktalari):
        max_mesafe = 200
        sensor_x = self.x
        sensor_y = self.y
        adim = 10
        
        for mesafe in range(0, max_mesafe, adim):
            sensor_x += math.cos(sensor_aci) * adim
            sensor_y -= math.sin(sensor_aci) * adim
            if not pistte_mi(sensor_x, sensor_y):
                return mesafe
        return max_mesafe
    
    def karar_ver(self):
        inputs = np.array(self.sensor_mesafeler) / 200.0
        inputs = np.append(inputs, [self.hiz / max_hiz, self.aci / 360.0])
        return self.brain.predict(inputs.reshape(1, -1))[0] > 0.5

    def fitness_hesapla(self):
        """Geliştirilmiş fitness hesaplama"""
        tur_bonus = self.tur_sayisi * 10000
        mesafe_bonus = self.yasam_suresi * self.hiz  
        hareket_cezasi = max(0, self.hareket_etmeme_sayaci * 100)  
        
        self.fitness = tur_bonus + mesafe_bonus - hareket_cezasi

    def hareket_kontrolu(self):
        """Robotun hareket edip etmediğini kontrol eder"""
        mesafe = math.sqrt((self.x - self.son_konum[0])**2 + (self.y - self.son_konum[1])**2)
        if mesafe < 0.5:  # Çok az hareket varsa
            self.hareket_etmeme_sayaci += 1
        else:
            self.hareket_etmeme_sayaci = max(0, self.hareket_etmeme_sayaci - 1)
        
        self.son_konum = (self.x, self.y)
        
       
        if self.hareket_etmeme_sayaci > 100:  
            self.aktif = False
            return False
        return True

class GelistirilmisJenerasyon:
    def __init__(self, populasyon_sayisi=30): 
        self.populasyon_sayisi = populasyon_sayisi
        self.oyuncular = [GelistirilmisYapayOyuncu() for _ in range(populasyon_sayisi)]
        self.jenerasyon_no = 1
        self.en_iyi_fitness = 0
        self.aktif_oyuncu_sayisi = populasyon_sayisi
    
    def veri_analizi_goster(self):
        print(f"Jenerasyon {self.jenerasyon_no}")
        print(f"En iyi fitness: {self.en_iyi_fitness}")
        print(f"Ortalama fitness: {np.mean([o.fitness for o in self.oyuncular])}")

def simulasyon_baslat():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    clock = pygame.time.Clock()
    
    jenerasyon = GelistirilmisJenerasyon(30)
    max_yasam_suresi = 1000
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        
        ekran.fill(YESIL)
        pist_ciz(ekran)
        start_cizgisi_ciz(ekran)
        
        for oyuncu in jenerasyon.oyuncular:
            if not oyuncu.aktif:
                continue
            
            oyuncu.sensor_guncelle(pist_noktalari_olustur())
            kararlar = oyuncu.karar_ver()
            
            # Hız kontrolü güncellendi
            if kararlar[0]:  # İleri
                oyuncu.hiz = min(oyuncu.hiz + ivmelenme, max_hiz)
            else:
                # Minimum hıza kadar yavaşla
                oyuncu.hiz = max(min_hiz, oyuncu.hiz - sürtünme)
            
            donme_hizi = hesapla_donme_hizi(oyuncu.hiz, max_hiz)
            if kararlar[2]:  # Sol
                oyuncu.aci += donme_hizi
            if kararlar[3]:  # Sağ
                oyuncu.aci -= donme_hizi
            
            yeni_x = oyuncu.x + math.cos(math.radians(oyuncu.aci)) * oyuncu.hiz
            yeni_y = oyuncu.y - math.sin(math.radians(oyuncu.aci)) * oyuncu.hiz
            
            if pistte_mi(yeni_x, yeni_y):
                oyuncu.x = yeni_x
                oyuncu.y = yeni_y
                
                # Hareket kontrolü
                if not oyuncu.hareket_kontrolu():
                    jenerasyon.aktif_oyuncu_sayisi -= 1
                    continue
                
                if start_cizgisinden_gecti(yeni_x, yeni_y, oyuncu.x, oyuncu.y):
                    if not oyuncu.son_gecis:
                        oyuncu.tur_sayisi += 1
                    oyuncu.son_gecis = True
                else:
                    oyuncu.son_gecis = False
            else:
                oyuncu.aktif = False
                jenerasyon.aktif_oyuncu_sayisi -= 1
            
            oyuncu.yasam_suresi += 1
            if oyuncu.yasam_suresi >= max_yasam_suresi:
                oyuncu.aktif = False
                jenerasyon.aktif_oyuncu_sayisi -= 1
            
            araba_ciz(ekran, oyuncu.x, oyuncu.y, oyuncu.aci)
            
            # Hız göstergesi eklendi
            font = pygame.font.Font(None, 20)
            hiz_text = font.render(f'{oyuncu.hiz:.1f}', True, SIYAH)
            ekran.blit(hiz_text, (oyuncu.x - 10, oyuncu.y - 20))
        
        # Ekran bilgileri
        font = pygame.font.Font(None, 36)
        gen_text = font.render(f'Jenerasyon: {jenerasyon.jenerasyon_no}', True, SIYAH)
        aktif_text = font.render(f'Aktif: {jenerasyon.aktif_oyuncu_sayisi}', True, SIYAH)
        ekran.blit(gen_text, (10, 10))
        ekran.blit(aktif_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
        
        if jenerasyon.aktif_oyuncu_sayisi == 0:
            for oyuncu in jenerasyon.oyuncular:
                oyuncu.fitness_hesapla()
            jenerasyon.veri_analizi_goster()
            jenerasyon = GelistirilmisJenerasyon(30)

if __name__ == "__main__":
    simulasyon_baslat() 
import gym
from gym import spaces
import numpy as np
import pygame
import math
import random
import pickle
from game import *
import sys

print("PROGRAM BAŞLADI!!!", flush=True)

class ArabaBeyin:
    def __init__(self, input_size=5, hidden_size=8, output_size=2):
        self.weights1 = np.random.randn(input_size, hidden_size)
        self.weights2 = np.random.randn(hidden_size, output_size)
    
    def forward(self, x):
        self.layer1 = np.tanh(np.dot(x, self.weights1))
        self.output = np.tanh(np.dot(self.layer1, self.weights2))
        return self.output
    
    def mutate(self, rate=0.1):
        self.weights1 += np.random.randn(*self.weights1.shape) * rate
        self.weights2 += np.random.randn(*self.weights2.shape) * rate

class F1YarisOrtami(gym.Env):
    def __init__(self, beyin=None):
        super(F1YarisOrtami, self).__init__()
        self.araba_x = 300  
        self.araba_y = 400  
        self.araba_aci = 0
        self.araba_hiz = 2.0 
        self.yasam_suresi = 0
        self.fitness = 0
        self.beyin = beyin if beyin else ArabaBeyin()
        self.hayatta = True
        self.son_kontrol_noktasi = 0  

class Populasyon:
    def __init__(self, boyut=100):
        self.boyut = boyut
        self.arabalar = [F1YarisOrtami() for _ in range(boyut)]
        self.jenerasyon = 1
        self.en_iyi_fitness = 0
        self.hayatta_kalanlar = boyut

def oyunu_sifirla():
    """Oyunu başlangiç durumuna getirir"""
    return {
        'araba_x': 300,  
        'araba_y': 400,  
        'araba_aci': 0,
        'araba_hiz': 0,
        'oyun_devam': True,
        'game_over': False,
        'tur_sayisi': 0,
        'son_gecis': False,
        'en_iyi_tur': 0,
        'baslangic_zamani': pygame.time.get_ticks()
    }

def start_cizgisinden_gecti(x, y, eski_x, eski_y):
    """Start çizgisinden doğru yönde geçişi kontrol eder"""
    
    if 375 <= y <= 425:  
        if eski_x < 300 and x >= 300: 
            return True
    return False

def format_sure(milisaniye):
    saniye = milisaniye // 1000
    dakika = saniye // 60
    saniye = saniye % 60
    milisaniye = milisaniye % 1000
    return f"{dakika:02d}:{saniye:02d}.{milisaniye:03d}"

def hesapla_donme_hizi(hiz, max_hiz):
    """Hiza bağli dönüş hizini hesaplar"""
    min_donme = 0.8  
    max_donme = 2.0 
    
   
    hiz_orani = hiz / max_hiz
    return max_donme - (hiz_orani * (max_donme - min_donme))

def ivmelenme_hesapla(mevcut_hiz, max_hiz):
    """Hiza bağli ivmelenmeyi hesaplar"""
    baslangic_ivme = 0.15  
    son_ivme = 0.05      
    
    
    hiz_orani = mevcut_hiz / max_hiz
    return baslangic_ivme - (hiz_orani * (baslangic_ivme - son_ivme))

def sensor_oku(x, y, aci):
    """Arabanin çevresindeki mesafeleri ölçer"""
    sensor_mesafeler = []
    sensor_acilar = [-90, -45, 0, 45, 90] 
    
    for sensor_aci in sensor_acilar:
        toplam_aci = aci + sensor_aci
        mesafe = 0
        test_x = x
        test_y = y
        
        while mesafe < 200:  
            test_x += math.cos(math.radians(toplam_aci))
            test_y -= math.sin(math.radians(toplam_aci))
            mesafe += 1
            
            if not pistte_mi(test_x, test_y):
                break
        
        sensor_mesafeler.append(mesafe / 200.0)  
    
    return sensor_mesafeler

def yeni_jenerasyon_olustur(populasyon):
    """En iyi arabalari seçer ve yeni nesil oluşturur"""
    
    arabalar = sorted(populasyon.arabalar, key=lambda x: x.fitness, reverse=True)
    
    
    en_iyi_fitness = arabalar[0].fitness
    if en_iyi_fitness > populasyon.en_iyi_fitness:
        populasyon.en_iyi_fitness = en_iyi_fitness
        print(f"Yeni en iyi fitness: {en_iyi_fitness}") 
    
    
    secilen_sayi = max(populasyon.boyut // 5, 1) 
    secilen_arabalar = arabalar[:secilen_sayi]
    
   
    yeni_arabalar = []
    
    for _ in range(populasyon.boyut):
     
        ebeveyn = random.choice(secilen_arabalar) 
        yeni_araba = F1YarisOrtami()
        yeni_araba.beyin.weights1 = ebeveyn.beyin.weights1.copy()
        yeni_araba.beyin.weights2 = ebeveyn.beyin.weights2.copy()
        yeni_araba.beyin.mutate(0.1)
        yeni_arabalar.append(yeni_araba)
    
    populasyon.arabalar = yeni_arabalar

def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    clock = pygame.time.Clock()
    
    font_buyuk = pygame.font.Font(None, 74)
    font_kucuk = pygame.font.Font(None, 36)
    game_over_text = font_buyuk.render('GAME OVER', True, (255, 0, 0))
    restart_text = font_buyuk.render('SPACE to Restart', True, (255, 255, 255))
    
 
    egitim_modu = False
    populasyon = Populasyon(boyut=50)
    durum = oyunu_sifirla()
    
    while durum['oyun_devam']:
        eski_x, eski_y = durum['araba_x'], durum['araba_y']
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                durum['oyun_devam'] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    durum['oyun_devam'] = False
                elif event.key == pygame.K_s:  
                    egitim_modu = not egitim_modu
                    if egitim_modu:
                        populasyon = Populasyon(boyut=50)  
                elif event.key == pygame.K_SPACE and durum['game_over']:
                    durum = oyunu_sifirla()
        
        ekran.fill(YESIL)
        pist_ciz(ekran)
        start_cizgisi_ciz(ekran)
        
        if egitim_modu:
            
            for araba in populasyon.arabalar:
                if araba.hayatta:
                    
                    sensor_veriler = sensor_oku(araba.araba_x, araba.araba_y, araba.araba_aci)
                    
                    kararlar = araba.beyin.forward(np.array(sensor_veriler))
                    
                    donme = kararlar[0] * 2.0
                    hizlanma = (kararlar[1] + 1) / 2 
                    
                    araba.araba_aci += donme
                    araba.araba_hiz = max(2.0, min(max_hiz, araba.araba_hiz + (hizlanma - 0.5)))
                    
                    yeni_x = araba.araba_x + math.cos(math.radians(araba.araba_aci)) * araba.araba_hiz
                    yeni_y = araba.araba_y - math.sin(math.radians(araba.araba_aci)) * araba.araba_hiz
                    
                    if pistte_mi(yeni_x, yeni_y):
                       
                        araba.fitness += araba.araba_hiz * 0.1
                        
                        if start_cizgisinden_gecti(yeni_x, yeni_y, araba.araba_x, araba.araba_y):
                            araba.fitness += 1000  
                        
                        araba.araba_x = yeni_x
                        araba.araba_y = yeni_y
                        araba.yasam_suresi += 1
                    else:
                        araba.hayatta = False
                    
                    if araba.yasam_suresi > 500 and araba.fitness < 10:
                        araba.hayatta = False
                    
                    if araba.hayatta:
                        araba_ciz(ekran, araba.araba_x, araba.araba_y, araba.araba_aci)
            
            
            if not any(araba.hayatta for araba in populasyon.arabalar):
                yeni_jenerasyon_olustur(populasyon)
                populasyon.jenerasyon += 1
            
           
            jenerasyon_text = font_kucuk.render(f'Jenerasyon: {populasyon.jenerasyon}', True, SIYAH)
            hayatta_text = font_kucuk.render(f'Hayatta: {sum(a.hayatta for a in populasyon.arabalar)}', True, SIYAH)
            fitness_text = font_kucuk.render(f'En İyi Fitness: {populasyon.en_iyi_fitness:.1f}', True, SIYAH)
            
            ekran.blit(jenerasyon_text, (10, 10))
            ekran.blit(hayatta_text, (10, 40))
            ekran.blit(fitness_text, (10, 70))
        else:
            
            if not durum['game_over']:
                tuslar = pygame.key.get_pressed()
                
                
                donme_hizi = hesapla_donme_hizi(durum['araba_hiz'], max_hiz)
                
              
                if tuslar[pygame.K_LEFT]:
                    durum['araba_aci'] += donme_hizi
                if tuslar[pygame.K_RIGHT]:
                    durum['araba_aci'] -= donme_hizi
                
                
                if tuslar[pygame.K_UP]:
                    
                    anlik_ivmelenme = ivmelenme_hesapla(durum['araba_hiz'], max_hiz)
                    durum['araba_hiz'] = min(durum['araba_hiz'] + anlik_ivmelenme, max_hiz)
                elif tuslar[pygame.K_DOWN]:
                   
                    durum['araba_hiz'] = max(0, durum['araba_hiz'] - 0.2)
                else:
                    
                    surtunme_etkisi = 0.01 + (durum['araba_hiz'] / max_hiz) * 0.03
                    durum['araba_hiz'] = max(0, durum['araba_hiz'] - surtunme_etkisi)
                
                
                yeni_x = durum['araba_x'] + math.cos(math.radians(durum['araba_aci'])) * durum['araba_hiz']
                yeni_y = durum['araba_y'] - math.sin(math.radians(durum['araba_aci'])) * durum['araba_hiz']
                
                
                if pistte_mi(yeni_x, yeni_y):
                   
                    durum['araba_x'] = yeni_x
                    durum['araba_y'] = yeni_y
                    
                  
                    if start_cizgisinden_gecti(yeni_x, yeni_y, eski_x, eski_y):
                        if not durum['son_gecis']:  
                            durum['tur_sayisi'] += 1
                            if durum['tur_sayisi'] > durum['en_iyi_tur']:
                                durum['en_iyi_tur'] = durum['tur_sayisi']
                        durum['son_gecis'] = True
                    else:
                        durum['son_gecis'] = False
                else:
                    durum['game_over'] = True
            
            araba_ciz(ekran, durum['araba_x'], durum['araba_y'], durum['araba_aci'])
            
        
            hiz_text = font_kucuk.render(f'Hiz: {abs(durum["araba_hiz"]):.1f}', True, SIYAH)
            tur_text = font_kucuk.render(f'Tur: {durum["tur_sayisi"]}', True, SIYAH)
            ekran.blit(hiz_text, (10, 10))
            ekran.blit(tur_text, (10, 40))
        
        
        mod_text = font_kucuk.render('Eğitim Modu: ' + ('Açik' if egitim_modu else 'Kapali'), True, SIYAH)
        ekran.blit(mod_text, (10, YUKSEKLIK - 30))
        
        if durum['game_over']:
            text_rect = game_over_text.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 - 50))
            restart_rect = restart_text.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 + 50))
            ekran.blit(game_over_text, text_rect)
            ekran.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

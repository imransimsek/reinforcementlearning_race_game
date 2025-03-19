print("Game.py başlatılıyor...")

import pygame
import sys
import math


pygame.init()


GENISLIK = 1200
YUKSEKLIK = 800


pist_genislik = 100
kenar_genislik = 15

BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
YESIL = (126, 200, 80)
ACIK_YESIL = (169, 214, 81)
GRI = (128, 128, 128)
TURUNCU_BEYAZ = (255, 99, 71)
KOYU_GRI = (90, 90, 90)
MAVI = (0, 0, 255)
SARI = (255, 255, 0)


araba_genislik = 14
araba_uzunluk = 30
max_hiz = 5.0
ivmelenme = 0.1
sürtünme = 0.03

def bezier_nokta(p0, p1, p2, p3, t):
    return (
        (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0],
        (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
    )

def pist_noktalari_olustur():
    
    kontrol_noktalari = [
       
        [(200, 400), (300, 400), (400, 400), (500, 400)],
        [(500, 400), (600, 400), (600, 200), (700, 200)],
        [(700, 200), (800, 200), (900, 200), (1000, 250)],
        [(1000, 250), (1000, 350), (900, 450), (800, 450)],
        [(800, 450), (700, 450), (600, 500), (500, 600)],
        [(500, 600), (400, 600), (200, 500), (200, 400)]
    ]
    
    pist_noktalari = []
    for curve in kontrol_noktalari:
        for t in range(31):
            t = t / 30
            nokta = bezier_nokta(curve[0], curve[1], curve[2], curve[3], t)
            pist_noktalari.append(nokta)
    
    return pist_noktalari

def pist_ciz(ekran):
    ekran.fill(YESIL)
    
    pist_noktalari = pist_noktalari_olustur()
    
 
    for i in range(len(pist_noktalari) - 1):
        pygame.draw.line(ekran, TURUNCU_BEYAZ, 
                        pist_noktalari[i], pist_noktalari[i + 1], 
                        pist_genislik + kenar_genislik)
    
   
    for i in range(len(pist_noktalari)):
        pygame.draw.circle(ekran, TURUNCU_BEYAZ, 
                         (int(pist_noktalari[i][0]), int(pist_noktalari[i][1])), 
                         (pist_genislik + kenar_genislik) // 2)
    
  
    for i in range(len(pist_noktalari) - 1):
        pygame.draw.line(ekran, KOYU_GRI, 
                        pist_noktalari[i], pist_noktalari[i + 1], 
                        pist_genislik)
    
   
    for i in range(len(pist_noktalari)):
        pygame.draw.circle(ekran, KOYU_GRI, 
                         (int(pist_noktalari[i][0]), int(pist_noktalari[i][1])), 
                         pist_genislik // 2)
    
 
    for i in range(0, len(pist_noktalari) - 1, 4):
        merkez = pist_noktalari[i]
        if i + 1 < len(pist_noktalari):
            sonraki = pist_noktalari[i + 1]
            dx = sonraki[0] - merkez[0]
            dy = sonraki[1] - merkez[1]
            aci = math.atan2(dy, dx)
            cizgi_uzunluk = 20
            
            baslangic = (merkez[0] - cizgi_uzunluk/2 * math.cos(aci),
                        merkez[1] - cizgi_uzunluk/2 * math.sin(aci))
            bitis = (merkez[0] + cizgi_uzunluk/2 * math.cos(aci),
                    merkez[1] + cizgi_uzunluk/2 * math.sin(aci))
            
            pygame.draw.line(ekran, BEYAZ, baslangic, bitis, 3)

def araba_ciz(ekran, x, y, aci):
  
    araba_surface = pygame.Surface((araba_uzunluk, araba_genislik), pygame.SRCALPHA)
    
  
    pygame.draw.rect(araba_surface, (0, 0, 150), 
                    (5, 2, araba_uzunluk-10, araba_genislik-4))
    
 
    pygame.draw.polygon(araba_surface, (30, 144, 255), [
        (araba_uzunluk-10, araba_genislik//2), 
        (araba_uzunluk-15, 2),                  
        (araba_uzunluk-15, araba_genislik-2)   
    ])
    
    pygame.draw.rect(araba_surface, (220, 0, 0),
                    (araba_uzunluk-8, 0, 8, araba_genislik))
    
    pygame.draw.ellipse(araba_surface, (40, 40, 40),
                       (8, araba_genislik//4, 8, araba_genislik//2))
    
    pygame.draw.rect(araba_surface, (220, 0, 0),
                    (0, 0, 5, araba_genislik))
    
    rotated_surface = pygame.transform.rotate(araba_surface, aci)
    rotated_rect = rotated_surface.get_rect(center=(x, y))
    ekran.blit(rotated_surface, rotated_rect)

def pistte_mi(x, y):
    pist_noktalari = pist_noktalari_olustur()
    
    for i in range(len(pist_noktalari) - 1):
        p1 = pist_noktalari[i]
        p2 = pist_noktalari[i + 1]
        
        uzaklik = nokta_cizgi_uzaklik(x, y, p1[0], p1[1], p2[0], p2[1])
        if uzaklik <= pist_genislik / 2:
            return True
    
    return False

def nokta_cizgi_uzaklik(px, py, x1, y1, x2, y2):
    A = px - x1
    B = py - y1
    C = x2 - x1
    D = y2 - y1
    
    dot = A * C + B * D
    len_sq = C * C + D * D
    
    if len_sq == 0:
        return math.sqrt(A * A + B * B)
    
    param = dot / len_sq
    
    if param < 0:
        return math.sqrt(A * A + B * B)
    elif param > 1:
        return math.sqrt((px - x2) * (px - x2) + (py - y2) * (py - y2))
    
    return abs(A * D - C * B) / math.sqrt(len_sq)

def start_cizgisi_ciz(ekran):
    pygame.draw.rect(ekran, BEYAZ, (300, 375, 5, 50))

print("Game.py yükleme tamamlandı")
print("Test başlıyor...")

try:
    import pygame
    print("Pygame import edildi")
    
    print("Game modülünü import etmeye çalışıyorum...")
    import game
    print("Game modülü import edildi")
    
except Exception as e:
    print(f"HATA OLUŞTU: {str(e)}")
    
    import traceback
    print("\nHata detayı:")
    traceback.print_exc()

print("Test tamamlandı")

input("Çıkmak için bir tuşa basın...") 
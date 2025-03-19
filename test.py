print("Test başliyor...")

try:
    import pygame
    print("Pygame import edildi")
    
    print("Game modülünü import etmeye çalişiyorum...")
    import game
    print("Game modülü import edildi")
    
except Exception as e:
    print(f"HATA OLUŞTU: {str(e)}")
    
    import traceback
    print("\nHata detayi:")
    traceback.print_exc()

print("Test tamamlandi")

input("Çikmak için bir tuşa basin...") 
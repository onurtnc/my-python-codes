import tkinter as tk
from tkinter import messagebox
import random

class RacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🏎️ ARABA YARIŞI")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)
        
        # Oyun ayarları
        self.genislik = 400
        self.yukseklik = 600
        self.araba_genislik = 40
        self.araba_yukseklik = 60
        self.dusman_genislik = 40
        self.dusman_yukseklik = 60
        
        # Renkler
        self.yol_renk = "#4a4a4a"
        self.cizgi_renk = "#ffff00"
        self.cimen_renk = "#2ecc71"
        
        # Oyun değişkenleri
        self.araba_x = self.genislik // 2 - self.araba_genislik // 2
        self.araba_y = self.yukseklik - 100
        self.araba_hiz = 15
        
        self.dusmanlar = []
        self.dusman_hiz = 5
        
        self.cizgiler = []
        self.cizgi_hiz = 8
        
        self.skor = 0
        self.en_yuksek_skor = 0
        self.seviye = 1
        self.oyun_devam = False
        
        self.arayuz_olustur()
    
    def arayuz_olustur(self):
        """Oyun arayüzünü oluştur"""
        # Ana çerçeve
        ana_frame = tk.Frame(self.root, bg="#2c3e50")
        ana_frame.pack(padx=20, pady=20)
        
        # Başlık
        baslik = tk.Label(
            ana_frame,
            text="🏎️ ARABA YARIŞI 🏁",
            font=("Arial", 32, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        baslik.pack(pady=10)
        
        # Skor paneli
        skor_frame = tk.Frame(ana_frame, bg="#34495e", relief=tk.RAISED, borderwidth=3)
        skor_frame.pack(fill=tk.X, pady=10)
        
        # Skor bilgileri
        bilgi_frame = tk.Frame(skor_frame, bg="#34495e")
        bilgi_frame.pack(pady=10)
        
        self.skor_label = tk.Label(
            bilgi_frame,
            text=f"🏆 SKOR: {self.skor}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#f39c12"
        )
        self.skor_label.pack(side=tk.LEFT, padx=15)
        
        self.en_yuksek_skor_label = tk.Label(
            bilgi_frame,
            text=f"⭐ REKOR: {self.en_yuksek_skor}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#3498db"
        )
        self.en_yuksek_skor_label.pack(side=tk.LEFT, padx=15)
        
        self.seviye_label = tk.Label(
            bilgi_frame,
            text=f"📊 SEVİYE: {self.seviye}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#2ecc71"
        )
        self.seviye_label.pack(side=tk.LEFT, padx=15)
        
        # Canvas (Oyun alanı)
        self.canvas = tk.Canvas(
            ana_frame,
            width=self.genislik,
            height=self.yukseklik,
            bg=self.yol_renk,
            highlightthickness=3,
            highlightbackground="#e74c3c"
        )
        self.canvas.pack()
        
        # Çimen kenarları
        self.canvas.create_rectangle(
            0, 0, 50, self.yukseklik,
            fill=self.cimen_renk, outline=""
        )
        self.canvas.create_rectangle(
            self.genislik - 50, 0, self.genislik, self.yukseklik,
            fill=self.cimen_renk, outline=""
        )
        
        # Yol çizgileri oluştur
        self.yol_cizgileri_olustur()
        
        # Oyuncu arabası
        self.araba = self.araba_olustur(self.araba_x, self.araba_y, "#e74c3c")
        
        # Kontrol bilgisi
        kontrol_label = tk.Label(
            ana_frame,
            text="🎮 YÖN TUŞLARI: ⬅️ ➡️  |  BOŞLUK: BAŞLAT  |  ESC: ÇIKIŞ",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        kontrol_label.pack(pady=10)
        
        # Başlangıç mesajı
        self.mesaj_text = self.canvas.create_text(
            self.genislik // 2,
            self.yukseklik // 2,
            text="BAŞLAMAK İÇİN\nBOŞLUK TUŞUNA BASIN",
            font=("Arial", 20, "bold"),
            fill="white",
            justify=tk.CENTER
        )
        
        # Klavye kontrolleri
        self.root.bind("<Left>", lambda e: self.hareket_et("Left"))
        self.root.bind("<Right>", lambda e: self.hareket_et("Right"))
        self.root.bind("<space>", lambda e: self.oyun_baslat())
        self.root.bind("<Escape>", lambda e: self.root.quit())
        
        # A ve D tuşları (alternatif)
        self.root.bind("a", lambda e: self.hareket_et("Left"))
        self.root.bind("d", lambda e: self.hareket_et("Right"))
    
    def araba_olustur(self, x, y, renk):
        """Araba şekli oluştur"""
        araba_parcalari = []
        
        # Ana gövde
        govde = self.canvas.create_rectangle(
            x, y, x + self.araba_genislik, y + self.araba_yukseklik,
            fill=renk, outline="black", width=2
        )
        araba_parcalari.append(govde)
        
        # Ön cam
        cam = self.canvas.create_rectangle(
            x + 5, y + 10, x + self.araba_genislik - 5, y + 25,
            fill="#87ceeb", outline="black", width=1
        )
        araba_parcalari.append(cam)
        
        # Arka cam
        cam2 = self.canvas.create_rectangle(
            x + 5, y + 35, x + self.araba_genislik - 5, y + 50,
            fill="#87ceeb", outline="black", width=1
        )
        araba_parcalari.append(cam2)
        
        return araba_parcalari
    
    def yol_cizgileri_olustur(self):
        """Yol çizgilerini oluştur"""
        cizgi_sayisi = 10
        cizgi_yukseklik = 40
        bosluk = 40
        
        for i in range(cizgi_sayisi):
            y = i * (cizgi_yukseklik + bosluk) - 300
            cizgi = self.canvas.create_rectangle(
                self.genislik // 2 - 3,
                y,
                self.genislik // 2 + 3,
                y + cizgi_yukseklik,
                fill=self.cizgi_renk,
                outline=""
            )
            self.cizgiler.append(cizgi)
    
    def dusman_olustur(self):
        """Düşman araba oluştur"""
        # Rastgele şerit seç (3 şerit var)
        seritler = [70, 180, 290]
        x = random.choice(seritler)
        y = -self.dusman_yukseklik
        
        renkler = ["#3498db", "#9b59b6", "#f39c12", "#1abc9c", "#34495e"]
        renk = random.choice(renkler)
        
        dusman = self.araba_olustur(x, y, renk)
        self.dusmanlar.append({"parcalar": dusman, "x": x, "y": y})
    
    def oyun_baslat(self):
        """Oyunu başlat"""
        if not self.oyun_devam:
            self.oyun_devam = True
            self.canvas.delete(self.mesaj_text)
            self.oyun_dongusu()
    
    def hareket_et(self, yon):
        """Arabayı hareket ettir"""
        if not self.oyun_devam:
            return
        
        if yon == "Left" and self.araba_x > 60:
            self.araba_x -= self.araba_hiz
            for parca in self.araba:
                self.canvas.move(parca, -self.araba_hiz, 0)
        
        elif yon == "Right" and self.araba_x < self.genislik - 50 - self.araba_genislik:
            self.araba_x += self.araba_hiz
            for parca in self.araba:
                self.canvas.move(parca, self.araba_hiz, 0)
    
    def yol_cizgilerini_hareket_ettir(self):
        """Yol çizgilerini aşağı hareket ettir"""
        for cizgi in self.cizgiler:
            coords = self.canvas.coords(cizgi)
            if coords[1] > self.yukseklik:
                self.canvas.move(cizgi, 0, -800)
            else:
                self.canvas.move(cizgi, 0, self.cizgi_hiz)
    
    def dusmanlari_hareket_ettir(self):
        """Düşman arabaları hareket ettir"""
        for dusman in self.dusmanlar[:]:
            dusman["y"] += self.dusman_hiz
            
            # Düşmanı hareket ettir
            for parca in dusman["parcalar"]:
                self.canvas.move(parca, 0, self.dusman_hiz)
            
            # Ekrandan çıktıysa sil ve skor ekle
            if dusman["y"] > self.yukseklik:
                for parca in dusman["parcalar"]:
                    self.canvas.delete(parca)
                self.dusmanlar.remove(dusman)
                self.skor_ekle()
    
    def carpishma_kontrol(self):
        """Çarpışma kontrolü"""
        for dusman in self.dusmanlar:
            dx = dusman["x"]
            dy = dusman["y"]
            
            # Basit çarpışma tespiti
            if (self.araba_x < dx + self.dusman_genislik and
                self.araba_x + self.araba_genislik > dx and
                self.araba_y < dy + self.dusman_yukseklik and
                self.araba_y + self.araba_yukseklik > dy):
                return True
        return False
    
    def skor_ekle(self):
        """Skor ekle"""
        self.skor += 10
        self.skor_label.config(text=f"🏆 SKOR: {self.skor}")
        
        # Seviye atla
        if self.skor % 100 == 0:
            self.seviye += 1
            self.seviye_label.config(text=f"📊 SEVİYE: {self.seviye}")
            self.dusman_hiz += 1
            self.cizgi_hiz += 1
    
    def oyun_bitti(self):
        """Oyun bitti"""
        self.oyun_devam = False
        
        # En yüksek skoru güncelle
        if self.skor > self.en_yuksek_skor:
            self.en_yuksek_skor = self.skor
            self.en_yuksek_skor_label.config(text=f"⭐ REKOR: {self.en_yuksek_skor}")
        
        # Oyun bitti mesajı
        self.mesaj_text = self.canvas.create_text(
            self.genislik // 2,
            self.yukseklik // 2,
            text=f"OYUN BİTTİ!\n\nSKOR: {self.skor}\n\nYENİ OYUN İÇİN\nBOŞLUK TUŞUNA BASIN",
            font=("Arial", 18, "bold"),
            fill="white",
            justify=tk.CENTER
        )
        
        # Düşmanları temizle
        for dusman in self.dusmanlar:
            for parca in dusman["parcalar"]:
                self.canvas.delete(parca)
        self.dusmanlar.clear()
        
        # Değişkenleri sıfırla
        self.skor = 0
        self.seviye = 1
        self.dusman_hiz = 5
        self.cizgi_hiz = 8
        
        self.skor_label.config(text=f"🏆 SKOR: {self.skor}")
        self.seviye_label.config(text=f"📊 SEVİYE: {self.seviye}")
        
        # Arabayı başlangıç pozisyonuna al
        dx = (self.genislik // 2 - self.araba_genislik // 2) - self.araba_x
        for parca in self.araba:
            self.canvas.move(parca, dx, 0)
        self.araba_x = self.genislik // 2 - self.araba_genislik // 2
    
    def oyun_dongusu(self):
        """Ana oyun döngüsü"""
        if not self.oyun_devam:
            return
        
        # Yol çizgilerini hareket ettir
        self.yol_cizgilerini_hareket_ettir()
        
        # Düşman oluştur (rastgele)
        if random.randint(1, 30) == 1:
            self.dusman_olustur()
        
        # Düşmanları hareket ettir
        self.dusmanlari_hareket_ettir()
        
        # Çarpışma kontrolü
        if self.carpishma_kontrol():
            self.oyun_bitti()
            return
        
        # Döngüyü tekrarla
        self.root.after(50, self.oyun_dongusu)


if __name__ == "__main__":
    root = tk.Tk()
    oyun = RacingGame(root)
    root.mainloop()

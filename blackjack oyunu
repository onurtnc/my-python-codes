import tkinter as tk
from tkinter import messagebox
import random

class Blackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 21 (BLACKJACK) OYUNU")
        self.root.geometry("800x700")
        self.root.configure(bg="#1a5f3f")
        self.root.resizable(False, False)
        
        # Oyun değişkenleri
        self.deste = []
        self.oyuncu_kartlar = []
        self.kasa_kartlar = []
        self.oyuncu_puan = 0
        self.kasa_puan = 0
        self.para = 1000
        self.bahis = 0
        self.oyun_bitti = False
        
        # Kart sembolleri
        self.semboller = ['♠', '♥', '♦', '♣']
        self.degerler = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        self.arayuz_olustur()
        self.yeni_oyun()
    
    def arayuz_olustur(self):
        """Oyun arayüzünü oluştur"""
        # Başlık
        baslik = tk.Label(
            self.root,
            text="🎰 21 (BLACKJACK) 🎰",
            font=("Arial", 28, "bold"),
            bg="#1a5f3f",
            fg="gold"
        )
        baslik.pack(pady=20)
        
        # Para ve bahis bilgisi
        self.bilgi_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.bilgi_frame.pack(pady=10)
        
        self.para_label = tk.Label(
            self.bilgi_frame,
            text=f"💰 Para: ${self.para}",
            font=("Arial", 16, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        self.para_label.pack(side=tk.LEFT, padx=20)
        
        self.bahis_label = tk.Label(
            self.bilgi_frame,
            text=f"🎲 Bahis: ${self.bahis}",
            font=("Arial", 16, "bold"),
            bg="#1a5f3f",
            fg="yellow"
        )
        self.bahis_label.pack(side=tk.LEFT, padx=20)
        
        # Kasa kartları alanı
        kasa_baslik = tk.Label(
            self.root,
            text="🏦 KASA",
            font=("Arial", 18, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        kasa_baslik.pack(pady=5)
        
        self.kasa_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.kasa_frame.pack(pady=10)
        
        self.kasa_puan_label = tk.Label(
            self.root,
            text="Puan: ?",
            font=("Arial", 14),
            bg="#1a5f3f",
            fg="white"
        )
        self.kasa_puan_label.pack()
        
        # Oyuncu kartları alanı
        oyuncu_baslik = tk.Label(
            self.root,
            text="👤 SİZ",
            font=("Arial", 18, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        oyuncu_baslik.pack(pady=5)
        
        self.oyuncu_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.oyuncu_frame.pack(pady=10)
        
        self.oyuncu_puan_label = tk.Label(
            self.root,
            text="Puan: 0",
            font=("Arial", 14),
            bg="#1a5f3f",
            fg="white"
        )
        self.oyuncu_puan_label.pack()
        
        # Bahis girişi
        bahis_frame = tk.Frame(self.root, bg="#1a5f3f")
        bahis_frame.pack(pady=15)
        
        tk.Label(
            bahis_frame,
            text="Bahis Miktarı:",
            font=("Arial", 12),
            bg="#1a5f3f",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.bahis_entry = tk.Entry(bahis_frame, font=("Arial", 12), width=10)
        self.bahis_entry.pack(side=tk.LEFT, padx=5)
        self.bahis_entry.insert(0, "50")
        
        # Butonlar
        buton_frame = tk.Frame(self.root, bg="#1a5f3f")
        buton_frame.pack(pady=10)
        
        self.bahis_buton = tk.Button(
            buton_frame,
            text="💵 BAHIS KOY",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.bahis_koy
        )
        self.bahis_buton.pack(side=tk.LEFT, padx=5)
        
        self.kart_cek_buton = tk.Button(
            buton_frame,
            text="🃏 KART ÇEK",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.kart_cek,
            state=tk.DISABLED
        )
        self.kart_cek_buton.pack(side=tk.LEFT, padx=5)
        
        self.dur_buton = tk.Button(
            buton_frame,
            text="✋ DUR",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=12,
            command=self.dur,
            state=tk.DISABLED
        )
        self.dur_buton.pack(side=tk.LEFT, padx=5)
        
        self.yeni_oyun_buton = tk.Button(
            buton_frame,
            text="🔄 YENİ OYUN",
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            width=12,
            command=self.yeni_oyun
        )
        self.yeni_oyun_buton.pack(side=tk.LEFT, padx=5)
        
        # Mesaj alanı
        self.mesaj_label = tk.Label(
            self.root,
            text="Bahis koyarak oyuna başlayın!",
            font=("Arial", 14, "bold"),
            bg="#1a5f3f",
            fg="yellow"
        )
        self.mesaj_label.pack(pady=10)
    
    def deste_olustur(self):
        """Yeni bir deste oluştur"""
        self.deste = []
        for sembol in self.semboller:
            for deger in self.degerler:
                self.deste.append(f"{deger}{sembol}")
        random.shuffle(self.deste)
    
    def kart_degeri(self, kart):
        """Kartın değerini hesapla"""
        deger = kart[:-1]  # Son karakter sembol
        if deger in ['J', 'Q', 'K']:
            return 10
        elif deger == 'A':
            return 11  # As başta 11, gerekirse 1 olacak
        else:
            return int(deger)
    
    def puan_hesapla(self, kartlar):
        """El puanını hesapla"""
        puan = 0
        as_sayisi = 0
        
        for kart in kartlar:
            deger = self.kart_degeri(kart)
            puan += deger
            if kart[:-1] == 'A':
                as_sayisi += 1
        
        # As'ları ayarla (21'i geçiyorsa 11 yerine 1 say)
        while puan > 21 and as_sayisi > 0:
            puan -= 10
            as_sayisi -= 1
        
        return puan
    
    def kart_goster(self, frame, kartlar, gizli=False):
        """Kartları ekranda göster"""
        # Eski kartları temizle
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Yeni kartları göster
        for i, kart in enumerate(kartlar):
            if gizli and i == 0:
                # Kasanın ilk kartını gizle
                kart_label = tk.Label(
                    frame,
                    text="🂠",
                    font=("Arial", 48),
                    bg="#1a5f3f",
                    fg="white"
                )
            else:
                # Kart rengini belirle
                if kart[-1] in ['♥', '♦']:
                    renk = "red"
                else:
                    renk = "black"
                
                kart_label = tk.Label(
                    frame,
                    text=kart,
                    font=("Arial", 36),
                    bg="white",
                    fg=renk,
                    width=3,
                    height=2,
                    relief=tk.RAISED,
                    borderwidth=3
                )
            kart_label.pack(side=tk.LEFT, padx=5)
    
    def bahis_koy(self):
        """Bahis koy ve oyunu başlat"""
        try:
            bahis = int(self.bahis_entry.get())
            
            if bahis <= 0:
                messagebox.showerror("Hata", "Bahis 0'dan büyük olmalı!")
                return
            
            if bahis > self.para:
                messagebox.showerror("Hata", "Yetersiz bakiye!")
                return
            
            self.bahis = bahis
            self.para -= bahis
            self.bahis_label.config(text=f"🎲 Bahis: ${self.bahis}")
            self.para_label.config(text=f"💰 Para: ${self.para}")
            
            # Oyunu başlat
            self.oyun_baslat()
            
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir bahis miktarı girin!")
    
    def oyun_baslat(self):
        """Oyunu başlat"""
        self.deste_olustur()
        self.oyuncu_kartlar = []
        self.kasa_kartlar = []
        self.oyun_bitti = False
        
        # İlk kartları dağıt
        self.oyuncu_kartlar.append(self.deste.pop())
        self.kasa_kartlar.append(self.deste.pop())
        self.oyuncu_kartlar.append(self.deste.pop())
        self.kasa_kartlar.append(self.deste.pop())
        
        # Puanları hesapla
        self.oyuncu_puan = self.puan_hesapla(self.oyuncu_kartlar)
        self.kasa_puan = self.puan_hesapla(self.kasa_kartlar)
        
        # Kartları göster
        self.kart_goster(self.oyuncu_frame, self.oyuncu_kartlar)
        self.kart_goster(self.kasa_frame, self.kasa_kartlar, gizli=True)
        
        # Puanları güncelle
        self.oyuncu_puan_label.config(text=f"Puan: {self.oyuncu_puan}")
        self.kasa_puan_label.config(text="Puan: ?")
        
        # Butonları aktif et
        self.bahis_buton.config(state=tk.DISABLED)
        self.kart_cek_buton.config(state=tk.NORMAL)
        self.dur_buton.config(state=tk.NORMAL)
        
        self.mesaj_label.config(text="Kart çekin veya durun!")
        
        # Blackjack kontrolü
        if self.oyuncu_puan == 21:
            self.mesaj_label.config(text="🎉 BLACKJACK! 🎉")
            self.oyun_bitir()
    
    def kart_cek(self):
        """Oyuncu kart çeker"""
        if self.oyun_bitti:
            return
        
        self.oyuncu_kartlar.append(self.deste.pop())
        self.oyuncu_puan = self.puan_hesapla(self.oyuncu_kartlar)
        
        self.kart_goster(self.oyuncu_frame, self.oyuncu_kartlar)
        self.oyuncu_puan_label.config(text=f"Puan: {self.oyuncu_puan}")
        
        if self.oyuncu_puan > 21:
            self.mesaj_label.config(text="💥 YANDI! 21'i geçtiniz!")
            self.oyun_bitir()
        elif self.oyuncu_puan == 21:
            self.dur()
    
    def dur(self):
        """Oyuncu durur, kasa oynar"""
        if self.oyun_bitti:
            return
        
        # Kasanın kartlarını göster
        self.kart_goster(self.kasa_frame, self.kasa_kartlar)
        self.kasa_puan_label.config(text=f"Puan: {self.kasa_puan}")
        
        # Kasa 17'ye kadar kart çeker
        while self.kasa_puan < 17:
            self.root.update()
            self.root.after(500)  # Animasyon için bekle
            
            self.kasa_kartlar.append(self.deste.pop())
            self.kasa_puan = self.puan_hesapla(self.kasa_kartlar)
            
            self.kart_goster(self.kasa_frame, self.kasa_kartlar)
            self.kasa_puan_label.config(text=f"Puan: {self.kasa_puan}")
        
        self.oyun_bitir()
    
    def oyun_bitir(self):
        """Oyunu bitir ve kazananı belirle"""
        self.oyun_bitti = True
        
        # Kasanın tüm kartlarını göster
        self.kart_goster(self.kasa_frame, self.kasa_kartlar)
        self.kasa_puan_label.config(text=f"Puan: {self.kasa_puan}")
        
        # Kazananı belirle
        if self.oyuncu_puan > 21:
            mesaj = "💥 YANDI! Kaybettiniz!"
            kazanc = 0
        elif self.kasa_puan > 21:
            mesaj = "🎉 KAZANDINIZ! Kasa yandı!"
            kazanc = self.bahis * 2
        elif self.oyuncu_puan > self.kasa_puan:
            mesaj = "🎉 KAZANDINIZ!"
            kazanc = self.bahis * 2
        elif self.oyuncu_puan < self.kasa_puan:
            mesaj = "😞 KAYBETTİNİZ!"
            kazanc = 0
        else:
            mesaj = "🤝 BERABERE!"
            kazanc = self.bahis
        
        # Blackjack bonusu
        if self.oyuncu_puan == 21 and len(self.oyuncu_kartlar) == 2:
            mesaj = "🎰 BLACKJACK! 1.5x Kazanç!"
            kazanc = int(self.bahis * 2.5)
        
        self.para += kazanc
        
        self.mesaj_label.config(text=mesaj)
        self.para_label.config(text=f"💰 Para: ${self.para}")
        
        # Butonları güncelle
        self.kart_cek_buton.config(state=tk.DISABLED)
        self.dur_buton.config(state=tk.DISABLED)
        self.bahis_buton.config(state=tk.NORMAL)
        
        # Para bitti mi?
        if self.para <= 0:
            messagebox.showinfo("Oyun Bitti", "Paranız bitti! Oyun sıfırlanıyor...")
            self.para = 1000
            self.para_label.config(text=f"💰 Para: ${self.para}")
    
    def yeni_oyun(self):
        """Yeni oyun başlat"""
        self.oyuncu_kartlar = []
        self.kasa_kartlar = []
        self.bahis = 0
        self.oyun_bitti = False
        
        # Kartları temizle
        for widget in self.oyuncu_frame.winfo_children():
            widget.destroy()
        for widget in self.kasa_frame.winfo_children():
            widget.destroy()
        
        # Puanları sıfırla
        self.oyuncu_puan_label.config(text="Puan: 0")
        self.kasa_puan_label.config(text="Puan: ?")
        self.bahis_label.config(text="🎲 Bahis: $0")
        
        # Butonları güncelle
        self.bahis_buton.config(state=tk.NORMAL)
        self.kart_cek_buton.config(state=tk.DISABLED)
        self.dur_buton.config(state=tk.DISABLED)
        
        self.mesaj_label.config(text="Bahis koyarak oyuna başlayın!")


if __name__ == "__main__":
    root = tk.Tk()
    oyun = Blackjack(root)
    root.mainloop()

import socket
from datetime import datetime

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.open_ports = []
        
        # Yaygın portlar ve servisleri
        self.common_ports = {
            20: "FTP Data",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP Proxy",
            8443: "HTTPS Alt",
            27017: "MongoDB"
        }
    
    def get_ip(self):
        """Hedef domain'i IP adresine çevir"""
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror:
            print(f"HATA: '{self.target}' cozumlenemedi!")
            return None
    
    def scan_port(self, port):
        """Tek bir portu tara"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                service = self.common_ports.get(port, "Bilinmiyor")
                self.open_ports.append((port, service))
                print(f"[+] Port {port} ACIK - {service}")
                sock.close()
                return True
            
            sock.close()
            return False
            
        except socket.error:
            return False
        except Exception as e:
            return False
    
    def scan(self):
        """Ana tarama fonksiyonu"""
        print("=" * 60)
        print("PORT TARAYICI - PYTHON")
        print("=" * 60)
        
        # IP adresini al
        ip = self.get_ip()
        if not ip:
            return
        
        print(f"Hedef: {self.target} ({ip})")
        print(f"Port Araligi: {self.start_port} - {self.end_port}")
        print(f"Timeout: {self.timeout} saniye")
        print(f"Baslangic Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        start_time = datetime.now()
        
        # Portları tara
        total_ports = self.end_port - self.start_port + 1
        scanned = 0
        
        for port in range(self.start_port, self.end_port + 1):
            self.scan_port(port)
            scanned += 1
            
            # İlerleme göster (her 50 portta bir)
            if scanned % 50 == 0:
                progress = (scanned / total_ports) * 100
                print(f"[*] Ilerleme: {scanned}/{total_ports} ({progress:.1f}%)")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Sonuçları göster
        self.show_results(duration)
    
    def show_results(self, duration):
        """Tarama sonuçlarını göster"""
        print("\n" + "=" * 60)
        print("TARAMA SONUCLARI")
        print("=" * 60)
        
        if self.open_ports:
            # Açık portları sırala
            self.open_ports.sort()
            
            print(f"\n[+] Toplam {len(self.open_ports)} acik port bulundu:\n")
            print(f"{'PORT':<10} {'SERVIS':<20} {'DURUM'}")
            print("-" * 60)
            
            for port, service in self.open_ports:
                print(f"{port:<10} {service:<20} ACIK")
            
            print("-" * 60)
        else:
            print("\n[-] Acik port bulunamadi!")
        
        print(f"\nTarama Suresi: {duration:.2f} saniye")
        print(f"Taranan Port Sayisi: {self.end_port - self.start_port + 1}")
        print("=" * 60)
    
    def quick_scan(self):
        """Sadece yaygın portları tara"""
        print("=" * 60)
        print("HIZLI TARAMA - YAYGIN PORTLAR")
        print("=" * 60)
        
        ip = self.get_ip()
        if not ip:
            return
        
        print(f"Hedef: {self.target} ({ip})")
        print(f"Baslangic Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        start_time = datetime.now()
        
        # Sadece yaygın portları tara
        port_list = sorted(self.common_ports.keys())
        
        for port in port_list:
            self.scan_port(port)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.show_results(duration)


def main():
    print("=" * 60)
    print("       IP/PORT TARAYICI - PYTHON")
    print("=" * 60)
    print()
    
    # Hedef IP/Domain al
    target = input("Hedef IP veya Domain girin (ornek: scanme.nmap.org): ").strip()
    
    if not target:
        print("HATA: Hedef bos olamaz!")
        return
    
    print("\nTarama Modu Secin:")
    print("1. Hizli Tarama (Yaygin portlar)")
    print("2. Belirli Port Araligi")
    print("3. Standart Tarama (1-1024)")
    
    mode = input("\nSeciminiz (1-3): ").strip()
    
    if mode == "1":
        # Hızlı tarama
        scanner = PortScanner(target, timeout=0.5)
        scanner.quick_scan()
        
    elif mode == "2":
        # Özel aralık
        try:
            start = int(input("Baslangic portu (ornek: 1): "))
            end = int(input("Bitis portu (ornek: 100): "))
            
            if start < 1 or end > 65535 or start > end:
                print("HATA: Gecersiz port araligi!")
                return
            
            if end - start > 1000:
                print("UYARI: Cok fazla port! Maksimum 1000 port taranabilir.")
                return
            
            timeout = float(input("Timeout suresi saniye (ornek: 1): ") or "1")
            
            scanner = PortScanner(target, start, end, timeout)
            scanner.scan()
            
        except ValueError:
            print("HATA: Gecersiz giris!")
            return
    
    elif mode == "3":
        # Standart tarama
        scanner = PortScanner(target, 1, 1024, timeout=1)
        scanner.scan()
    
    else:
        print("HATA: Gecersiz secim!")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTarama kullanici tarafindan durduruldu!")
    except Exception as e:
        print(f"\nHATA: {e}")

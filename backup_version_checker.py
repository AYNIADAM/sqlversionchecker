import os
import struct

SQL_BACKUP_VERSIONS = {
    655: "SQL Server 2008",
    661: "SQL Server 2008 R2",
    706: "SQL Server 2012",
    782: "SQL Server 2014",
    852: "SQL Server 2016",
    868: "SQL Server 2017",
    869: "SQL Server 2017 (Rev)",
    904: "SQL Server 2019",
    957: "SQL Server 2022"
}

def read_bytes_at(file, offset, size):
    file.seek(offset)
    return file.read(size)

def get_backup_version(file_path):
    """
    Dosya yolunu alır, SQL Server backup dosyası ise (bak/bck),
    sürüm kodunu ve sürüm adını döndürür.
    Dönüş: (result: str, version: str) -> (Başarılı/Başarısız, Sürüm adı veya hata)
    """
    if not os.path.isfile(file_path):
        return ("Başarısız", "Dosya bulunamadı")

    try:
        with open(file_path, 'rb') as f:
            header = read_bytes_at(f, 0, 4096)  # İlk 4 KB yeterli

            if not header.startswith(b'TAPE'):
                return ("Başarısız", "Geçersiz yedek dosyası (TAPE imzası yok)")

            # Bilinen versiyon araması
            version_code = None
            for i in range(len(header) - 2):
                candidate = struct.unpack('<H', header[i:i+2])[0]
                if candidate in SQL_BACKUP_VERSIONS:
                    version_code = candidate
                    break

            if version_code:
                return ("Başarılı", f"{SQL_BACKUP_VERSIONS[version_code]} ({version_code})")
            else:
                return ("Başarılı", "Bilinmeyen Sürüm (Geçerli SQL Server yedeği)")

    except Exception as e:
        return ("Başarısız", f"Hata: {e}")

# Komut satırından çalıştırma
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SQL Server BAK/BCK dosyasının sürümünü belirler.")
    parser.add_argument("filepath", help="Yedek (.bak/.bck) dosyasının yolu")
    args = parser.parse_args()
    result, version = get_backup_version(args.filepath)
    print(f"Sonuç: {result}, Sürüm: {version}")

import os
import struct

# SQL Server sürüm kodları haritası
SQL_SERVER_VERSIONS = {
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

# Dosyada kontrol edilecek offset
VERSION_OFFSET = 0x12064

def check_mdf_version(file_path):
    if not os.path.isfile(file_path):
        print(f"Hata: Dosya bulunamadı: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f:
            f.seek(VERSION_OFFSET)
            version_bytes = f.read(2)
            if len(version_bytes) < 2:
                print("Dosya geçerli değil veya çok küçük.")
                return

            # Little-endian olarak short int oku
            version_code = struct.unpack('<H', version_bytes)[0]

            # Sürüm eşleşmesi kontrolü
            if version_code in SQL_SERVER_VERSIONS:
                print(f"Dosya: {os.path.basename(file_path)}")
                print(f"SQL Server Sürümü: {SQL_SERVER_VERSIONS[version_code]} ({version_code})")
            else:
                print(f"Dosya: {os.path.basename(file_path)}")
                print(f"Tanımlanamayan versiyon kodu bulundu: {version_code} (Hex: {version_code:04X})")

    except Exception as e:
        print(f"İşlem sırasında hata oluştu: {e}")

# Örnek kullanım
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SQL Server MDF dosyasının versiyonunu belirler.")
    parser.add_argument("filepath", help="Kontrol edilecek .mdf dosyasının yolu")
    args = parser.parse_args()

    check_mdf_version(args.filepath)

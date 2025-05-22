
# SQL DATA Version Checker

## English Description

[![Download Setup](https://img.shields.io/badge/⬇️%20Download%20Setup-SQLVersionChecker_Setup.exe-blue?style=for-the-badge&logo=windows)](https://github.com/AYNIADAM/sqlversionchecker/releases/latest)

Modern, multi-language desktop app for batch SQL Server MDF, BAK, and BCK file version detection and health check.

This application is designed for IT professionals and database administrators who need to quickly and reliably identify the version and integrity of large numbers of SQL Server data and backup files. It not only finds all relevant files in the selected folder and its subfolders, but also tests each file, detects its SQL Server version, and distinguishes between healthy and corrupted files. Results can be filtered, and batch actions can be performed for efficient management.

### Features
- Scans selected folder and all subfolders to find every `.mdf`, `.bak`, and `.bck` file
- Tests each file to detect its SQL Server version and checks file health (healthy/corrupted)
- Clearly separates and marks healthy and corrupted files in the results
- Batch version checking and result filtering (by status, file type, etc.)
- Modern dashboard UI with SVG/PNG icons
- Batch move and delete operations (preserves original folder structure, prevents overwriting)
- CPU/RAM friendly, stable operation with progress bar and responsive interface
- Multi-language support (Turkish/English, flag selector at top right)
- Result filtering, batch select, and progress tracking for large datasets

---

### File Descriptions

| File/Folder                | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `main.py`                  | Main application file. Starts the GUI and manages the overall workflow.      |
| `mdf_version_checker.py`   | Module for detecting SQL Server version and health of MDF files.             |
| `backup_version_checker.py`| Module for detecting SQL Server version and health of BAK/BCK files.         |
| `ui/`                      | Contains GUI components and dashboard logic.                                |
| `ui/dashboard.py`          | Main dashboard and user interface logic.                                    |
| `icons/`                   | Contains SVG/PNG icons and flag images used in the GUI.                     |
| `core/`                    | Core modules and initializations.                                           |
| `requirements.txt`         | List of required Python packages.                                           |
| `README.md`                | Project description and usage instructions.                                 |
| `.gitignore`               | Specifies files and folders to be ignored by Git.                           |
| `LICENSE`                  | Project license (MIT).                                                      |

---

## Türkçe Açıklama

[![Kurulum Dosyasını İndir](https://img.shields.io/badge/⬇️%20Kurulum%20Dosyasını%20İndir-SQLVersionChecker_Setup.exe-blue?style=for-the-badge&logo=windows)](https://github.com/AYNIADAM/sqlversionchecker/releases/latest)

SQL Server MDF, BAK ve BCK dosyalarının sürümünü ve bütünlüğünü toplu ve hızlı şekilde tespit eden, modern ve çok dilli (Türkçe/İngilizce) bir masaüstü uygulamasıdır.

Bu uygulama, çok sayıda SQL Server veri ve yedek dosyasının sürümünü ve sağlığını hızlıca tespit etmek isteyen IT uzmanları ve veritabanı yöneticileri için geliştirilmiştir. Sadece klasör ve alt klasörlerdeki ilgili dosyaları bulmakla kalmaz, her bir dosyayı test eder, SQL Server sürümünü belirler ve dosyanın sağlıklı mı yoksa bozuk mu olduğunu ayırt eder. Sonuçlar filtrelenebilir ve toplu işlemlerle dosya yönetimi kolaylaştırılır.

### Özellikler
- Seçilen klasör ve tüm alt klasörlerdeki `.mdf`, `.bak`, `.bck` dosyalarını bulur
- Her dosyayı test ederek SQL Server sürümünü ve dosya bütünlüğünü (sağlam/bozuk) tespit eder
- Sağlam ve bozuk dosyaları sonuçlarda açıkça ayırır ve işaretler
- Toplu sürüm kontrolü ve sonuç filtreleme (duruma, dosya tipine göre vb.)
- Modern dashboard arayüzü, SVG/PNG ikonlar
- Toplu taşıma ve silme işlemleri (orijinal dizin yapısı korunur, dosya üzerine yazma engellenir)
- CPU/RAM dostu, stabil çalışma; ilerleme çubuğu ve duyarlı arayüz
- Çoklu dil desteği (Türkçe/İngilizce, sağ üstte bayrak ile seçim)
- Sonuçları filtreleme, toplu seçim ve büyük veri kümeleri için ilerleme takibi

---

### Dosya Açıklamaları

| Dosya/Klasör                | Açıklama                                                                   |
|-----------------------------|----------------------------------------------------------------------------|
| `main.py`                   | Ana uygulama dosyası. Arayüzü başlatır ve genel iş akışını yönetir.        |
| `mdf_version_checker.py`    | MDF dosyalarının SQL Server sürümünü ve bütünlüğünü tespit eden modül.      |
| `backup_version_checker.py` | BAK/BCK dosyalarının sürümünü ve bütünlüğünü tespit eden modül.             |
| `ui/`                       | Arayüz bileşenleri ve dashboard mantığı.                                   |
| `ui/dashboard.py`           | Ana dashboard ve kullanıcı arayüzü mantığı.                                |
| `icons/`                    | Arayüzde kullanılan SVG/PNG ikonlar ve bayrak görselleri.                  |
| `core/`                     | Çekirdek modüller ve başlangıç dosyaları.                                 |
| `requirements.txt`          | Gerekli Python paketlerinin listesi.                                       |
| `README.md`                 | Proje açıklaması ve kullanım talimatları.                                  |
| `.gitignore`                | Git tarafından yok sayılacak dosya ve klasörler.                           |
| `LICENSE`                   | Proje lisansı (MIT).                                                       |

---

## Author / Yazar
- **Author** AYNIADAM  
- **E-mail:** a.ceyhan@goldverikurtarma.com  
- **Web:** [www.goldverikurtarma.com](https://www.goldverikurtarma.com)

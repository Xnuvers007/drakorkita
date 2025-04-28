from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

import re, os

# Konfigurasi untuk menggunakan mode seluler
mobile_emulation = {
    "deviceName": "Nexus 5"  # Atau ganti dengan perangkat lain sesuai keinginanmu
}

# Mengatur opsi untuk menggunakan Edge
edge_options = Options()
edge_options.add_experimental_option("mobileEmulation", mobile_emulation)
edge_options.add_argument('--disable-logging')

# Menggunakan webdriver-manager untuk otomatis mengunduh EdgeDriver yang sesuai
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

actions = ActionChains(driver)

# Mengunjungi halaman https://drakorkita.in
driver.get("https://drakorkita.in")

# Tunggu beberapa detik agar halaman dimuat
driver.implicitly_wait(10)

try:
    # Menemukan elemen hamburger button untuk membuka menu
    hamburgerButton = driver.find_element(By.XPATH, '/html/body/header/nav/div/button')  # Ganti dengan XPath sesuai elemen yang kamu cari
    hamburgerButton.click()
    sleep(1)  # Tunggu beberapa detik setelah klik
    
    # Menemukan elemen input pencarian menggunakan XPath
    search_input = driver.find_element(By.XPATH, '/html/body/header/nav/div/div/form/input')  # Ganti dengan XPath sesuai elemen yang kamu cari
    search_input.click()  # Klik pada input pencarian
    inputan = input("Masukan Nama Film: ")  # Meminta input dari pengguna
    search_input.send_keys(inputan)  # Mengisi input pencarian dengan kata kunci yang diberikan pengguna
    search_input.send_keys(Keys.RETURN)  # Menekan Enter untuk melakukan pencarian
    sleep(6)  # Tunggu beberapa detik agar hasil pencarian muncul
    
    # Menemukan semua elemen dengan class "titit" yang berisi judul
    titles = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'titit'))
    )

    # Menemukan semua elemen dengan class "type" yang berisi informasi seperti 'TV' atau 'Movie'
    types = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'type'))
    )

    # Menemukan semua elemen dengan class "type" yang berisi durasi
    durations = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'type'))
    )

    # Menemukan semua elemen <a> dengan class "poster" untuk mendapatkan link
    links = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'poster'))
    )

    # Menampilkan semua informasi
    print("\nDaftar hasil pencarian:")
    for idx, title in enumerate(titles):
        link = links[idx].get_attribute('href')
        print(f"{idx + 1}. {title.text} - {types[idx].text} - Durasi: {durations[idx].text} - Link: {link}\n")

    # Meminta input dari pengguna untuk memilih salah satu judul
    choice = int(input("\nPilih salah satu judul berdasarkan nomor (misalnya 1 untuk judul pertama): "))

    if choice < 1 or choice > len(titles):
        print("Pilihan tidak valid!")
    else:
        # Mengambil elemen <a> dengan class "poster" yang sesuai dengan pilihan
        selected_link = links[choice - 1]

        # Scroll ke elemen sebelum mengklik
        driver.execute_script("arguments[0].scrollIntoView(true);", selected_link)
        
        # Tunggu hingga elemen bisa diklik menggunakan WebDriverWait
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(selected_link))
        
        # Klik link yang dipilih
        try:
            selected_link.click()
        except:
            actions.move_to_element(selected_link).click().perform()

        # Tunggu beberapa detik setelah klik
        sleep(3)
    
    # Tunggu sampai tombol download bisa diklik
    # download_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div/div[1]/div[7]/div[2]/div[3]/a')))
    
    # # Klik tombol download
    # download_button.click()

    try:
        download_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[1]/div[7]/div[2]/div[3]/a'))
        )
        download_button.click()
    except StaleElementReferenceException as e:
        print("Stale element reference error caught! Trying to find the element again.")
        download_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[1]/div[7]/div[2]/div[3]/a'))
        )
        download_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")

    sleep(3)  # Tunggu beberapa detik setelah klik

    if len(driver.window_handles) > 1:
        # Tutup tab baru
        # driver.switch_to.window(driver.window_handles[1])
        # driver.close()
        i = 1
        for handle in driver.window_handles:
            if i > 1:
                driver.switch_to.window(handle)
                driver.close()
            i += 1
        # Kembali ke tab asli
        driver.switch_to.window(driver.window_handles[0])
        # Tunggu beberapa detik setelah kembali
        sleep(3)
    else:
        print("Tidak ada tab baru yang dibuka.")
    

    episode_cards = driver.find_elements(By.CLASS_NAME, 'card')
    
    # Loop untuk setiap episode dan ambil link download
    # for card in episode_cards:
    #     episode_number = card.find_element(By.CLASS_NAME, 'card-header').text
    #     video_links = card.find_elements(By.TAG_NAME, 'a')

    #     print(f"\n{episode_number} - Links:")
        
    #     # Mengambil semua link download video (baik 360p dan 540p)
    #     for idx, link in enumerate(video_links):
    #         if re.search(r'(web-dl.*\d+p|\d+p.*web-dl)', link.text, re.IGNORECASE):
    #             print(f"  Download {link.text}: {link.get_attribute('href')}")
                
    #             file_name = f"{inputan.replace(' ', '_')}.txt"
    #             f = open(file_name, 'a', encoding='utf-8')
    #             f.write(link.get_attribute('href') + '\n')
    #             f.close()

    # Loop untuk setiap episode dan ambil link download
    for card in episode_cards:
        episode_number = card.find_element(By.CLASS_NAME, 'card-header').text
        video_links = card.find_elements(By.TAG_NAME, 'a')

        print(f"\n{episode_number} - Links:")
        
        # Membuat direktori untuk menyimpan file jika belum ada
        directory_name = "drakorkita_downloads"
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)

        high_quality_file_path = os.path.join(directory_name, f"{inputan.replace(' ', '_')}_480p_up.txt")
        low_quality_file_path = os.path.join(directory_name, f"{inputan.replace(' ', '_')}_below_480p.txt")

        high_quality_file = open(high_quality_file_path, 'a', encoding='utf-8')
        low_quality_file = open(low_quality_file_path, 'a', encoding='utf-8')
        
        # Mengambil semua link download video (baik 360p dan 540p)
        for idx, link in enumerate(video_links):
            link_text = link.text.lower()  # Ubah ke lowercase agar pencarian lebih mudah
            
            if re.search(r'(web-dl.*\d+p|\d+p.*web-dl)', link.text, re.IGNORECASE):
                print(f"  Download {link.text}: {link.get_attribute('href')}")
                
                # Memisahkan berdasarkan resolusi video
                if '360p' in link_text or '480p' in link_text:
                    # Video dengan resolusi di bawah 480p
                    low_quality_file.write(link.get_attribute('href') + '\n')
                else:
                    # Video dengan resolusi 480p ke atas
                    high_quality_file.write(link.get_attribute('href') + '\n')
        
        # Menutup file setelah selesai menulis link
        high_quality_file.close()
        low_quality_file.close()
        # Menunggu beberapa detik sebelum melanjutkan ke episode berikutnya
        sleep(2)

    # videodownload = WebDriverWait(driver, 20).until(
    #     # EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div/div[2]/div[1]'))
    #     EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div/div[2]'))
    # )
    # # for v in videodownload.find_elements(By.TAG_NAME, 'a'):
    # for idx, v in enumerate(videodownload.find_elements(By.TAG_NAME, 'a')):
    #     # Mengambil URL dari elemen <a>
    #     video_url = v.get_attribute('href')
    #     # print(f"Link download: {video_url}")
    #     print(f"Link download {idx + 1}: {video_url}")
    #     # with open('drakorkita.txt', 'a') as f:
    #     #     f.write(video_url + '\n')

except Exception as e:
    print(f"An error occurred: {e}")

# Menutup browser setelah selesai
input("Press Enter to close the browser...")
driver.quit()

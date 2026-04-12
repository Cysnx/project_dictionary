import pandas as pd
from datetime import datetime
def update_source():
    # 1. Read the files.
    items = pd.read_csv("items.txt", sep=";")
    learn_matrix = pd.read_csv("learn_matrix.txt", sep=";")

    # 2. Kümeleme (Set Creation)
    # Arama maliyetini O(N)'den O(1)'e düşüren o kritik adım.
    # Artık içerideki kelimeleri bir "hash table" olarak tutuyoruz.
    existing_words = set(learn_matrix['word'])

    # 3. Bekleme Odası (Buffer)
    # Ana matrisi sürekli rahatsız etmemek için yeni kelimeleri burada biriktireceğiz.
    new_rows = []

    # Sadece eklenecek aday kelimeler üzerinde tek bir döngü kuruyoruz
    for word_b in items['word']:
        # Kelime kümemizde yoksa...
        if word_b not in existing_words:
            # Onu bekleme odasına alıyoruz (Senin verdiğin 7 sütunlu formata sadık kalarak)
            new_rows.append([word_b, 0, 0, 0, datetime.now().isoformat(), None, 0])

            # Kelimenin items.txt içinde kendini tekrar etme ihtimaline karşı,
            # onu hemen mevcut kelimeler kümemize de ekliyoruz ki aynı kelime iki kez girmesin.
            existing_words.add(word_b)

    # 4. Toplu Birleştirme (Batch Concatenation)
    # Eğer bekleme odasında yeni kelimeler birikmişse, bunları tek bir hamlede ana matrise ekliyoruz.
    if new_rows:
        # Bekleme odasındaki veriyi, ana matrisin sütun isimlerini kullanarak bir DataFrame'e çeviriyoruz
        new_df = pd.DataFrame(new_rows, columns=learn_matrix.columns)

        # Pandas'ın en sevdiği yöntem: Blokları uç uca eklemek (append yerine concat kullanıyoruz)
        learn_matrix = pd.concat([learn_matrix, new_df], ignore_index=True)

        print(f"{len(new_rows)} ea new words added successfully.")
    else:
        print("No new items to be added.")

    # Son durumu inceleyelim
    #print(learn_matrix)
    learn_matrix.to_csv("learn_matrix.txt",sep=";",index=False)
def calculate_breed_score(answers):
    scores = {
        "Persia": 0,
        "Ragdoll": 0,
        "Bengal": 0,
        "Maine Coon": 0,
        "Anggora": 0,
        "Domestic Shorthair": 0,
        "Sphynx": 0,
        "British Shorthair": 0,
        "Bombay": 0,
        "Siamese": 0,
        "Devon Rex": 0
    }

    for answer in answers:
        q = answer['question']
        a = answer['answer']

        if q == "Bagaimana lingkungan tempat tinggamu?":
            if a == "Ramai":
                scores["Anggora"] -= 1
                scores["Maine Coon"] += 2
                scores["Domestic Shorthair"] += 1
                scores["Bombay"] += 2
                scores["Sphynx"] += 1
                scores["British Shorthair"] += 1
                scores["Persia"] -= 1
                scores["Ragdoll"] += 1
                scores["Bengal"] += 2
                scores["Devon Rex"] -= 1
                scores["Siamese"] -= 1
            elif a == "Tenang":
                for breed in scores:
                        scores[breed] += 1

        elif q == "Berapa banyak waktu luang yang kamu miliki untuk bermain setiap hari?":
            if a == "Banyak":
                for breed in scores:
                        scores[breed] += 11
            elif a == "Sedikit":
                scores["Anggora"] -= 1
                scores["Maine Coon"] -= 1
                scores["Domestic Shorthair"] += 2
                scores["Bombay"] += 1
                scores["Sphynx"] += 1
                scores["British Shorthair"] += 2
                scores["Persia"] += 2
                scores["Ragdoll"] -= 1
                scores["Bengal"] -= 1
                scores["Devon Rex"] -= 1
                scores["Siamese"] -= 1

        elif q == "Apakah kamu punya pengalaman merawat kucing sebelumnya?":
            if a == "Punya":
                for breed in scores:
                        scores [breed] +=1
            elif a == "Belum":
                scores["Anggora"] -= 1
                scores["Maine Coon"] -= 1
                scores["Domestic Shorthair"] += 3
                scores["Bombay"] += 1
                scores["Sphynx"] += 1
                scores["British Shorthair"] += 2
                scores["Persia"] -= 1
                scores["Ragdoll"] += 1
                scores["Bengal"] -= 1
                scores["Devon Rex"] -= 1
                scores["Siamese"] -= 1

        elif q == "Apakah ada anak kecil atau hewan peliharaan lain di rumah?":
            if a == "Ada":
                scores["Maine Coon"] += 2
                scores["Domestic Shorthair"] += 1
                scores["Bombay"] += 1
                scores["Sphynx"] += 1
                scores["British Shorthair"] += 1
                scores["Persia"] -= 1
                scores["Ragdoll"] += 1
                scores["Bengal"] += 1
                scores["Devon Rex"] -= 1
                scores["Siamese"] -= 1
            elif a == "Tidak Ada":
                for breed in scores:
                        scores [breed] +=1

        elif q == "Apa yang ingin kamu lakukan bersama kucingmu?":
            if a == "Bermain":
                scores["Anggora"] += 1
                scores["Maine Coon"] += 1
                scores["Domestic Shorthair"] += 1
                scores["Sphynx"] += 2
                scores["Bengal"] += 2
                scores["Devon Rex"] += 2
                scores["Siamese"] += 2
            elif a == "Peluk":
                scores["Maine Coon"] += 2
                scores["Bombay"] += 2
                scores["Sphynx"] += 2
                scores["British Shorthair"] += 1
                scores["Persia"] += 2
                scores["Ragdoll"] += 2

        elif q == "Bagaimana sifat kucing yang kamu suka?":
            if a == "Aktif":
                scores["Anggora"] += 2
                scores["Maine Coon"] += 1
                scores["Domestic Shorthair"] += 2
                scores["Sphynx"] += 2
                scores["Bengal"] += 2
                scores["Devon Rex"] += 2
                scores["Siamese"] += 2
            elif a == "Tenang":
                scores["Anggora"] += 1
                scores["Maine Coon"] += 2
                scores["Domestic Shorthair"] += 1
                scores["Bombay"] += 1
                scores["British Shorthair"] += 1
                scores["Persia"] += 2
                scores["Ragdoll"] += 2
                scores["Bengal"] -= 1
                scores["Devon Rex"] -= 1
                scores["Siamese"] -= 1
        
        elif q == "Apakah kamu alergi terhadap bulu?":
            if a == "Iya":
                scores["Anggora"] -= 2
                scores["Maine Coon"] -= 2
                scores["Domestic Shorthair"] += 1
                scores["Bombay"] -= 1
                scores["Sphynx"] += 2
                scores["British Shorthair"] -= 1
                scores["Persia"] -= 3
                scores["Ragdoll"] -= 2
                scores["Devon Rex"] += 1
            elif a == "Tidak":
                for breed in scores:
                        scores [breed] +=1

        elif q == "Apa kamu tinggal di apartemen(ruang terbatas) atau tempat yang luas?":
            if a == "Ruang terbatas":
                scores["Anggora"] -= 1
                scores["Maine Coon"] -= 1
                scores["Domestic Shorthair"] += 2
                scores["Bombay"] += 2
                scores["Sphynx"] += 1
                scores["British Shorthair"] += 2
                scores["Persia"] += 2
                scores["Ragdoll"] += 1
                scores["Bengal"] -= 1
                scores["Devon Rex"] += 1
                scores["Siamese"] -= 1
            elif a == "Tempat yang luas":
                for breed in scores:
                        scores [breed] +=1

        elif q == "Apa kamu lebih suka kalau kucingmu mengikutimu dan bermanja denganmu?":
            if a == "Ya, tentu":
                scores["Maine Coon"] += 1
                scores["Bombay"] += 2
                scores["Sphynx"] += 1
                scores["Persia"] += 1
                scores["Ragdoll"] += 2
                scores["Devon Rex"] += 2
                scores["Siamese"] += 2
            elif a == "Tidak terlalu":
                scores["Anggora"] += 2
                scores["Sphynx"] -= 1
                scores["British Shorthair"] += 2
                scores["Persia"] += 1
                scores["Bengal"] += 2

        elif q == "Apa kamu tertantang untuk melatih kucingmu?":
            if a == "Ya, aku suka tantangan":
                scores["Anggora"] -= 1
                scores["British Shorthair"] -= 1
                scores["Persia"] -= 1
                scores["Bombay"] += 1
                scores["Ragdoll"] += 1
                scores["Bengal"] += 2
                scores["Devon Rex"] += 2
                scores["Siamese"] += 2
            elif a == "Aku tidak pandai melatih":
                scores["Anggora"] += 1
                scores["Maine Coon"] +=1
                scores["Domestic Shorthair"] += 2
                scores["Bombay"] += 1
                scores["British Shorthair"] += 2
                scores["Persia"] += 1
                scores["Ragdoll"] += 1
                scores["Siamese"] += 1

        elif q == "Apa kamu suka curhat atau ajak kucingmu mengobrol?":
            if a == "Iyaaa":
                scores["Bombay"] += 2
                scores["Ragdoll"] += 1
                scores["Bengal"] += 2
                scores["Devon Rex"] += 2
                scores["Siamese"] += 2
            elif a == "Tidak terlalu":
                scores["Domestic Shorthair"] += 1
                scores["British Shorthair"] += 1
                scores["Persia"] += 1
                scores["Ragdoll"] += 1
                scores["Anggora"] += 1

    best_match = max(scores, key=scores.get)
    return best_match, scores

def get_top_breeds(scores, top_n=3):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]
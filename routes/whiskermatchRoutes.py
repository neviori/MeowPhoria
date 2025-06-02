from flask import Blueprint, request, jsonify, url_for, render_template
from models import WhiskerMatch
from app import db
from app.services.matchService import calculate_breed_score, get_top_breeds

whiskermatch_bp = Blueprint('whiskermatch', __name__)

@whiskermatch_bp.route('/whiskermatch', methods=['GET', 'POST'])
def whisker_match():
    if request.method == 'POST':
        answers = request.get_json()
        if not answers:
            return jsonify({"error": "Tidak ada data jawaban"}), 400

        best_match, scores = calculate_breed_score(answers)
        return jsonify({
            "best_match": best_match,
            "scores": scores
    })
    return render_template('whiskermatch.html')
    


@whiskermatch_bp.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.get_json()
    answers = data.get('answers', [])
    best_match, scores = calculate_breed_score(answers)
    top_breeds = get_top_breeds(scores)

    print("Top 3 Ras Kucing yang Cocok:")
    for i, (breed, score) in enumerate(top_breeds, 1):
        print(f"{i}. {breed} - Skor: {score}")

    # Informasi tentang masing-masing kucing
    cat_info = {
        "Persia": {
            "cat_image_url": url_for('static', filename='img/persian.png'),
            "cat_personality": "Lembut, tenang, tidak agresif, cocok untuk lingkungan damai.",
            "message": "Persia cocok buat kamu yang suka ketenangan dan kucing penyayang!"
        },
        "Ragdoll": {
            "cat_image_url": url_for('static', filename='img/ragdoll.png'),
            "cat_personality": "Si kalem yang suka dipangku.",
            "message": "Ragdoll adalah pilihan tepat jika kamu suka pelukan hangat dan kucing yang kalem!"
        },
        "Bengal": {
            "cat_image_url": url_for('static', filename='img/bengal.png'),
            "cat_personality": "Cheetah mini yang suka bermain dan berinteraksi.",
            "message": "Bengal yang ekspresif akan jadi teman bermain aktifmu di rumah yang ramai!"
        },
        "Maine Coon": {
            "cat_image_url": url_for('static', filename='img/mainecoon.png'),
            "cat_personality": "The Gentle giant yang penuh kasih sayang.",
            "message": "Maine Coon cocok untukmu yang punya keluarga besar atau hewan peliharaan lain!"
        },
        "Anggora": {
            "cat_image_url": url_for('static', filename='img/anggora.png'),
            "cat_personality": "Bulu panjang yang anggun dan suka eksplorasi.",
            "message": "Pilihan tepat jika kamu suka kucing yang tenang dan mandiri!"
        },
        "Bombay": {
            "cat_image_url": url_for('static', filename='img/bombay.png'),
            "cat_personality": "Tenang, tidak cerewet, dan suka disayang",
            "message": "Bombay cocok banget buat kamu yang penyayang!"
        },
        "Siamese": {
            "cat_image_url": url_for('static', filename='img/siamese.png'),
            "cat_personality": "Elegan, aktif, suka ngobrol, dan mudah dirawat.",
            "message": "Siamese bisa jadi teman curhat yang baik loh, dan memeriahkan suasana rumah!"
        },
        "Devon Rex": {
            "cat_image_url": url_for('static', filename='img/devonrex.png'),
            "cat_personality": "Si telinga besar yang cerdas, ekstrovert, dan lincah.",
            "message": "Devon Rex cocok untuk kamu yang pecinta kucing dan punya banyak mainan!"
        },
        "Sphynx": {
            "cat_image_url": url_for('static', filename='img/sphynx.png'),
            "cat_personality": "Kucing tanpa bulu yang sangat sosial, suka berinteraksi.",
            "message": "Sphynx yang cerdas dan aktif cocok buat kamu yang suka berinteraksi!"
        },
        "Domestic Shorthair": {
            "cat_image_url": url_for('static', filename='img/domestic.png'),
            "cat_personality": "Kucing campuran yang tidak mudah sakit dan gampang beradaptasi.",
            "message": "Domestic shorthair sangat cocok untuk pemilik pemula karena sangat mudah dirawat!"
        },
        "British Shorthair": {
            "cat_image_url": url_for('static', filename='img/britiSH.png'),
            "cat_personality": "kucing tenang yang mandiri dan tenang.",
            "message": "British Sorthair cocok jika kamu tidak punya banyak waktu untuk bermain!"
        }
    }

    result = cat_info.get(best_match, {})
    return jsonify({
        "cat_name": best_match,
        **result
    })

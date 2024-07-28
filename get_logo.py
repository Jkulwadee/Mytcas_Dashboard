import pandas as pd

# ข้อมูลมหาวิทยาลัยและ URL ของโลโก้
university_logos = {
    "ชื่อมหาลัย": [
        "จุฬาลงกรณ์มหาวิทยาลัย",
        "มหาวิทยาลัยธรรมศาสตร์",
        "มหาวิทยาลัยเกษตรศาสตร์",
        "มหาวิทยาลัยมหิดล",
        "มหาวิทยาลัยเชียงใหม่",
        "มหาวิทยาลัยขอนแก่น",
        "มหาวิทยาลัยสงขลานครินทร์",
        "มหาวิทยาลัยศิลปากร",
        "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี",
        "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ"
    ],
    "Logo_URL": [
        "https://upload.wikimedia.org/wikipedia/en/5/5e/Chulalongkorn_University_seal.svg",
        "https://upload.wikimedia.org/wikipedia/en/8/84/Thammasat_University_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/9/9d/Kasetsart_University_seal.svg",
        "https://upload.wikimedia.org/wikipedia/en/5/5e/Mahidol_University_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/5/54/Chiang_Mai_University_seal.svg",
        "https://upload.wikimedia.org/wikipedia/en/1/1f/Khon_Kaen_University_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/a/ab/Prince_of_Songkla_University_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/2/23/Silpakorn_University_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/7/7e/King_Mongkut%27s_University_of_Technology_Thonburi_Logo.svg",
        "https://upload.wikimedia.org/wikipedia/en/d/d1/King_Mongkut%27s_University_of_Technology_North_Bangkok_Logo.svg"
    ]
}

# สร้าง DataFrame
df_logos = pd.DataFrame(university_logos)

# บันทึกเป็นไฟล์ CSV
df_logos.to_csv('university_logos.csv', index=False)

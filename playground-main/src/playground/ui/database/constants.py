import logging

logger = logging.getLogger(__name__)


def generate_course_naming(start: int, end: int) -> list[str]:
    return [
        "course_" + str(i).zfill(3) + ".png"
        for i in range(start, end+1)
    ]


# name = [grandprix_KOR, grandprix_ENG, cup_KOR, cup_ENG, track_KOR, track_ENG]
course001 = ["니트로 그랑프리", "Nitro Grand Prix", "버섯 컵", "Mushroom cup", "마리오 카트 스타디움", "Mario Kart Stadium"]
course002 = ["니트로 그랑프리", "Nitro Grand Prix", "버섯 컵", "Mushroom cup", "워터 파크", "Water Park"]
course003 = ["니트로 그랑프리", "Nitro Grand Prix", "버섯 컵", "Mushroom cup", "스위트 캐니언", "Sweet Sweet Canyon"]
course004 = ["니트로 그랑프리", "Nitro Grand Prix", "버섯 컵", "Mushroom cup", "쿵쿵 유적", "Thwomp Ruins"]
course005 = ["니트로 그랑프리", "Nitro Grand Prix", "플라워 컵", "Flower cup", "마리오 서킷", "Mario Circuit"]
course006 = ["니트로 그랑프리", "Nitro Grand Prix", "플라워 컵", "Flower cup", "키노피오 하버", "Toad Harbor"]
course007 = ["니트로 그랑프리", "Nitro Grand Prix", "플라워 컵", "Flower cup", "비틀어진 맨션", "Twisted Mansion"]
course008 = ["니트로 그랑프리", "Nitro Grand Prix", "플라워 컵", "Flower cup", "헤이호 광산", "Shy Guy Falls"]
course009 = ["니트로 그랑프리", "Nitro Grand Prix", "스타 컵", "Star cup", "선샤인 공항", "Sunshine Airport"]
course010 = ["니트로 그랑프리", "Nitro Grand Prix", "스타 컵", "Star cup", "돌핀 케이프", "Dolphin Shoals"]
course011 = ["니트로 그랑프리", "Nitro Grand Prix", "스타 컵", "Star cup", "일렉트로 드림", "Electrodrome"]
course012 = ["니트로 그랑프리", "Nitro Grand Prix", "스타 컵", "Star cup", "와리오 스노 마운틴", "Mount Wario"]
course013 = ["니트로 그랑프리", "Nitro Grand Prix", "스페셜 컵", "Special cup", "스카이 가든", "Cloudtop Cruise"]
course014 = ["니트로 그랑프리", "Nitro Grand Prix", "스페셜 컵", "Special cup", "뼈다귀 사막", "Bone Dry Dunes"]
course015 = ["니트로 그랑프리", "Nitro Grand Prix", "스페셜 컵", "Special cup", "쿠파 성", "Bowswer's Castle"]
course016 = ["니트로 그랑프리", "Nitro Grand Prix", "스페셜 컵", "Special cup", "무지개 로드", "Rainbow Road"]

course017 = ["레트로 그랑프리", "Retro Grand Prix", "등껍질 컵", "Shell Cup", "Wii 음매음매 컨트리", "Wii Moo Moo Meadows"]
course018 = ["레트로 그랑프리", "Retro Grand Prix", "등껍질 컵", "Shell Cup", "GBA 마리오 서킷", "GBA Mario Circuit"]
course019 = ["레트로 그랑프리", "Retro Grand Prix", "등껍질 컵", "Shell Cup", "DS 뽀꾸뽀꾸 비치", "DS Cheep Cheep Beach"]
course020 = ["레트로 그랑프리", "Retro Grand Prix", "등껍질 컵", "Shell Cup", "N64 키노피오 하이웨이", "N64 Toad's Turnpike"]
course021 = ["레트로 그랑프리", "Retro Grand Prix", "바나나 컵", "Banana Cup", "GC 바싹바싹 사막", "GC Dry Dry Desert"]
course022 = ["레트로 그랑프리", "Retro Grand Prix", "바나나 컵", "Banana Cup", "SFC 도넛 평야 3", "SFC Dount Plains 3"]
course023 = ["레트로 그랑프리", "Retro Grand Prix", "바나나 컵", "Banana Cup", "N64 피치 서킷", "N64 Royal Raceway"]
course024 = ["레트로 그랑프리", "Retro Grand Prix", "바나나 컵", "Banana Cup", "3DS DK 정글", "3DS DK Jungle"]
course025 = ["레트로 그랑프리", "Retro Grand Prix", "리프 컵", "Leaf Cup", "DS 와리오 스타디움", "DS Wario Stardium"]
course026 = ["레트로 그랑프리", "Retro Grand Prix", "리프 컵", "Leaf Cup", "GC 셔벗 랜드", "GC Sherbet Land"]
course027 = ["레트로 그랑프리", "Retro Grand Prix", "리프 컵", "Leaf Cup", "3DS 뮤직 파크", "3DS Music Park"]
course028 = ["레트로 그랑프리", "Retro Grand Prix", "리프 컵", "Leaf Cup", "N64 요시 밸리", "N64 Yoshi Valley"]
course029 = ["레트로 그랑프리", "Retro Grand Prix", "번개 컵", "Lightning Cup", "DS 똑딱시계 코스", "DS Tick Tock Clock"]
course030 = ["레트로 그랑프리", "Retro Grand Prix", "번개 컵", "Lightning Cup", "3DS 뻐끔 슬라이더", "3DS Piranha Plant Slide"]
course031 = ["레트로 그랑프리", "Retro Grand Prix", "번개 컵", "Lightning Cup", "Wii 이글이글 화산", "Wii Grumble Volcano"]
course032 = ["레트로 그랑프리", "Retro Grand Prix", "번개 컵", "Lightning Cup", "N64 무지개 로드", "N64 Rainbow Road"]

course033 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "알 컵", "Egg Cup", "GC 요시 서킷", "GC Yoshi's Circuit"]
course034 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "알 컵", "Egg Cup", "익사이트 바이크", "Excitebike Arena"]
course035 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "알 컵", "Egg Cup", "드래곤 드리프트 로드", "Dragon Driftway"]
course036 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "알 컵", "Egg Cup", "뮤트 시티", "Mute City"]
course037 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "젤다 컵", "Triforce Cup", "Wii 와리오 광산", "Wii Wario's Gold Mine"]
course038 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "젤다 컵", "Triforce Cup", "SFC 무지개 로드", "SFC Rainbow Road"]
course039 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "젤다 컵", "Triforce Cup", "미끌미끌 트위스터", "Ice Ice Outpost"]
course040 = ["Wii U DLC 제 1탄", "Wii U DLC Pack 1", "젤다 컵", "Triforce Cup", "하이랄 서킷", "Hyrule Circuit"]

course041 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "동물 컵", "Crossing Cup", "GC 베이비 파크", "GC Baby Park"]
course042 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "동물 컵", "Crossing Cup", "GBA 치즈 랜드", "GBA Cheese Land"]
course043 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "동물 컵", "Crossing Cup", "네이처 로드", "Wild Woods"]
course044 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "동물 컵", "Crossing Cup", "동물의 숲", "Animal Crossing"]
course045 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "벨 컵", "Bell Cup", "3DS 네오 쿠파 시티", "3DS Neo Bowswer City"]
course046 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "벨 컵", "Bell Cup", "GBA 리본 로드", "GBA Ribbon Road"]
course047 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "벨 컵", "Bell Cup", "슈퍼 벨 메트로", "Super Bell Subway"]
course048 = ["Wii U DLC 제 2탄", "Wii U DLC Pack 2", "벨 컵", "Bell Cup", "빅 블루", "Big Blue"]

course049 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "황금대시 컵", "Golden Dash Cup", "Tour 파리 산책로", "Tour Paris Promenade"]
course050 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "황금대시 컵", "Golden Dash Cup", "3DS 키노피오 서킷", "3DS Toad Circuit"]
course051 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "황금대시 컵", "Golden Dash Cup", "N64 초코 마운틴", "N64 Choco Mountain"]
course052 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "황금대시 컵", "Golden Dash Cup", "Wii 코코넛 몰", "Wii Coconut Mall"]
course053 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "복고양이 컵", "Lucky Cat Cup", "Tour 도쿄 블러", "Tour Tokyo Blur"]
course054 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "복고양이 컵", "Lucky Cat Cup", "DS 버섯 고개", "DS Shroom Ridge"]
course055 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "복고양이 컵", "Lucky Cat Cup", "GBA 스카이 가든", "GBA Sky Garden"]
course056 = ["부스터 코스 패스 제 1탄", "Booster Course Pass Wave 1", "복고양이 컵", "Lucky Cat Cup", "Tour 닌자 도장", "Tour Ninja Hideway"]

course057 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "순무 컵", "Turnip Cup", "Tour 뉴욕 미닛", "Tour New York Minute"]
course058 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "순무 컵", "Turnip Cup", "SFC 마리오 서킷 3", "SFC Mario Circuit 3"]
course059 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "순무 컵", "Turnip Cup", "N64 바싹바싹 사막", "N64 Kalimari Desert"]
course060 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "순무 컵", "Turnip Cup", "DS 와루이지 핀볼", "DS Wallugi Pinball"]
course061 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "프로펠러 컵", "Propeller Cup", "Tour 시드니 스프린트", "Tour Sydney Sprint"]
course062 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "프로펠러 컵", "Propeller Cup", "GBA 스노우 랜드", "GBA Snow Land"]
course063 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "프로펠러 컵", "Propeller Cup", "Wii 버섯 캐니언", "Wii Mushroom Gorge"]
course064 = ["부스터 코스 패스 제 2탄", "Booster Course Pass Wave 2", "프로펠러 컵", "Propeller Cup", "아이스크림 빌딩", "Sky-High Sundae"]

course065 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "바위 컵", "Rock Cup", "Tour 런던 루프", "Tour London Loop"]
course066 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "바위 컵", "Rock Cup", "GBA 부끄부끄 호수", "GBA Boo Lake"]
course067 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "바위 컵", "Rock Cup", "3DS 록 록 마운틴", "3DS Rock Rock Mountain"]
course068 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "바위 컵", "Rock Cup", "Wii 단풍나무 로드", "Wii Maple Treeway"]
course069 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "문 컵", "Moon Cup", "Tour 베를린 샛길", "Tour Berlin Byways"]
course070 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "문 컵", "Moon Cup", "DS 피치 가든", "DS Peach Gardens"]
course071 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "문 컵", "Moon Cup", "Tour 메리 마운틴", "Tour Merry Mountain"]
course072 = ["부스터 코스 패스 제 3탄", "Booster Course Pass Wave 3", "문 컵", "Moon Cup", "3DS 무지개 로드", "3DS Rainbow Road"]

course073 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "과일 컵", "Fruit Cup", "Tour 암스테르담 해류", "Tour Amsterdam Drift"]
course074 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "과일 컵", "Fruit Cup", "GBA 리버사이드 파크", "GBA Riverside Park"]
course075 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "과일 컵", "Fruit Cup", "Wii DK 스노보드 경기장", "Wii DK Summit"]
course076 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "과일 컵", "Fruit Cup", "요시 아일랜드", "Yoshi's Island"]
course077 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "부메랑 컵", "Boomerang Cup", "Tour 방콕 러시", "Tour Bangkok Rush"]
course078 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "부메랑 컵", "Boomerang Cup", "DS 마리오 서킷", "DS Mario Circuit"]
course079 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "부메랑 컵", "Boomerang Cup", "GC 와루이지 스타디움", "GC Waluigi Stadium"]
course080 = ["부스터 코스 패스 제 4탄", "Booster Course Pass Wave 4", "부메랑 컵", "Boomerang Cup", "Tour 싱가포르 스피드웨이", "Tour Singapore Speedway"]

course081 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "깃털 컵", "Feather Cup", "Tour 아테네 폴리스", "Tour Athens Dash"]
course082 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "깃털 컵", "Feather Cup", "GC 데이지 크루저", "GC Daisy Cruiser"]
course083 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "깃털 컵", "Feather Cup", "Wii 달맞이 하이웨이", "Wii Moonview Highway"]
course084 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "깃털 컵", "Feather Cup", "비눗방울 로드", "Squeaky Clean Sprint"]
course085 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "체리 컵", "Cherry Cup", "Tour 로스앤젤레스 랩", "Tour Los Angeles Laps"]
course086 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "체리 컵", "Cherry Cup", "GBA 선셋 황야", "GBA Sunset Wilds"]
course087 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "체리 컵", "Cherry Cup", "Wii 엉금엉금 케이프", "Wii Koopa Cape"]
course088 = ["부스터 코스 패스 제 5탄", "Booster Course Pass Wave 5", "체리 컵", "Cherry Cup", "Tour 밴쿠버 벨로시티", "Tour Vancouver Velocity"]

course089 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "도토리 컵", "Acorn Cup", "Tour 로마 아반티", "Tour Rome Avanti"]
course090 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "도토리 컵", "Acorn Cup", "GC DK 마운틴", "GC DK Mountain"]
course091 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "도토리 컵", "Acorn Cup", "Wii 데이지 서킷", "Wii Daisy Circuit"]
course092 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "도토리 컵", "Acorn Cup", "Tour 뻐끔 신전", "Tour Piranha Plant Cove"]
course093 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "가시돌이 컵", "Spiny Cup", "Tour 마드리드 그란데", "Tour Madrid Drive"]
course094 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "가시돌이 컵", "Spiny Cup", "3DS 로젤리나 플래닛", "3DS Rosalina's Ice World"]
course095 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "가시돌이 컵", "Spiny Cup", "SFC 쿠파 성 3", "SFC Bowswer Castle 3"]
course096 = ["부스터 코스 패스 제 6탄", "Booster Course Pass Wave 6", "가시돌이 컵", "Spiny Cup", "Wii 무지개 로드", "Wii Rainbow Road"]


COURSE_NAMING = {
    # Nitro Grand Prix
    "course001.png": course001,   "course002.png": course002,   
    "course003.png": course003,   "course004.png": course004,
    "course005.png": course005,   "course006.png": course006,   
    "course007.png": course007,   "course008.png": course008,
    "course009.png": course009,   "course010.png": course010,   
    "course011.png": course011,   "course012.png": course012,
    "course013.png": course013,   "course014.png": course014,   
    "course015.png": course015,   "course016.png": course016,
    
    # Retro Grand Prix
    "course017.png": course017,   "course018.png": course018,
    "course019.png": course019,   "course020.png": course020,
    "course021.png": course021,   "course022.png": course022,
    "course023.png": course023,   "course024.png": course024,
    "course025.png": course025,   "course026.png": course026,
    "course027.png": course027,   "course028.png": course028,
    "course029.png": course029,   "course030.png": course030,
    "course031.png": course031,   "course032.png": course032,
    
    # DLC Pack 1
    "course033.png": course033,   "course034.png": course034,
    "course035.png": course035,   "course036.png": course036,
    "course037.png": course037,   "course038.png": course038,
    "course039.png": course039,   "course040.png": course040,
    
    # DLC Pack 2
    "course041.png": course041,   "course042.png": course042,
    "course043.png": course043,   "course044.png": course044,
    "course045.png": course045,   "course046.png": course046,
    "course047.png": course047,   "course048.png": course048,
    
    # BCP Wave 1
    "course049.png": course049,   "course050.png": course050,
    "course051.png": course051,   "course052.png": course052,
    "course053.png": course053,   "course054.png": course054,
    "course055.png": course055,   "course056.png": course056,
    
    # BCP Wave 2
    "course057.png": course057,   "course058.png": course058,
    "course059.png": course059,   "course060.png": course060,
    "course061.png": course061,   "course062.png": course062,
    "course063.png": course063,   "course064.png": course064,
    
    # BCP Wave 3
    "course065.png": course065,   "course066.png": course066,
    "course067.png": course067,   "course068.png": course068,
    "course069.png": course069,   "course070.png": course070,
    "course071.png": course071,   "course072.png": course072,
    
    # BCP Wave 4
    "course073.png": course073,   "course074.png": course074,
    "course075.png": course075,   "course076.png": course076,
    "course077.png": course077,   "course078.png": course078,
    "course079.png": course079,   "course080.png": course080,
    
    # BCP Wave 5
    "course081.png": course081,   "course082.png": course082,
    "course083.png": course083,   "course084.png": course084,
    "course085.png": course085,   "course086.png": course086,
    "course087.png": course087,   "course088.png": course088,
    
    # BCP Wave 6
    "course089.png": course089,   "course090.png": course090,
    "course091.png": course091,   "course092.png": course092,
    "course093.png": course093,   "course094.png": course094,
    "course095.png": course095,   "course096.png": course096,
}
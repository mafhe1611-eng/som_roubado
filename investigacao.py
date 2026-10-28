import pandas as pd

crimes = pd.read_csv("crime_scene.csv")
pistas = pd.read_csv("witnesses.csv")
suspeitos = pd.read_csv("suspects.csv")
interrogatorios = pd.read_csv("interviews.csv")

cena = crimes[
    (crimes["date"].astype(str) == "19830715") &
    (crimes["location"] == "West Hollywood Records")
]
print("\n=== 1. CENA DO CRIME ===")
print(cena.to_string(index=False))

if cena.empty:
    print("Cena do crime não encontrada.")
else:
    cena_id = cena.iloc[0]["id"]

pistas_cena = pistas[pistas["crime_scene_id"] == cena_id]
print("\n=== 2. PISTAS DAS TESTEMUNHAS ===")
print(pistas_cena.to_string(index=False))

print("\n=== 3. SUSPEITOS COMPATÍVEIS ===")

compativeis = suspeitos[
        (suspeitos["bandana_color"] == "vermelha") &
        (suspeitos["accessory"] == "relógio de ouro")
    ]
print(compativeis.to_string(index=False))

resultado = compativeis.merge(
        interrogatorios,
        left_on="id",
        right_on="suspect_id",
        how="left"
    )

confissoes = resultado[
        resultado["transcript"].fillna("").str.contains(
            "peguei o disco",
            case=False,
            regex=False
        )
    ]

print("\n=== 4. CONFISSÃO ENCONTRADA ===")

if confissoes.empty:
        print("Nenhuma confissão correspondente encontrada.")
else:
    print(
            confissoes[
                ["id", "name", "bandana_color", "accessory", "transcript"]
            ].to_string(index=False)
        )

    print("\n=== RESULTADO FINAL ===")
    for _, suspeito in confissoes.iterrows():
            print(f"Suspeito: {suspeito['name']}")
            print(f"ID: {suspeito['id']}")
            print(f"Confissão: {suspeito['transcript']}")
import os
import json

DIRETORIO = "./guitar-chords-db-json"
SAIDA = "acordes_com_variacoes.json"

acordes = []

def json_para_lista(nome_acorde, positions):
    resultado = []
    for i, pos in enumerate(positions):
        if isinstance(pos, dict) and "frets" in pos:
            resultado.append({
                "name": nome_acorde,
                "variation": i + 1,
                "frets": pos.get("frets", ""),
                "fingers": pos.get("fingers", ""),
                "barres": pos.get("barres", ""),
                "capo": pos.get("capo", "")
            })
    return resultado

for root, _, files in os.walk(DIRETORIO):
    for nome_arquivo in files:
        if nome_arquivo.endswith(".json"):
            caminho = os.path.join(root, nome_arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if isinstance(data, dict) and "key" in data and "suffix" in data and "positions" in data:
                        nome_completo = f"{data['key']}{data['suffix']}".replace("♯", "#").replace("♭", "b")
                        acordes.extend(json_para_lista(nome_completo.strip(), data["positions"]))
                    else:
                        print(f"⚠️  Ignorado (estrutura incompleta): {caminho}")
            except Exception as e:
                print(f"❌ Erro ao processar {caminho}: {e}")

# Salva a saída final
with open(SAIDA, "w", encoding="utf-8") as f_out:
    json.dump(acordes, f_out, indent=2, ensure_ascii=False)

print(f"✅ Exportado {len(acordes)} variações para: {SAIDA}")

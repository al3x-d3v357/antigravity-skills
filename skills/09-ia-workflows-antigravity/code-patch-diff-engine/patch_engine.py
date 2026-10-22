#!/usr/bin/env python3
import sys
import re
import argparse
from pathlib import Path

DIFF_BLOCK_REGEX = re.compile(
    r"<<<<<<< SEARCH\r?\n(.*?)\r?\n=======\r?\n(.*?)\r?\n>>>>>>> REPLACE",
    re.DOTALL
)

def apply_patches(file_path: Path, patch_content: str) -> tuple[bool, str]:
    if not file_path.exists():
        return False, f"ERRO: Arquivo '{file_path}' não encontrado."
    with open(file_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    # Normaliza quebras de linha para busca consistente
    crlf_mode = "\r\n" in original_text
    working_text = original_text.replace("\r\n", "\n")
    normalized_patch = patch_content.replace("\r\n", "\n")

    matches = list(DIFF_BLOCK_REGEX.finditer(normalized_patch))
    if not matches:
        return False, "ERRO: Nenhum bloco SEARCH/REPLACE válido encontrado no patch."

    current_text = working_text
    applied_count = 0

    for idx, match in enumerate(matches, 1):
        search_block = match.group(1)
        replace_block = match.group(2)

        # 1. Busca exata
        occurrences = current_text.count(search_block)
        if occurrences == 0:
            # Fallback: remove espaços no final das linhas para tolerar pequenas variações
            cleaned_search = "\n".join(line.rstrip() for line in search_block.split("\n"))
            lines = [line.rstrip() for line in current_text.split("\n")]
            reconstructed_text = "\n".join(lines)

            if cleaned_search not in reconstructed_text:
                return False, (
                    f"FALHA Bloco {idx}: Bloco SEARCH não corresponde ao conteúdo atual.\n"
                    f"Certifique-se de fornecer 2 ou 3 linhas de contexto idênticas."
                )

            # Se encontrou na versão limpa, substitui mapeando o padrão
            current_text = current_text.replace(search_block, replace_block, 1)
        elif occurrences > 1:
            return False, (
                f"FALHA Bloco {idx}: Bloco SEARCH é ambíguo ({occurrences} ocorrências encontradas).\n"
                f"Adicione mais linhas de contexto acima ou abaixo para torná-lo único."
            )
        else:
            current_text = current_text.replace(search_block, replace_block, 1)

        applied_count += 1

    final_content = current_text.replace("\n", "\r\n") if crlf_mode else current_text
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    return True, f"SUCESSO: {applied_count} bloco(s) aplicado(s) com sucesso em '{file_path}'."

def main():
    parser = argparse.ArgumentParser(description="Aplica patches SEARCH/REPLACE em arquivos de código.")
    parser.add_argument("file", help="Caminho relativo ou absoluto do arquivo alvo.")
    parser.add_argument("--patch-file", help="Arquivo contendo o patch (opcional). Se omitido, lê do stdin.")
    args = parser.parse_args()

    target_path = Path(args.file)
    if args.patch_file:
        patch_text = Path(args.patch_file).read_text(encoding="utf-8")
    else:
        patch_text = sys.stdin.read()

    success, message = apply_patches(target_path, patch_text)
    print(message)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

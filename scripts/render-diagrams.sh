#!/bin/bash
set -e

DOCS_DIR="docs"
DIAGRAMS_DIR="$DOCS_DIR/diagrams"
IMAGES_DIR="$DOCS_DIR/images"

mkdir -p "$DIAGRAMS_DIR" "$IMAGES_DIR"

echo "Processando arquivos .md com Mermaid..."

find "$DOCS_DIR" -name "*.md" | while read -r md; do

  # Caminho relativo a docs/
  rel=${md#$DOCS_DIR/}

  # Remove .md
  base=${rel%.md}

  # Remove prefixo diagrams/ se existir
  clean=${base#diagrams/}

  mmd="$DIAGRAMS_DIR/$clean.mmd"
  svg="$IMAGES_DIR/$clean.svg"

  mermaid=$(awk '
    BEGIN {in_block=0}
    /^```mermaid/ {in_block=1; next}
    /^```/ {if (in_block) exit}
    in_block {print}
  ' "$md")

  [ -z "$mermaid" ] && continue

  echo "Gerando $mmd"
  mkdir -p "$(dirname "$mmd")"
  echo "$mermaid" > "$mmd"

  echo "🎨 Renderizando $svg"
  mkdir -p "$(dirname "$svg")"
  mmdc -i "$mmd" -o "$svg"

done

echo "✅ Diagramas gerados corretamente"

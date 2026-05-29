# PDF_SPLIT

## 概要

このツールは、**`pdf_divide.py` と同じフォルダ内にある PDF を自動検出**し、**約 25MB 目安**で複数の PDF に分割する CLI ツールです。

- Mac / Windows の両方で使えます
- **標準の実行方法は IDE ではなく、ターミナル（Mac）または PowerShell（Windows）** です
- 分割後の PDF は `output` フォルダに保存されます
- **元の PDF は削除されません**
- 実行ファイル名は **`pdf_divide.py`** です

## 特徴

- PDF ファイル名をコードに書く必要がありません
- 同じフォルダ内の PDF を自動検出します（`output` 内の PDF は対象外）
- 分割結果を `output` フォルダにまとめます
- Mac / Windows 両対応
- 初心者でもコマンドをコピーして実行できます
- GitHub 公開時に PDF 本体を誤って公開しないよう `.gitignore` を設定しています

## 対象ユーザー

- PDF を小さく分割したい人
- ChatGPT 等に投入するために PDF を分割したい人
- Python 学習中の人
- Mac / Windows のどちらでも簡単に使いたい人

## 対応環境

| 項目 | 内容 |
|------|------|
| Python | 3.x |
| OS | Mac、Windows |

**標準実行方法**

| OS | 実行環境 |
|----|----------|
| Mac | ターミナル + `python3` |
| Windows | PowerShell + `py` または `python` |

VSCode / PyCharm は補足扱いです（後述）。

## 公開リポジトリ利用時の注意

- **このリポジトリには PDF ファイル本体を含めません**
- 利用者は自分の PC 上で `PDF_SPLIT` 用フォルダを用意し、分割したい PDF を **1 つだけ** 置いて実行してください
- **著作権のある PDF、教材 PDF、個人情報を含む PDFを GitHub にアップロードしないでください**
- `*.pdf` と `output/` は `.gitignore` で除外しています

### なぜ PDF を GitHub に上げないのか

PDF には著作権のある教材や個人情報が含まれる可能性があります。そのため、GitHub には **ツール本体だけ** を公開し、PDF 本体は利用者のローカル PC で扱います。

## フォルダ構成

### 利用時（自分の PC）

```
Desktop
└── PDF_SPLIT
    ├── pdf_divide.py
    ├── requirements.txt
    └── 分割したいPDF.pdf
```

### 実行後

```
Desktop
└── PDF_SPLIT
    ├── pdf_divide.py
    ├── requirements.txt
    ├── 分割したいPDF.pdf
    └── output
        ├── 分割したいPDF-(01／04).pdf
        ├── 分割したいPDF-(02／04).pdf
        ├── 分割したいPDF-(03／04).pdf
        └── 分割したいPDF-(04／04).pdf
```

### GitHub リポジトリ上

```
tools
├── pdf_divide.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── samples
    └── .gitkeep
```

### なぜ `pdf_devide.py` ではなく `pdf_divide.py` なのか

`divide` は「分割する」という意味の正しい英語スペルです。GitHub で公開する正式ファイル名として **`pdf_divide.py`** に統一しています。

## 事前準備

依存パッケージ `pypdf` をインストールします。

**Mac:**

```bash
python3 -m pip install -r requirements.txt
```

**Windows:**

```powershell
py -m pip install -r requirements.txt
```

`py` が使えない場合:

```powershell
python -m pip install -r requirements.txt
```

## Macでの使い方

```bash
cd ~/Desktop/PDF_SPLIT
python3 -m pip install -r requirements.txt
python3 pdf_divide.py
```

## Windowsでの使い方

PowerShell で以下を実行します。

```powershell
cd $env:USERPROFILE\Desktop\PDF_SPLIT
py -m pip install -r requirements.txt
py pdf_divide.py
```

`py` が使えない場合:

```powershell
cd $env:USERPROFILE\Desktop\PDF_SPLIT
python -m pip install -r requirements.txt
python pdf_divide.py
```

## VSCode / PyCharm を使う場合の注意

- VSCode / PyCharm から実行しても構いません
- ただし **標準手順はターミナル / PowerShell での実行** です
- IDE で実行する場合、その IDE が使っている Python 環境に `pypdf` が入っている必要があります
- `ModuleNotFoundError: No module named 'pypdf'` が出た場合、IDE が使っている Python 環境に `pypdf` が入っていません
- PyCharm の Python Interpreter と、ターミナルの `python3` は **別環境** のことがあります
- VSCode の Python Interpreter と、PowerShell の `py` も **別環境** のことがあります
- **初心者はまずターミナル / PowerShell での実行を推奨** します

### なぜ IDE 実行を標準にしないのか

PyCharm / VSCode は、それぞれ独自に Python Interpreter を選択します。そのため、ターミナルでは動くのに IDE では `pypdf` が見つからない、ということが起きます。初心者向けには、まずターミナル / PowerShell に実行方法を統一した方が、トラブルの切り分けがしやすくなります。

## 実行結果

- 実行すると `output` フォルダが作成されます（存在しない場合）
- 分割された PDF が `output` フォルダに保存されます
- 元の PDF はそのまま残ります
- 実行ログには、元サイズ、ページ数、分割数、保存ファイル名、保存後サイズが表示されます

## よくあるエラーと対処

### 1. ModuleNotFoundError: No module named 'pypdf'

**原因:** 現在使用している Python 環境に `pypdf` が入っていない。

**Mac:**

```bash
python3 -m pip install -r requirements.txt
```

**Windows:**

```powershell
py -m pip install -r requirements.txt
```

または:

```powershell
python -m pip install -r requirements.txt
```

### 2. PDFが見つかりません

**原因:** `pdf_divide.py` と同じフォルダに PDF がない。

**対処:** `PDF_SPLIT` フォルダ直下に、分割したい PDF を 1 つ置く。

### 3. PDFが複数あります

**原因:** `PDF_SPLIT` フォルダ直下に PDF が 2 個以上ある。

**対処:** 分割対象の PDF を 1 個だけ残す。

### 4. python3 が認識されない

**Mac の場合:** Python 3 がインストールされているか確認する。

### 5. py または python が認識されない

**Windows の場合:** Python がインストールされているか、PATH が通っているか確認する。

### 6. OneDrive / iCloud 同期中に失敗する

**原因:** 同期中の PDF にアクセスできない場合がある。

**対処:** PDF を一度 `Desktop/PDF_SPLIT` のようなローカル作業フォルダにコピーしてから実行する。

## 注意点

- `PDF_SPLIT` フォルダ直下には分割対象 PDF を **1 個だけ** 置く
- 複数 PDF の一括処理には対応しない
- 分割後 PDF は `output` フォルダに保存される
- 元 PDF は削除されない
- OneDrive や iCloud 同期中の PDF ではなく、**ローカルにコピーしてから実行** することを推奨する
- **PDF ファイル本体は GitHub にコミットしない**

## このツールの制約

- このツールは **ページ数で均等分割する簡易方式** です
- PDF はページごとに容量が異なります
- 画像が多いページが偏っている場合、分割後 PDF が 25MB を超える可能性があります
- つまり、**厳密に 25MB 以下を保証するツールではありません**
- 厳密に 25MB 以下へ分割したい場合は、ページ追加ごとに一時 PDF を書き出してサイズ確認する方式への改修が必要です

## GitHub公開時に含めないもの

| 対象 | 理由 |
|------|------|
| `*.pdf` | 著作権・個人情報漏洩防止 |
| `output/` | 実行結果であり再生成可能 |
| `.venv/` | 環境依存で容量が大きい |
| `.env` | 秘密情報混入防止 |
| `.idea/` `.vscode/` | 個人の IDE 設定 |
| `__pycache__/` | Python 実行時の生成物 |
| `.DS_Store` | OS が自動生成するファイル |

## ライセンス

MIT License（詳細は [LICENSE](LICENSE) を参照）

Copyright (c) 2026 Takashi Oikawa

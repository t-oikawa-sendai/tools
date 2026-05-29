# Program Name: pdf_divide.py
# Language:     Python3
# Function:     同フォルダ内のPDFを25MB目安でページ均等分割するCLIツール
# Author:       Takashi Oikawa
# Date:         2026-05-16
# LastUpdate:   2026-05-29
# Memo:         Mac / Windows 対応。output 内のPDFは検出対象外。

"""PDFを25MB目安で分割するCLIツール。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

TARGET_MB = 25
OUTPUT_DIR_NAME = "output"


def get_script_dir() -> Path:
    """このスクリプトが置かれたフォルダのパスを返す。"""
    return Path(__file__).resolve().parent


def find_target_pdf(script_dir: Path) -> Path | None:
    """
    スクリプトと同じフォルダ直下のPDFを1件だけ検出する。
    output フォルダ内のPDFは対象外。
    """
    pdf_files = sorted(
        p
        for p in script_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    )

    if len(pdf_files) == 0:
        print("エラー: PDFが見つかりません。")
        print()
        print("対処:")
        print("  pdf_divide.py と同じフォルダに、分割したいPDFを1つだけ置いてください。")
        print("  output フォルダ内のPDFは検出されません。")
        return None

    if len(pdf_files) >= 2:
        print("エラー: PDFが複数あります。")
        print()
        print("pdf_divide.py と同じフォルダに置けるPDFは、1つだけです。")
        print("検出されたPDF:")
        for pdf in pdf_files:
            print(f"  - {pdf.name}")
        print()
        print("対処:")
        print("  分割したいPDFを1つだけ残し、それ以外は別のフォルダへ移動してください。")
        return None

    return pdf_files[0]


def format_size_mb(size_bytes: int) -> str:
    """バイト数をMB表示用の文字列に変換する。"""
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def split_pdf_by_size(input_path: Path, max_mb: int = TARGET_MB) -> int:
    """
    PDFをページ数で均等分割し、output フォルダへ保存する。
    戻り値: 終了コード（0=成功、1=失敗）
    """
    try:
        file_size_bytes = input_path.stat().st_size
    except OSError as exc:
        print(f"エラー: ファイル情報を取得できませんでした: {input_path.name}")
        print(f"  詳細: {exc}")
        return 1

    max_bytes = max_mb * 1024 * 1024
    num_splits = math.ceil(file_size_bytes / max_bytes)

    if num_splits <= 1:
        print(f"対象PDF: {input_path.name}")
        print(f"元ファイルサイズ: {format_size_mb(file_size_bytes)}")
        print()
        print(
            f"このPDFは既に約 {max_mb} MB 以下のため、分割の必要はありません。"
        )
        return 0

    try:
        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)
    except Exception as exc:
        print("エラー: PDFを読み込めませんでした。")
        print()
        print("考えられる原因:")
        print("  - PDFファイルが破損している")
        print("  - パスワード保護などで開けない")
        print("  - ファイルが他のアプリでロックされている")
        print()
        print(f"  詳細: {exc}")
        return 1

    if total_pages == 0:
        print("エラー: PDFにページがありません。")
        return 1

    pages_per_split = math.ceil(total_pages / num_splits)
    base_name = input_path.stem
    output_dir = input_path.parent / OUTPUT_DIR_NAME

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print("エラー: output フォルダを作成できませんでした。")
        print()
        print("考えられる原因:")
        print("  - 書き込み権限がない")
        print("  - ディスク容量が不足している")
        print()
        print(f"  出力先: {output_dir}")
        print(f"  詳細: {exc}")
        return 1

    print(f"対象PDF名: {input_path.name}")
    print(f"元ファイルサイズ: {format_size_mb(file_size_bytes)}")
    print(f"総ページ数: {total_pages}")
    print(f"分割予定数: {num_splits}")
    print(f"1ファイルあたりのページ数: 約 {pages_per_split} ページ")
    print(f"出力先: {output_dir}")
    print()

    for i in range(num_splits):
        writer = PdfWriter()
        start_page = i * pages_per_split
        end_page = min((i + 1) * pages_per_split, total_pages)

        if start_page >= total_pages:
            break

        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        output_filename = f"{base_name}-({i + 1:02d}／{num_splits:02d}).pdf"
        output_path = output_dir / output_filename

        try:
            with output_path.open("wb") as file_obj:
                writer.write(file_obj)
            saved_size = output_path.stat().st_size
        except OSError as exc:
            print(f"エラー: ファイルを保存できませんでした: {output_filename}")
            print()
            print("考えられる原因:")
            print("  - 書き込み権限がない")
            print("  - ディスク容量が不足している")
            print("  - OneDrive / iCloud 同期中でファイルがロックされている")
            print()
            print(f"  出力先: {output_path}")
            print(f"  詳細: {exc}")
            return 1

        print(
            f"保存完了: {output_filename}  "
            f"サイズ: {format_size_mb(saved_size)}"
        )

    return 0


def main() -> int:
    """エントリポイント。"""
    script_dir = get_script_dir()
    target_pdf = find_target_pdf(script_dir)

    if target_pdf is None:
        return 1

    try:
        return split_pdf_by_size(target_pdf)
    except Exception as exc:
        print("エラー: 予期しない問題が発生しました。")
        print()
        print("対処:")
        print("  - PDFをローカルフォルダにコピーしてから再実行してください")
        print("  - 同じフォルダにPDFが1つだけあるか確認してください")
        print("  - ターミナル / PowerShell に表示されたメッセージを確認してください")
        print()
        print(f"  詳細: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

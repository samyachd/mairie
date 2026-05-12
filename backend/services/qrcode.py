import io
import zipfile
import qrcode
from fastapi.responses import StreamingResponse


def generate_qr_bytes(content: str) -> bytes:
    img = qrcode.make(content)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr(content: str) -> StreamingResponse:
    return StreamingResponse(io.BytesIO(generate_qr_bytes(content)), media_type="image/png")


def generate_qr_zip(items: list[tuple[str, str]], zip_filename: str) -> StreamingResponse:
    """Build a ZIP of QR code PNGs. items = list of (filename_stem, qr_content)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for stem, content in items:
            zf.writestr(f"{stem}.png", generate_qr_bytes(content))
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{zip_filename}"'},
    )

from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_folder="slides"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # Clear existing slides
        for f in os.listdir(output_folder):
            if f.endswith((".jpg", ".jpeg", ".png")):
                os.remove(os.path.join(output_folder, f))

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        slide_path = os.path.join(output_folder, f"slide{i+1}.jpg")
        page.save(slide_path, "JPEG")
    print(f"✅ Converted {len(pages)} slides to {output_folder}")

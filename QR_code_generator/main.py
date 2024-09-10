import qrcode

def qr_code_generator():
    url = input("Enter a web url you would like a QR code for: ")
    file_name = input("Enter the name of the file to generate (don't include file type): ")

    qr = qrcode.QRCode(version =  1,
                        box_size = 20,
                        border = 1
                        )

    qr.add_data(url)
    qr.make(fit = True)

    img = qr.make_image(fill_color = "black", back_color = "white")
    img.save(file_name + ".png")

qr_code_generator()
import streamlit as st
from PIL import Image
from cryptography.fernet import Fernet
import io

st.set_page_config(
    page_title='Image Encryption App',
    page_icon='🔒',
    layout='wide'
)

def generate_key():
    return Fernet.generate_key()

def encrypt_image(key, image_bytes):
    f = Fernet(key=key)
    encrypted_data = f.encrypt(image_bytes)
    return encrypted_data

def decrypt_image(key, encrypt_data):
    f = Fernet(key=key)
    decrypted_data = f.decrypt(encrypt_data)
    return decrypted_data

if 'key' not in st.session_state:
    st.session_state.key = None
if 'image_encrypt' not in st.session_state:
    st.session_state.image_encrypt = None

st.markdown("<h1 style='text-align: center; color: blue;'>Image Encryption for Secure Internet Transfer</h1>", unsafe_allow_html=True)
st.write("This app allows you to upload an Image, encrypt it for secure transfer, and then download the encrypted image.")

image_uploader = st.file_uploader(label='Choose an image...', type=['jpg', 'png'])

if image_uploader:
    col1, col2 = st.columns(2)

    with col1:
        img = Image.open(image_uploader)
        st.image(image=img, caption="Uploaded Image", use_column_width=True)
        image_uploader.seek(0)
        image_bytes = image_uploader.read()
    
    with col2:
        if st.session_state.key is None:
            st.session_state.key = generate_key()
        if st.session_state.image_encrypt is None:
            st.session_state.image_encrypt = encrypt_image(key=st.session_state.key, image_bytes=image_bytes)
        st.write("Image Encrypted Successfully!")
        st.download_button(label='Download Encrypted Image', data=st.session_state.image_encrypt, file_name='encrypted_image.bin', mime='application/octet-stream')
        st.write("Save the key securely to decrypt the image later:")
        st.code(st.session_state.key.decode())

        decrypt = st.checkbox(label="Decrypt image(For demostrate purposes)")

        if decrypt:
            try:
                decrypted_image_bytes = decrypt_image(key=st.session_state.key, encrypt_data=st.session_state.image_encrypt)
                decrypted_image = Image.open(io.BytesIO(decrypted_image_bytes))
                st.image(image=decrypted_image, caption="Decrypted Image", use_column_width=True)
            except Exception as e:
                st.error(f"Erro decrypting an image: {e}")


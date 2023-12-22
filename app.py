import streamlit as st
import pandas as pd
from joblib import load
# import mysql.connector
# from mysql.connector import Error

# Load model
model = load('model_klasifikasi_dctc45.model')

# Streamlit app
def main():
    st.title("Prediksi Calon Kandidat Outsourcing TOG Indonesia")

    # Form inputs
    nama = st.text_input("Masukkan Nama", key="input_Nama")
    posisi_harapan = st.text_input("Masukkan Posisi Harapan", key="input_Posisi_Harapan")
    usia = st.text_input("Masukkan Usia Calon Kandidat", key="range_Usia")

    pendidikan_options = ["Lebih dari atau Sama dengan S1 / D4", "Kurang dari S1 / D4"]
    pendidikan = st.selectbox("Pilih Kategori Pendidikan Calon Kandidat", pendidikan_options, key="range_Pendidikan")

    pengalaman_options = ["Lebih dari Setahun", "Kurang dari Setahun"]
    lama_pengalaman = st.selectbox("Pilih Kategori Lama Pengalaman Calon Kandidat", pengalaman_options, key="range_Lama_Pengalaman")

    skill_options = ["Posisi Harapan dengan Skills yang Dimiliki Calon Kandidat SESUAI",
                     "Posisi Harapan dengan Skills yang Dimiliki Calon Kandidat TIDAK SESUAI"]
    kesesuaian_posisi_skill = st.selectbox("Pilih Kategori Kesesuaian Posisi Harapan dengan Skills", skill_options, key="range_Kesesuaian_Posisi_Skill")

    pengalaman_posisi_options = ["Posisi Harapan dengan Posisi Riwayat Kerja yang Dimiliki Calon Kandidat SESUAI",
                                 "Posisi Harapan dengan Posisi Riwayat Kerja yang Dimiliki Calon Kandidat TIDAK SESUAI"]
    kesesuaian_posisi_pengalaman = st.selectbox("Pilih Kategori Kesesuaian Posisi Harapan dengan Pengalaman", pengalaman_posisi_options, key="range_Kesesuaian_Posisi_Pengalaman")

    # Prediction button
    if st.button("Prediksi"):
        try:
            # Perform prediction
            df_test = pd.DataFrame(data={
    "Usia": [usia],
    "Pendidikan": [1 if pendidikan == "Lebih dari atau Sama dengan S1 / D4" else 0],
    "Lama_Pengalaman": [1 if lama_pengalaman == "Lebih dari Setahun" else 0],
    "Kesesuaian_Posisi_Skill": [1 if kesesuaian_posisi_skill == "Posisi Harapan dengan Skills yang Dimiliki Calon Kandidat SESUAI" else 0],
    "Kesesuaian_Posisi_Pengalaman": [1 if kesesuaian_posisi_pengalaman == "Posisi Harapan dengan Posisi Riwayat Kerja yang Dimiliki Calon Kandidat SESUAI" else 0]
    }, 
    columns=[
        "Usia", "Pendidikan", "Lama_Pengalaman", "Kesesuaian_Posisi_Skill", "Kesesuaian_Posisi_Pengalaman"
    ])

            hasil_prediksi = model.predict(df_test)[0]

            # Map prediction to a string
            if hasil_prediksi == 1:
                hasil_prediksi_str = 'Recommended Candidate'
            elif hasil_prediksi == 0:
                hasil_prediksi_str = 'Not Recommended Candidate'
            else:
                hasil_prediksi_str = 'Data Tidak Sesuai Dengan Format'

#             # Save data to the database
#             try:
#                 connection = mysql.connector.connect(host='localhost',
#                                                     database='hasil_prediksi',
#                                                     user='root',
#                                                     password='')
#                 if connection.is_connected():
#                     cursor = connection.cursor()
#                     cursor.execute(f"INSERT INTO klasifikasi (nama, usia, pendidikan, lama_pengalaman, "
#                                     f"kesesuaian_posisi_dg_skills, kesesuaian_posisi_dg_pengalaman, "
#                                     f"posisi_harapan, hasil_prediksi) "
#                                     f"VALUES ('{nama}', {usia}, {1 if pendidikan == 'Lebih dari atau Sama dengan S1 / D4' else 0}, "
#                                     f"{1 if lama_pengalaman == 'Lebih dari Setahun' else 0}, "
#                                     f"{1 if kesesuaian_posisi_skill == 'Posisi Harapan dengan Skills yang Dimiliki Calon Kandidat SESUAI' else 0}, "
#                                     f"{1 if kesesuaian_posisi_pengalaman == 'Posisi Harapan dengan Posisi Riwayat Kerja yang Dimiliki Calon Kandidat SESUAI' else 0}, "
#                                     f"'{posisi_harapan}', '{hasil_prediksi_str}')")
#                     connection.commit()
#                     st.success("Data berhasil disimpan ke database.")
#             except Error as e:
#                 st.error(f"Error while connecting to MySQL: {e}")
#             finally:
#                 if connection.is_connected():
#                     cursor.close()
#                     connection.close()
#                     st.info("MySQL connection is closed")

            # Display prediction result
            st.success(f"Hasil Prediksi : {hasil_prediksi_str}")

        except Exception as e:
            st.error(f"Error during prediction: {e}")

# # View data table
# @st.cache
# def view_tabel():
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                             database='hasil_prediksi',
#                                             user='root',
#                                             password='')
#         if connection.is_connected():
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM klasifikasi")
#             data_tabel = cursor.fetchall()
#             return data_tabel
#     except Error as e:
#         st.error(f"Error while connecting to MySQL: {e}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             st.info("MySQL connection is closed")

# Main function
if __name__ == "__main__":
    main()
    # Show data table if the user clicks the corresponding button
    # if st.button("View Data Table"):
    #     data_tabel = view_tabel()
    #     st.dataframe(pd.DataFrame(data_tabel))


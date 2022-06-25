import streamlit as st
import os
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "documentation"))

def show_pdf():
    with open(file_path+"/Bn Parameter Calibration using Bayesian Inference Process (1).pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Download PDF ",
                       data=PDFbyte,
                       file_name="Documentation.pdf",
                       mime='application/octet-stream')
# show_pdf()
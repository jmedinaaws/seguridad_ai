"""
A web page with streamlit that upload an excel file, ask the column to read and the column to write in.
then allow the user got row by row reading from the column to read from. call a function that return 3 strings (answer1, answer2, generated)
show the tree string in and allows the user to edit them and select one of then to write in the write column.
Update the excel and continue moving to the next row
please do not include the langchain and chroma functions in this file.
"""
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from dotenv import load_dotenv
import os
load_dotenv()  # Load the .env file
temp_dir = os.environ.get("TEMP_DIR")
def get_row_content_by_number(excel_file, row_number):
    """
    Gets the content of a specific row in an Excel file using openpyxl.

    Args:
        excel_file (str): The path to the Excel file.
        row_number (int): The row number to retrieve.

    Returns:
        list: A list containing the values of each cell in the specified row.
    """

    # Load the Excel workbook
    workbook = load_workbook(excel_file)

    # Get the active worksheet
    worksheet = workbook.active

    # Get the row content
    row_content = [cell.value for cell in worksheet[row_number]]

    # Return the row content
    return row_content

def go_editing():
    st.session_state["stage"] = "EDITING"  
    

import streamlit as st
import os



if "stage" not in st.session_state:
      st.session_state["stage"] = "NO_FILE"


if "stage" not in st.session_state:
      st.session_state["stage"] = "NO_FILE"
      
st.title("Responder encuestas")

if st.session_state["stage"] == "NO_FILE":
    # Upload the Excel file
    st.text("Archivos disponibles")
    temp_dir
    filenames = os.listdir(temp_dir)
    excel_files = [""] + [x for x in filenames if x.endswith(".xlsx")]
    excel_files
    selected_filename = st.selectbox('Seleccione el archivo', excel_files)
         
    
    with st.popover("Subir archivo"):
        uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"],)
        if uploaded_file is not None:
            # Read the Excel file into a Pandas DataFrame
            excel_file = os.path.join(temp_dir,uploaded_file.name)
            
            with open(excel_file,"wb",) as f:
                f.write(uploaded_file.getbuffer())
            st.session_state["uploaded"] = uploaded_file.name

    if selected_filename is not None and len(selected_filename) >0:
        excel_file = os.path.join(temp_dir,uploaded_file.name)
        st.session_state["FILE"] = uploaded_file.name
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_excel(excel_file,)
        st.dataframe(df.head(10))


        # Display the columns in the Excel file
        column_to_read = st.selectbox("Selecciona la columna a leer", df.columns)
        st.session_state["column_to_read"] = column_to_read
        column_to_write = st.selectbox("Selecciona la columna a escribir", df.columns)
        st.session_state["column_to_write"] = column_to_write
        column_to_write = st.number_input("Iniciando en fila", )
        st.session_state["row"] = column_to_write        
        st.button("Continuar", on_click=go_editing)
        

elif st.session_state["stage"] == "EDITING":
        # Iterate over the rows of the DataFrame
        file_name = st.session_state["FILE"]
        excel_file = os.path.join(temp_dir,file_name)
        st.header(f"Editando {file_name}")

        for index, row in df.iterrows():
            # Display the question from the selected column
            st.write(f"Pregunta {index+1}: {row[column_to_read]}")

            # Call the function to get the answers
            answer1, answer2, generated = "old1","2ad dasgsgssdsdds asd","fasdfasg asdgasdg"#get_answers(row[column_to_read])

            # Display the answers
            st.write(f"Respuesta 1: {answer1}")
            st.write(f"Respuesta 2: {answer2}")
            st.write(f"Respuesta Generada: {generated}")

            # Allow the user to edit the answers
            edited_answer1 = st.text_area(
                "Edita la Respuesta 1", value=answer1)
            edited_answer2 = st.text_area(
                "Edita la Respuesta 2", value=answer2)
            edited_generated = st.text_area(
                "Edita la Respuesta Generada", value=generated)

            # Allow the user to select the answer to write
            selected_answer = st.radio("Selecciona la respuesta a escribir", [
                "Respuesta 1", "Respuesta 2", "Respuesta Generada"])

            # Write the selected answer to the selected column
            if selected_answer == "Respuesta 1":
                    df.loc[index, column_to_write] = edited_answer1
            elif selected_answer == "Respuesta 2":
                    df.loc[index, column_to_write] = edited_answer2
            else:
                    df.loc[index, column_to_write] = edited_generated

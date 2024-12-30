###############################################################################
# Web App for Converting your documents/images to Markdown
#
# Author: devlab@qq.com
# History:
# When      | Who           | What
# 30/12/2024|TQ Ye          | Creation
###############################################################################
import sys
import streamlit as st
from markitdown import MarkItDown
from random import randint
import base64

class Local:    
    title: str
    choose_content_type: str
    language: str
    lang_code: str
    file_upload_label: str
    enter_url_label: str
    file_download_label: str
    support_message: str
    
    def __init__(self, 
                title,
                choose_content_type,
                language,
                lang_code,
                file_upload_label,
                enter_url_label,
                file_download_label,
                support_message,
                ):
        self.title= title
        self.choose_content_type = choose_content_type
        self.language= language
        self.lang_code= lang_code
        self.lang_code= lang_code
        self.file_upload_label = file_upload_label
        self.enter_url_label = enter_url_label
        self.file_download_label=file_download_label
        self.support_message = support_message

en = Local(
    title="Markdown, Please!",
    choose_content_type="File or Link",
    language="English",
    lang_code="en",
    file_upload_label="Please uploaded your file (your file will never be saved anywhere)",
    enter_url_label="Please input the URL",
    file_download_label="Markdown File Download Link",
    support_message="""
                Please report any issues or suggestions to tqye@yahoo.com<br>If you like this App please <a href='https://buymeacoffee.com/tqye2006'>buy me a :coffee:🌝 </a>
                <p> To use other AI models：
                <br><a href='https://geminiecho.streamlit.app'>Gemini models</a>
                <br><a href='https://askcrp.streamlit.app'>Command R+</a>
                <br><a href='https://gptecho.streamlit.app'>OpenAI GPT-4o</a>
                <br><a href='https://claudeecho.streamlit.app'>Claude</a>
                <br><a href='https://imagicapp.streamlit.app'>Photo enhancer/background remover</a>
                """,
)

zw = Local(
    title="Markdown, Please!",
    choose_content_type="文件或链接",
    language="Chinese",
    lang_code="ch",
    file_upload_label="请上传你的文件（文件只在内存，不会被保留）",
    enter_url_label="请输入链接",
    file_download_label="Markdown文件下载链接",
    support_message="""
                    如遇什么问题或有什么建议，反馈，请电 tqye@yahoo.com
                    <p>使用其它AI模型:<br><a href='https://geminiecho.streamlit.app'>Gemini models</a>
                    <br><a href='https://askcrp.streamlit.app'>Command R+</a>
                    <br><a href='https://gptecho.streamlit.app'>OpenAI GPT-4o</a>
                    <br><a href='https://claudeecho.streamlit.app'>Claude</a>
                    <br><a href='https://imagicapp.streamlit.app'>照片增强/去背景</a>
                    """,
)
    
def get_binary_file_downloader_html(bin_file : bytes, file_label='File'):
    '''
    Generates a link allowing the data in a given bin_file to be downloaded
    in:  bin_file (bytes)
    out: href string
    '''
    b64 = base64.b64encode(bin_file).decode()
    href = f'{st.session_state.locale.file_download_label} <a href="data:application/octet-stream;base64,{b64}" download="{file_label}">{file_label}</a>'
    
    return href

@st.cache_resource()
def GetModel():

    return MarkItDown()

@st.cache_resource()
def Main_Title(text: str) -> None:

    st.markdown(f'<p style="background-color:#ffffff;color:#049ca4;font-weight:bold;font-size:24px;border-radius:2%;">{text}</p>', unsafe_allow_html=True)

##############################################
################ MAIN ########################
##############################################
def main(argv):
    
    Main_Title(st.session_state.locale.title + " (v0.0.1)")

    st.session_state.choose_type_placeholder = st.empty()
    st.session_state.uploading_file_placeholder = st.empty()
    st.session_state.download_links = st.empty()
    st.session_state.output_placeholder = st.empty()
    filePath = ""
    results = ""
    
    md = GetModel()
    
    file_or_link = st.session_state.choose_type_placeholder.radio(st.session_state.locale.choose_content_type, ("File/文件", "Link/链接(Youtube, Wikipedia)"), index=st.session_state.type_index, horizontal=True)
    with st.session_state.uploading_file_placeholder:
        if "File" in file_or_link:
            st.session_state.type_index = 0

            file_types = ['docx', 'pdf', 'ppt', 'pptx', 'xlsx', 'txt', 'csv', 'json', 'xml', 'yaml', 'yml', 'toml', 'c', 'cpp', 'h', 'hpp', 'cs', 'java', 'js', 'html', 'css', 'py', 'ipynb', 'r', 'rb', 'php', 'pl', 'sh', 'bat', 'ps1', 'cmd',]
            st.session_state.uploaded_file = st.file_uploader(label=st.session_state.locale.file_upload_label, type=file_types, key=st.session_state.fup_key)
            if st.session_state.uploaded_file is not None:
                #get file path
                filePath = st.session_state.uploaded_file.name
                try:
                    md_results = md.convert(filePath)
                    results = md_results.text_content
                except Exception as ex:
                    st.session_state.output_placeholder.warning(f"Error: {str(ex)}")
                    return
        elif "Link" in file_or_link:
            st.session_state.type_index = 1
            with st.form(key='link_form'):
                url = st.text_input(st.session_state.locale.enter_url_label, "")
                bnt_convert = st.form_submit_button("Convert")
                if bnt_convert:
                    try:
                        md_results = md.convert(url)
                        results = md_results.text_content
                        # using the url last part as the file name
                        filePath = url.split("=")[-1]
                        filePath = filePath.split("/")[-1]
                    except Exception as ex:
                        st.session_state.output_placeholder.warning(f"Error: {str(ex)}")
                        return
        else:
            st.warning("No file uploaded")
            return                
        
    if results == "":
        st.session_state.output_placeholder.warning("No result")
        return
        
    # create link to download the result
    out_file_name = f"{filePath}.md"
    with st.session_state.download_links:
        st.markdown(get_binary_file_downloader_html(results.encode(), out_file_name), unsafe_allow_html=True)

    # display the result
    with st.session_state.output_placeholder:
        st.markdown(results, unsafe_allow_html=True)


##############################
# Entry point
##############################
if __name__ == "__main__":

    # Initiaiise session_state elements
    if "locale" not in st.session_state:
        st.session_state.locale = zw

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if "lang_index" not in st.session_state:
        st.session_state.lang_index = 1

    if "type_index" not in st.session_state:
        st.session_state.type_index = 0

    if "disabled" not in st.session_state:
        st.session_state.disabled = True

    if 'fup_key' not in st.session_state:
        st.session_state.fup_key = str(randint(1000, 10000000))    
    
    st.markdown(
            """
                <style>
                    .appview-container .block-container {{
                        padding-top: {padding_top}rem;
                        padding-bottom: {padding_bottom}rem;
                    }}
                    .sidebar .sidebar-content {{
                        width: 200px;
                    }}
                    button {{
                        /*    height: auto; */
                        width: 120px;
                        height: 32px;
                        padding-top: 10px !important;
                        padding-bottom: 10px !important;
                    }}
                </style>""".format(padding_top=5, padding_bottom=10),
            unsafe_allow_html=True,
    )

    language = st.radio("Choose UI language", ("English UI", "中文界面"), index=st.session_state.lang_index, label_visibility="collapsed", horizontal=True)
    if "English" in language:
        st.session_state.locale = en
        st.session_state.lang_index = 0
    else:
        st.session_state.locale = zw
        st.session_state.lang_index = 1

    st.sidebar.markdown(st.session_state.locale.support_message, unsafe_allow_html=True)
        
    main(sys.argv)


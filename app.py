###############################################################################
# Web App for Converting your documents/images to Markdown
#
# Author: devlab@qq.com
# History:
# When      | Who           | What
# 30/12/2024|TQ Ye          | Creation
###############################################################################
import streamlit as st
from markitdown import MarkItDown
import yt_dlp
from urllib.error import HTTPError
import tempfile
import os
import sys
from random import randint
import base64
import time

class Local:    
    title: str
    description: str
    choose_content_type: str
    language: str
    lang_code: str
    file_upload_label: str
    enter_url_label: str
    file_download_label: str
    support_message: str
    
    def __init__(self, 
                title,
                description,
                choose_content_type,
                language,
                lang_code,
                file_upload_label,
                enter_url_label,
                file_download_label,
                btn_convert_label,
                btn_download_label,
                support_message,
                ):
        self.title= title
        self.description= description
        self.choose_content_type = choose_content_type
        self.language= language
        self.lang_code= lang_code
        self.lang_code= lang_code
        self.file_upload_label = file_upload_label
        self.enter_url_label = enter_url_label
        self.file_download_label=file_download_label
        self.btn_convert_label = btn_convert_label
        self.btn_download_label = btn_download_label
        self.support_message = support_message

en = Local(
    title="Markdown, Please!",
    description="<li>Convert File or Website to Markdown Format<li>Download Video from Youtube<p>",
    choose_content_type="File or Link",
    language="English",
    lang_code="en",
    file_upload_label="Please uploaded your file (your file will never be saved anywhere)",
    enter_url_label="Please input the URL",
    file_download_label="Markdown File Download Link",
    btn_convert_label="Markdown",
    btn_download_label="Download",
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
    description="<li>将文件或网页转换为Markdown格式<li>从Youtube下载视频<p>",
    choose_content_type="文件或链接",
    language="Chinese",
    lang_code="ch",
    file_upload_label="请上传你的文件（文件只在内存，不会被保留）",
    enter_url_label="请输入链接",
    file_download_label="Markdown文件下载链接",
    btn_convert_label="获取Markdown",
    btn_download_label="下载视频",
    support_message="""
                    如遇什么问题或有什么建议，反馈，请电 tqye@yahoo.com
                    <p>使用其它AI模型:<br><a href='https://geminiecho.streamlit.app'>Gemini models</a>
                    <br><a href='https://askcrp.streamlit.app'>Command R+</a>
                    <br><a href='https://gptecho.streamlit.app'>OpenAI GPT-4o</a>
                    <br><a href='https://claudeecho.streamlit.app'>Claude</a>
                    <br><a href='https://imagicapp.streamlit.app'>照片增强/去背景</a>
                    """,
)

@st.cache_data()
def download_youtube_video(url, output_dir):
    '''
    Download a YouTube video using the provided URL
    '''
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Ensure the output path includes the file name template
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            #video_title = info_dict.get('title', None)
            video_title = "video_output"
            video_ext = info_dict.get('ext', None)
            file_path = os.path.join(output_dir, f"{video_title}.{video_ext}")
        return file_path
    except yt_dlp.utils.DownloadError as e:
        print(f"Download Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return None

    # # Example usage
    # url = "https://www.youtube.com/watch?v=example"
    # output_path = "path/to/download"
    # download_youtube_video(url, output_path)

@st.cache_data()
def create_download_link(out_file_name, results):
    st.markdown(get_binary_file_downloader_html(results.encode(), out_file_name), unsafe_allow_html=True)

@st.cache_data()
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
def Main_Title(title: str, desc: str) -> None:

    st.markdown(f'<div style="background-color:#ffffff;color:#049ca4;font-weight:bold;font-size:24px;border-radius:2%;">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:16px;">{desc}</div>', unsafe_allow_html=True)

##############################################
################ MAIN ########################
##############################################
def main(argv):
    
    Main_Title(st.session_state.locale.title + " (v0.0.1)", desc=st.session_state.locale.description)

    # Create placeholders
    st.session_state.choose_type_placeholder = st.empty()
    st.session_state.uploading_file_placeholder = st.empty()
    st.session_state.download_links = st.empty()
    st.session_state.output_placeholder = st.empty()
    filePath = ""
    results = ""
    video_path = None

    # Get the model
    md = GetModel()
    
    # Choose file or link
    file_or_link = st.session_state.choose_type_placeholder.radio(st.session_state.locale.choose_content_type, ("File/文件", "URL/链接(Youtube, Wikipedia, etc)"), index=st.session_state.type_index, horizontal=True)
    with st.session_state.uploading_file_placeholder:
        if "File" in file_or_link:
            st.session_state.type_index = 0
            file_types = ['docx', 'pdf', 'ppt', 'pptx', 'xlsx', 'txt', 'csv', 'json', 'xml', 'yaml', 'yml', 'toml', 'c', 'cpp', 'h', 'hpp', 'cs', 'java', 'js', 'html', 'css', 'py', 'ipynb', 'php', 'pl',]
            st.session_state.uploaded_file = st.file_uploader(label=st.session_state.locale.file_upload_label, type=file_types, accept_multiple_files=False, key=st.session_state.fup_key)
            if st.session_state.uploaded_file is not None:
                #get file path
                filePath = st.session_state.uploaded_file.name
                try:
                    with st.spinner('Wait ...'):
                        md_results = md.convert(filePath)
                        results = md_results.text_content
                        with st.session_state.download_links:
                            create_download_link(out_file_name, results)
                        # display the result
                        with st.session_state.output_placeholder:
                            st.markdown(results, unsafe_allow_html=True)
                except Exception as ex:
                    st.session_state.output_placeholder.warning(f"Error: {str(ex)}")
                    return
        elif "URL" in file_or_link:
            st.session_state.type_index = 1
            with st.form(key='link_form'):
                url = st.text_input(st.session_state.locale.enter_url_label, "")
                col1, col2 = st.columns(2)
                bnt_convert = col1.form_submit_button(st.session_state.locale.btn_convert_label)
                bnt_download = col2.form_submit_button(st.session_state.locale.btn_download_label)
                if bnt_convert:
                    try:
                        with st.spinner('Wait ...'):
                            md_results = md.convert(url)
                            results = md_results.text_content
                        # using the url last part as the file name
                        filePath = url.split("=")[-1]
                        filePath = filePath.split("/")[-1]
                        filePath += "_output"
                        # create link to download the result
                        out_file_name = f"{filePath}.md"
                        with st.session_state.download_links:
                            create_download_link(out_file_name, results)
                        # display the result
                        with st.session_state.output_placeholder:
                            st.markdown(results, unsafe_allow_html=True)
                    except Exception as ex:
                        st.session_state.output_placeholder.warning(f"Error: {str(ex)}")
                        return
                
                if bnt_download:
                    try:
                        if "youtube.com" in url or "youtu.be" in url:
                            with st.spinner('Downloading video...'):
                                with tempfile.TemporaryDirectory() as tmpdirname:
                                    #output_path = os.path.join(tmpdirname, "video.mp4")
                                    output_dir = tmpdirname
                                    video_path = download_youtube_video(url, output_dir)
                                    time.sleep(5)  # Sleep for 5 seconds to ensure the file is downloaded
                                    
                        else:
                            st.warning("Download is only supported for YouTube links.")
                    except Exception as ex:
                        st.session_state.output_placeholder.warning(f"Error: {str(ex)}")
                        return
                    
            if video_path is not None:
                with open(video_path, "rb") as file:
                    btn = st.download_button(
                                    label="Download Video",
                                    data=file,
                                    file_name="video.mp4",
                                    mime="video/mp4")
                st.session_state.output_placeholder.success("Video is ready for download.")
        else:
            return                
        
    if results == "":
        st.session_state.output_placeholder.warning("No result")
        return
        



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


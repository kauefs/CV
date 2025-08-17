import  streamlit         as   st
import        cv2         as   cv
import      numpy         as   np
import     pandas         as   pd
import    seaborn         as   sns
import matplotlib.pyplot  as   plt
from          PIL       import Image, ImageEnhance
st.set_page_config(page_title='PhotoMoidal', page_icon='🎑', layout='wide', initial_sidebar_state='expanded')
# Settings:
pd.options.plotting.matplotlib.register_converters = True
pd.options.display.max_columns         =             None
plt.rcParams[  'figure.autolayout']    =             True
plt.rcParams[    'font.family'    ]    =                                          'sans-serif'
sns.set_theme(context='notebook', style='whitegrid', palette='colorblind',  font ='sans-serif', font_scale=1.15, color_codes=True, rc={'grid.color':'1','grid.linestyle':':'})
FontT={'family':'sans-serif'    ,'color':'#000000', 'size': 13,    'fontweight':'semibold'  }
FontY={'family':'sans-serif'    ,'color':'#FF4500', 'size': 10,    'fontweight':'regular'   }
FontX={'family':'sans-serif'    ,'color':'#4CAF50', 'size': 10,    'fontweight':'regular'   }
OutPutWidth=500
def state( ):
    if 'points' not in st.session_state:st.session_state.points=[]
state    ( )
def main ( ):
    st.sidebar.markdown('''[![logo](https://raw.githubusercontent.com/carlosfab/escola-data-science/master/img/novo_logo_bg_escuro.png)](https://sigmoidal.ai/)''')
    st.sidebar.divider (   )
    st.sidebar.header  ('PhotoMoidal')
    st.sidebar.warning ('100% in Python')
    st.sidebar.caption ('Apply filters to images, using OpenCV library.')
    # Page Options
    options    =['Filters','About']
    choice     =st.sidebar.selectbox('Pages', options)
    st.sidebar.divider (   )
    st.sidebar.header  ('File UpLoad Area')
   #image      =Image.open          ('empty.jpg')
    image      =st.sidebar.file_uploader('UpLoad Image File (GIF/JPG/PNG)', type=['gif','png','jpg'])
    # Filters:
    if choice == 'Filters':
        st.title('Computer Vision MasterClass')
        st.markdown(f'''➡️ Project from Introduction to Computer Vision MasterClass by Carlos Melo **@** [Sigmoidal](https://sigmoidal.ai/).''')
        # Load & Display Image:
        # image= cv.imread(image.img)   # -> This won't work!
        st.subheader('Image Filters')
        if not image:
            st.sidebar.warning('No Image Loaded!')
            st        .warning('Use SideBar to UpLoad Image')
            st.stop( )    
        if  image is not None:
            image=Image.open(image)
            st.sidebar.text('Original Image')
            st.sidebar.image(image, width=150)
        col1,col2=st.columns(2)
        filters=st.sidebar.radio('Filters:',['Original',
                                            'GrayScale',
                                            'Sketch',
                                            'Sepia',
                                            'BrightNess',
                                            'Contrast',
                                            'Blur',
                                            'Canny'])
        if   filters   =='GrayScale':
            convertedIMG=np.array(image.convert('RGB'))
            grayIMG     =cv.cvtColor(convertedIMG, cv.COLOR_RGB2GRAY)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('GrayScale')
            col2.image(grayIMG, use_container_width=True)
           #st.image  (grayIMG, width=OutPutWidth, caption='Image with GrayScale Filter')
        elif filters   =='Sketch':
            convertedIMG=np.array(image.convert('RGB'))
            grayIMG     =cv.cvtColor(convertedIMG, cv.COLOR_RGB2GRAY)
            INVgrayIMG  =255-grayIMG
            blurIMG     =cv.GaussianBlur(INVgrayIMG,(25, 25), 0,0)
            sketchIMG   =cv.divide(grayIMG,255-blurIMG, scale=256)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('Sketch')
            col2.image(sketchIMG, use_container_width=True)
           #st.image(sketchIMG, width=OutPutWidth, caption='Image with Sketch Filter')
        elif filters   =='Sepia':
            convertedIMG=np.array(image.convert('RGB'))
            convertedIMG=cv.cvtColor(convertedIMG, cv.COLOR_RGB2BGR)
            kernel      =np.array([[.275,.535,.135],
                                   [.350,.685,.170],
                                   [.390,.770,.190]])
            sepiaIMG    =cv.filter2D(convertedIMG, -1, kernel)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('Sepia')
            col2.image(sepiaIMG, channels='BGR', use_container_width=True)
           #st.image  (sepiaIMG, channels='BGR', width=OutPutWidth, caption='Image with Sepia Filter')
        elif filters   =='BrightNess':
            brightness  =st.sidebar.slider('BrightNess', 0.,2.,1.)
            enhancer    =ImageEnhance.Brightness(image)
            brightIMG   =enhancer.enhance(brightness)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('BrightNess')
            col2.image(brightIMG, use_container_width=True)
        elif filters   =='Contrast':
            contrast    =st.sidebar.slider('Contrast', 0.,2.,1.)
            enhancer    =ImageEnhance.Contrast(image)
            contrastIMG =enhancer.enhance(contrast)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('Contrast')
            col2.image(contrastIMG, use_container_width=True)
           #st.image(contrastIMG, width=OutPutWidth, caption='Image with Contrast at {}'.format(contrast))
        elif filters   =='Blur':
            blur        =st.sidebar.slider('Kernel (n x n)', 3, 27, 9, step=2)
            convertedIMG=np.array(image.convert('RGB'))
            convertedIMG=cv.cvtColor    (convertedIMG, cv.COLOR_RGB2BGR)
            blurIMG     =cv.GaussianBlur(convertedIMG, (blur, blur), 0, 0)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('Blur')
            col2.image(blurIMG, channels='BGR', use_container_width=True)
           #st.image  (blurIMG, channels='BGR', width=OutPutWidth, caption='Image with Blur Filter ({} x {}).'.format(blur, blur))
        elif filters   =='Canny':
            convertedIMG=np.array(image.convert('RGB'))
            convertedIMG=cv.cvtColor    (convertedIMG, cv.COLOR_RGB2BGR)
            blurIMG     =cv.GaussianBlur(convertedIMG, (11, 11), 0)
            canny       =cv.Canny(blurIMG, 100, 150)
            col1.header('Original')
            col1.image(image, use_container_width=True)
            col2.header('Canny Edge Detection')
            col2.image(canny, use_container_width=True)
           #st.image  (canny, width=OutPutWidth, caption='Image with Canny Filter')
        elif filters   =='Original':st.image(image, use_container_width=True)   # width=OutPutWidth
        else                       :st.image(image, use_container_width=True)   # width=OutPutWidth
        st.sidebar.divider (   )
        st.sidebar.markdown('''
        ![2025.08.15   ](https://img.shields.io/badge/2025.08.15-000000)

        [![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

        [![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
        [![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
        [![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
        [![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

        [![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2025&labelColor=0065FF)](https://datavision.one/)
                                ''')
    elif     choice    =='About':
        st.subheader('Project from Introduction to Computer Vision MasterClass.')
        st.markdown ('[Sigmoidal](https://sigmoidal.ai/)')
        st.text     ('Carlos Melo')
        st.success  ('Instagram @carlos_melo.py')
        st.video    ('https://www.youtube.com/watch?v=JhkhbTTxlQg')
if __name__=='__main__':main( )
st.toast('Loaded!', icon='✨')

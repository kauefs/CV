# StreamLit PersPective Correction App:
# https://github.com/carlosfab/vis101-fundamentos-visao/blob/main/vis102/perspective-correction/app.py
import   io,      json
import   cv2       as   cv
import numpy       as   np
import streamlit   as   st
from   streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from   PIL       import Image, ImageDraw, ImageFont
from   typing    import List, Tuple
st.set_page_config(page_title = 'Perspective Correction (4 Points)', layout='wide', initial_sidebar_state='expanded')
st.title          (       'Image Perspective Correction')
st.subheader      (                                  'in 4 clicks')
# Functions:
def state( ):
    if 'points' not in st.session_state:st.session_state.points:List[Tuple[int,int]]=[]
def OverLay(image:Image.Image, points:List[Tuple[int,int]], poly=True)->Image.Image:
    '''Draw Circles & Indices & (Optional) Polygon on the Image.'''
    img =image    .copy(   )
    draw=ImageDraw.Draw(img)
    r   =max(3 ,    min(img.size)//150)
    try   :font=ImageFont.truetype('verdana.ttf'  ,    size=max(12,r*6))
    except:font=ImageFont.load_default( )
    # Points:
    for idx,(x,y)in enumerate(points,start=1):
        draw .ellipse((x - r, y - r, x + r, y + r), outline=(255, 0, 0), width=2)
        label=str(idx)
        tw,th=draw.textlength(label, font  = font), font.size
        draw .rectangle((x + r + 2, y - th // 2 - 2, x + r + 2 + tw + 4, y + th // 2 + 2), fill=(255, 255, 255)           )
        draw .text     ((x + r + 4, y - th // 2), label,                                   fill=(  0,   0,   0), font=font)
    # Polygon (Clicked Order):
    if poly  and       len(points)>=2:
        for i in range(len(points)- 1):draw.line([points[ i], points[i + 1]], fill=(0, 255, 0), width=2)
        if             len(points)==4 :draw.line([points[-1], points  [0]  ], fill=(0, 255, 0), width=2)
    return img
def OrderQuadPoints(pts:np.ndarray)->np.ndarray:
    '''
    Order 4 Points as Top-Left (TL), Top-Right (TR), Bottom-Right (BR), Bottom-Left (BL).
    Classic Strategy: Sum & Difference of Coordinates.
    '''
    rect   =    np.zeros((4, 2), dtype='float32')
    diff   =    np.diff ( pts  ,  axis=       1 )  # y - x
    s      =pts   .sum  (         axis=       1 )  # x + y
    rect[0]=pts[np.argmin(  s )]        # TL
    rect[2]=pts[np.argmax(  s )]        # BR
    rect[1]=pts[np.argmin(diff)]        # TR
    rect[3]=pts[np.argmax(diff)]        # BL
    return  rect
def WarpDocument(imageNP: np.ndarray,     pts:List[Tuple[int,int]],
                 targetW:int=   1100, targetH: int=1600)->np.ndarray:
    '''
    Apply Warp Perspective Based on 4 Points of the Original Image Space.
    Fixed OutPut (targetW x targetH).
    '''
    ptsNP  =np.array(pts, dtype='float32')
    rect   =OrderQuadPoints(ptsNP)
    targetW=max(int(targetW) , 50)
    targetH=max(int(targetH) , 50)
    dst    =     np.array([[0,  0],[targetW-1, 0], [targetW-1, targetH-1],[0, targetH-1]], dtype='float32')
    M      =     cv.getPerspectiveTransform(rect ,  dst)     # Calculates TransFormation Matrix, Based on Origin Points with Expected OutPut Dimensions (OutPut Points)
    warped =     cv.warpPerspective(imageNP,   M , (targetW  , targetH)  , flags=cv.INTER_CUBIC)
    return warped
def pilToBytes(pilIMG:Image.Image, fmt='PNG')->bytes:
    buf=io.BytesIO        ( )
    pilIMG.save(buf, format=fmt)
    return buf.getvalue   ( )
# UI:
state( )
btn1,btn2,btn3=st.columns(3)
with btn1:
    if    st.button('↩️ Undo' , use_container_width=True, disabled=len(st.session_state.points)==0):st.session_state.points.pop  ( )
with btn2:
    if    st.button('🧹 Clear', use_container_width=True, disabled=len(st.session_state.points)==0):st.session_state.points.clear( )
with btn3:st.write('')  # spacing
with st.sidebar:
   #st .sidebar.markdown('''[![logo](https://raw.githubusercontent.com/carlosfab/escola-data-science/master/img/novo_logo_bg_escuro.png)](https://sigmoidal.ai/)''')
    st .sidebar.markdown('''[![academy](https://sigmoidal.ai/wp-content/uploads/2024/09/Academia-Sigmoidal-Light.png)](https://escola.sigmoidal.ai/pos-graduacao-em-visao-computacional-e-deep-learning/)
    
                            Processamento Digital de Imagens I
                            
                            by Carlos Melo''')
    st .sidebar.divider (   )
    st .header('File UpLoad Area')
    upload=st.file_uploader('UpLoad Image File (PNG/JPG)', type=['png','jpg'])
    st .caption('Coordinates registered in the original image space; display may be rescaled, but points are remapped.')
    if not upload:st.sidebar.warning ('No Image Loaded!')
    st .sidebar.divider (   )
    st .sidebar.markdown('''
    ![2025.08.15   ](https://img.shields.io/badge/2025.08.15-000000)

    [![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

    [![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
    [![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
    [![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
    [![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

    [![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2025&labelColor=0065FF)](https://datavision.one/)
                        ''')
if not upload:
    st.warning('Use SideBar to UpLoad Image')
    st.stop( )
# LoadIMG:
image=Image.open(upload).convert('RGB')
origW,origH=image.size
# Fixed Resized Exhibition to Click (No Slider):
wDisplay=900
displayW=min(wDisplay, origW)
scale   =    displayW/ origW
displayH=int(origH*scale)
st.subheader('1) Click on the 4 corners of the document in any order.')
click   =img_coords(image, width=displayW, height=displayH, key='img_click_doc')
# Click Registry (Remapped from Original Space) — Freezes After 4 Clicks:
if click and ('x' in click  and 'y' in  click):
    if len(st.session_state.points)<4:
        origX=int(round(click['x']/scale))
        origY=int(round(click['y']/scale))
        st.session_state.points.append((origX, origY))
# OverLay PreView:
st.subheader('2) Points PreView')
overlay  =OverLay(image, st.session_state.points, poly=True)
col1,col2=st.columns(2)
with col1:st.image(overlay, caption=f'{len(st.session_state.points)} marked ponit(s).', use_container_width=True)
# Warp Compute (OutPut 1100 x 1600) After 4 Points:
warpedIMG=None
if len(st.session_state.points)==4:
    st.subheader('3) Rectified Document (OutPut 1100×1600)')
    imgNP =np.array(image)[:,:,::-1]   # PIL RGB -> OpenCV BGR
    warped=WarpDocument(imgNP, st.session_state.points, targetW=1100, targetH=1600)
    # Convert to PIL (BGR->RGB):
    warpedRGB=cv.cvtColor(warped, cv.COLOR_BGR2RGB)
    warpedIMG=Image.fromarray(warpedRGB)
    with col2:st.image(warpedIMG, caption='Rectified Image', use_container_width=True)
    # DownLoads:
    cdl1,cdl2=st.columns(2)
    with cdl1:st.download_button('⬇️ DownLoad Rectified Image (PNG)', data=pilToBytes(warpedIMG, fmt='PNG'),
                                 file_name='RectFiedDoc.png', mime='image/png', use_container_width=True)
    with cdl2:
        payload=[{'index':i,'x':int(x),'y':int(y)}for i,(x,y)in enumerate(st.session_state.points, start=1)]
        st.download_button('⬇️ Points (JSON)', data=json.dumps(payload, indent=2).encode('utf-8'),
                           file_name='points.json', mime='application/json', use_container_width=True)
else:
    with col2:st.warning ('Mark exactly 4 points to generate perspective correction.')
    with      st.expander('Tips & Observations'):st.markdown('''
                - **Click in Any Order**: points are automatically reordered to TL, TR, BR, BL.
                - OutPut fixed @ 1100px × 1600px.
                - Use **UnDo** or **Clear** to correct clicks.
                                                             ''')
st.toast('Ready!', icon='📑')

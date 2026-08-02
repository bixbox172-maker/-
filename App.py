import streamlit as st
import google.generativeai as genai
import os

# 1. پیج کی سیٹنگ
st.set_page_config(page_title="قرآنی الفاظ کی لغت (المعجم المفهرس)", page_icon="📖", layout="centered")
st.title("📖 قرآنی الفاظ اور مادے کی تلاش")
st.write("اپنا مادہ (Root Word) درج کریں اور اس سے بننے والے تمام منفرد قرآنی صیغے حاصل کریں۔")

# 2. API Key لینا (سائیڈ بار سے)
api_key = st.sidebar.text_input("اپنی Gemini API Key یہاں ڈالیں:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # ماڈل کی سیٹنگ (ہمیں Gemini 1.5 Pro یا Flash استعمال کرنا چاہیے جو بڑی فائلز پڑھ سکے)
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    # 3. PDF اپ لوڈ کرنے کا آپشن
    uploaded_file = st.file_uploader("المعجم المفهرس کی PDF کتاب یہاں اپ لوڈ کریں", type=['pdf'])
    
    if uploaded_file is not None:
        st.success("✅ کتاب اپ لوڈ ہو گئی ہے! (نوٹ: AI اس کتاب کے اندر سے آپ کا مادہ تلاش کرے گا)")
        
        # 4. مادہ (Root Word) پوچھنا
        maddah = st.text_input("مادہ (Root Word) لکھیں (مثلاً: ن ف ق):")
        
        if st.button("تلاش کریں"):
            if maddah:
                with st.spinner("AI کتاب میں تلاش کر رہا ہے اور الفاظ کو فلٹر کر رہا ہے۔ براہ کرم انتظار کریں..."):
                    
                    # 5. AI کو سخت ہدایات (The Magic Prompt)
                    prompt = f"""
                    آپ کے پاس 'المعجم المفهرس لألفاظ القرآن الكريم' کا ڈیٹا ہے۔
                    صارف نے یہ مادہ دیا ہے: '{maddah}'

                    آپ کا کام اس مادے سے بننے والے تمام الفاظ (صیغوں) کو تلاش کرنا اور نیچے دیے گئے اصولوں کے مطابق فلٹر کر کے جواب دینا ہے:

                    اصول نمبر 1: کوئی لفظ دہرایا نہ جائے (Remove all duplicates)۔ ایک صیغہ صرف ایک بار لکھا جائے۔
                    اصول نمبر 2: اگر کسی صیغے کے شروع یا آخر میں حروفِ زیادت یا ضمیریں (جیسے هَا، هُمْ، كُمْ، نَا، فَ، وَ، لِ وغیرہ) لگی ہوں (مثلاً يُنْفِقُونَهَا)، تو آپ نے ان ضمیروں کو ہٹا کر اس کا بنیادی صیغہ (يُنْفِقُونَ) نکالنا ہے۔
                    اصول نمبر 3: اگر ضمیر ہٹانے کے بعد والا بنیادی صیغہ فہرست میں پہلے سے موجود ہے، تو ضمیر والے لفظ کو فہرست میں شامل مت کریں۔
                    اصول نمبر 4: جواب بالکل اس فارمیٹ میں دیں:
                    
                    **مادہ:** {maddah}
                    **کل منفرد الفاظ کی تعداد:** [یہاں عدد لکھیں]
                    
                    **الفاظ کی فہرست:**
                    1. [لفظ 1]
                    2. [لفظ 2]
                    ...
                    """
                    
                    try:
                        # چونکہ Streamlit پر PDF کا سائز بڑا ہو سکتا ہے، ہم پراپمٹ کے ذریعے AI کی ذہانت استعمال کر رہے ہیں۔
                        response = model.generate_content(prompt)
                        st.subheader("نتیجہ:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"کوئی مسئلہ پیش آ گیا: {e}")
            else:
                st.warning("تلاش کرنے کے لیے پہلے مادہ (Root Word) لکھیں!")
else:
    st.info("👈 ایپ استعمال کرنے کے لیے بائیں طرف (Sidebar) میں اپنی Gemini API Key ڈالیں۔")

import pandas as pd
import sqlite3

excel_file = 'data/products.xlsx'
db_file = 'z_compressor.db'

def upload_products():
    try:
        df = pd.read_excel(excel_file)
        
        # Mapping: Tumhare Excel Headers -> Database Columns
        # Screenshot ke exact headers yahan likhe hain
        mapping = {
            'Product Name': 'name',
            'Part Number': 'part_no',
            'Category': 'category',
            'Price (₹)': 'price',
            'Description': 'description'
        }
        
        # Excel headers ko rename karo
        df = df.rename(columns=mapping)
        
        # Price column se agar koi '₹' ya ',' hai toh hata kar number banao
        if 'price' in df.columns:
            df['price'] = df['price'].replace(r'[₹,]', '', regex=True).astype(float)

        conn = sqlite3.connect(db_file)
        
        # Jo column DB mein hai par Excel mein nahi (jaise image) use add karo
        if 'image' not in df.columns:
            df['image'] = 'default.jpg'
            
        # Sirf wahi columns jo database mangta hai
        final_cols = ['name', 'part_no', 'category', 'price', 'description', 'image']
        
        # Missing values ko 'N/A' se bharo
        df = df.reindex(columns=final_cols).fillna('N/A')

        # 'append' ko badal kar 'replace' kar do
        df.to_sql('inventory', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        
        print(f"✅ DHAMAKA! {len(df)} products successfully load ho gaye hain.")
        print("Ab browser mein check karo Aman!")

    except Exception as e:
        print(f"❌ Abhi bhi error hai: {e}")

if __name__ == '__main__':
    upload_products()
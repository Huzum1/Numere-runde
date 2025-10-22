import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import io

# Page config
st.set_page_config(
    page_title="Smart Number Generator",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title("🎯 Smart Number Generator")
st.markdown("*Generator inteligent de numere cu algoritm hibrid de filtrare*")

# Sidebar for algorithm weights
st.sidebar.header("⚙️ Configurare Algoritm")
st.sidebar.markdown("Ajustează greutățile criteriilor:")

freq_weight = st.sidebar.slider("Frecvență Numere", 0, 100, 45, 5, help="Cât de des apar numerele în runde")
match_complete_weight = st.sidebar.slider("Match Complet (4/4, 3/4)", 0, 100, 33, 5, help="Match-uri complete și parțiale mari")
match_partial_weight = st.sidebar.slider("Match Parțial (2/4)", 0, 100, 12, 5, help="Match-uri parțiale mici")
distribution_weight = st.sidebar.slider("Distribuție Echilibrată", 0, 100, 10, 5, help="Distribuție pare/impare")

# Show total weight
total_weight = freq_weight + match_complete_weight + match_partial_weight + distribution_weight
st.sidebar.markdown(f"**Total:** {total_weight}%")
if total_weight != 100:
    st.sidebar.warning("⚠️ Total nu este 100%")

st.sidebar.markdown("---")

# Configuration section
st.header("📝 Configurare")
col1, col2, col3 = st.columns(3)

with col1:
    total_numbers = st.number_input("Număr total numere în joc", min_value=10, max_value=200, value=49, step=1)
    
with col2:
    numbers_per_combo = st.number_input("Numere per combinație", min_value=2, max_value=20, value=4, step=1)
    
with col3:
    output_count = st.number_input("Variante finale de extras", min_value=1, max_value=10000, value=1000, step=100)

st.markdown("---")

# Upload sections
col_upload1, col_upload2 = st.columns(2)

variants_data = None
rounds_data = None

with col_upload1:
    st.subheader("📤 Variante (10000)")
    
    variant_tab1, variant_tab2 = st.tabs(["📁 Upload Fișier", "✍️ Introducere Manuală"])
    
    with variant_tab1:
        st.caption("Format: ID, num1 num2 num3 num4")
        variants_file = st.file_uploader("Alege fișier .txt cu variante", type=['txt'], key="variants")
        
        if variants_file:
            try:
                content = variants_file.read().decode('utf-8')
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                variants_list = []
                for line in lines:
                    if ',' in line:
                        parts = line.split(',', 1)
                        variant_id = parts[0].strip()
                        numbers = [int(x) for x in parts[1].strip().split()]
                        variants_list.append({'id': variant_id, 'numbers': numbers})
                
                variants_data = variants_list
                
                # Statistics
                st.success(f"✅ {len(variants_data)} variante încărcate")
                
                all_numbers = [num for v in variants_data for num in v['numbers']]
                unique_numbers = set(all_numbers)
                counter = Counter(all_numbers)
                most_common = counter.most_common(1)[0]
                least_common = counter.most_common()[-1]
                
                st.markdown(f"""
                **Statistici:**
                - Numere unice folosite: **{len(unique_numbers)} din {total_numbers}**
                - Cel mai frecvent: **{most_common[0]}** (apare de {most_common[1]}× ori)
                - Cel mai rar: **{least_common[0]}** (apare de {least_common[1]}× ori)
                """)
                
                # Preview
                with st.expander("👁️ Preview primele 5 variante"):
                    for i, v in enumerate(variants_data[:5]):
                        st.text(f"{v['id']}, {' '.join(map(str, v['numbers']))}")
                        
            except Exception as e:
                st.error(f"❌ Eroare la citirea fișierului: {str(e)}")
    
    with variant_tab2:
        st.caption("Format: O variantă per linie - ID, num1 num2 num3 num4")
        manual_variants = st.text_area(
            "Introdu variantele aici:",
            height=200,
            placeholder="1, 5 12 23 34\n2, 7 15 22 38\n3, 3 14 27 41",
            key="manual_variants"
        )
        
        if manual_variants.strip():
            try:
                lines = [line.strip() for line in manual_variants.split('\n') if line.strip()]
                
                variants_list = []
                for line in lines:
                    if ',' in line:
                        parts = line.split(',', 1)
                        variant_id = parts[0].strip()
                        numbers = [int(x) for x in parts[1].strip().split()]
                        variants_list.append({'id': variant_id, 'numbers': numbers})
                
                variants_data = variants_list
                
                # Statistics
                st.success(f"✅ {len(variants_data)} variante introduse")
                
                all_numbers = [num for v in variants_data for num in v['numbers']]
                unique_numbers = set(all_numbers)
                counter = Counter(all_numbers)
                most_common = counter.most_common(1)[0]
                least_common = counter.most_common()[-1]
                
                st.markdown(f"""
                **Statistici:**
                - Numere unice folosite: **{len(unique_numbers)} din {total_numbers}**
                - Cel mai frecvent: **{most_common[0]}** (apare de {most_common[1]}× ori)
                - Cel mai rar: **{least_common[0]}** (apare de {least_common[1]}× ori)
                """)
                
                # Preview
                with st.expander("👁️ Preview primele 5 variante"):
                    for i, v in enumerate(variants_data[:5]):
                        st.text(f"{v['id']}, {' '.join(map(str, v['numbers']))}")
                        
            except Exception as e:
                st.error(f"❌ Eroare la procesarea variantelor: {str(e)}")

with col_upload2:
    st.subheader("📤 Runde Câștigătoare (100+)")
    
    rounds_tab1, rounds_tab2 = st.tabs(["📁 Upload Fișier", "✍️ Introducere Manuală"])
    
    with rounds_tab1:
        st.caption("Format: num1, num2, num3, num4 (o rundă per linie)")
        rounds_file = st.file_uploader("Alege fișier .txt cu runde", type=['txt'], key="rounds")
        
        if rounds_file:
            try:
                content = rounds_file.read().decode('utf-8')
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                rounds_list = []
                for line in lines:
                    # Handle comma-separated numbers
                    numbers = [int(x.strip()) for x in line.split(',') if x.strip()]
                    rounds_list.append(numbers)
                
                rounds_data = rounds_list
                
                # Statistics
                st.success(f"✅ {len(rounds_data)} runde încărcate")
                
                all_round_numbers = [num for r in rounds_data for num in r]
                counter = Counter(all_round_numbers)
                top_5 = counter.most_common(5)
                
                even_count = sum(1 for num in all_round_numbers if num % 2 == 0)
                odd_count = len(all_round_numbers) - even_count
                even_pct = (even_count / len(all_round_numbers) * 100) if all_round_numbers else 0
                odd_pct = 100 - even_pct
                
                avg_sum = np.mean([sum(r) for r in rounds_data])
                
                top_5_str = ", ".join([f"{num}({count}×)" for num, count in top_5])
                
                st.markdown(f"""
                **Analiza Rundelor:**
                - Total runde: **{len(rounds_data)}**
                - Top 5 frecvente: **{top_5_str}**
                - Pare/Impare: **{even_pct:.0f}% / {odd_pct:.0f}%**
                - Media sumei: **{avg_sum:.1f}**
                """)
                
                # Preview
                with st.expander("👁️ Preview primele 5 runde"):
                    for i, r in enumerate(rounds_data[:5]):
                        st.text(', '.join(map(str, r)))
                        
            except Exception as e:
                st.error(f"❌ Eroare la citirea fișierului: {str(e)}")
    
    with rounds_tab2:
        st.caption("Format: O rundă per linie - num1, num2, num3, num4")
        manual_rounds = st.text_area(
            "Introdu rundele aici:",
            height=200,
            placeholder="24, 46, 47, 44, 3, 60, 25, 33, 27, 40, 1, 58\n5, 12, 23, 34\n7, 15, 22, 38",
            key="manual_rounds"
        )
        
        if manual_rounds.strip():
            try:
                lines = [line.strip() for line in manual_rounds.split('\n') if line.strip()]
                
                rounds_list = []
                for line in lines:
                    # Handle comma-separated numbers
                    numbers = [int(x.strip()) for x in line.split(',') if x.strip()]
                    rounds_list.append(numbers)
                
                rounds_data = rounds_list
                
                # Statistics
                st.success(f"✅ {len(rounds_data)} runde introduse")
                
                all_round_numbers = [num for r in rounds_data for num in r]
                counter = Counter(all_round_numbers)
                top_5 = counter.most_common(5)
                
                even_count = sum(1 for num in all_round_numbers if num % 2 == 0)
                odd_count = len(all_round_numbers) - even_count
                even_pct = (even_count / len(all_round_numbers) * 100) if all_round_numbers else 0
                odd_pct = 100 - even_pct
                
                avg_sum = np.mean([sum(r) for r in rounds_data])
                
                top_5_str = ", ".join([f"{num}({count}×)" for num, count in top_5])
                
                st.markdown(f"""
                **Analiza Rundelor:**
                - Total runde: **{len(rounds_data)}**
                - Top 5 frecvente: **{top_5_str}**
                - Pare/Impare: **{even_pct:.0f}% / {odd_pct:.0f}%**
                - Media sumei: **{avg_sum:.1f}**
                """)
                
                # Preview
                with st.expander("👁️ Preview primele 5 runde"):
                    for i, r in enumerate(rounds_data[:5]):
                        st.text(', '.join(map(str, r)))
                        
            except Exception as e:
                st.error(f"❌ Eroare la procesarea rundelor: {str(e)}")

st.markdown("---")

# Process button
if st.button("🚀 Procesează și Filtrează", type="primary", use_container_width=True):
    if variants_data is None:
        st.error("❌ Te rog să încarci variantele!")
    elif rounds_data is None:
        st.error("❌ Te rog să încarci rundele câștigătoare!")
    elif total_weight != 100:
        st.error("❌ Suma greutăților trebuie să fie 100%!")
    else:
        with st.spinner("⏳ Procesare în curs... Acest lucru poate dura câteva secunde..."):
            
            # Calculate frequency scores
            round_numbers_freq = Counter([num for r in rounds_data for num in r])
            max_freq = max(round_numbers_freq.values()) if round_numbers_freq else 1
            
            variant_scores = []
            
            for variant in variants_data:
                variant_nums = set(variant['numbers'])
                
                # 1. Frequency score (45%)
                freq_score = sum(round_numbers_freq.get(num, 0) for num in variant_nums) / (max_freq * len(variant_nums))
                freq_score = freq_score * (freq_weight / 100)
                
                # 2. Match complete score (33%) - 4/4 and 3/4
                match_4 = 0
                match_3 = 0
                match_2 = 0
                
                for round_nums in rounds_data:
                    round_set = set(round_nums)
                    matches = len(variant_nums & round_set)
                    
                    if matches == len(variant_nums):  # Full match (4/4)
                        match_4 += 1
                    elif matches == len(variant_nums) - 1:  # 3/4
                        match_3 += 1
                    elif matches == len(variant_nums) - 2:  # 2/4
                        match_2 += 1
                
                # Weight 4/4 more than 3/4
                match_complete_score = (match_4 * 1.0 + match_3 * 0.6) / len(rounds_data)
                match_complete_score = match_complete_score * (match_complete_weight / 100)
                
                # 3. Partial match score (12%) - 2/4
                match_partial_score = match_2 / len(rounds_data)
                match_partial_score = match_partial_score * (match_partial_weight / 100)
                
                # 4. Distribution score (10%)
                even_count = sum(1 for num in variant_nums if num % 2 == 0)
                odd_count = len(variant_nums) - even_count
                # Closer to 50/50 is better
                balance = 1 - abs(even_count - odd_count) / len(variant_nums)
                distribution_score = balance * (distribution_weight / 100)
                
                # Total score
                total_score = freq_score + match_complete_score + match_partial_score + distribution_score
                
                variant_scores.append({
                    'id': variant['id'],
                    'numbers': variant['numbers'],
                    'score': total_score,
                    'match_4': match_4,
                    'match_3': match_3,
                    'match_2': match_2
                })
            
            # Sort by score and get top N
            variant_scores.sort(key=lambda x: x['score'], reverse=True)
            top_variants = variant_scores[:output_count]
            
            # Results statistics
            st.success("✅ Procesare completă!")
            
            match_4_count = sum(1 for v in top_variants if v['match_4'] > 0)
            match_3_count = sum(1 for v in top_variants if v['match_3'] > 0)
            match_2_count = sum(1 for v in top_variants if v['match_2'] > 0)
            avg_score = np.mean([v['score'] for v in top_variants])
            
            st.markdown(f"""
            **📊 Rezultate Filtrate:**
            - Variante selectate: **{len(top_variants)} din {len(variants_data)}**
            - Scor mediu: **{avg_score*100:.1f}/100**
            - Match-uri 4/4: **{match_4_count} variante**
            - Match-uri 3/4: **{match_3_count} variante**
            - Match-uri 2/4: **{match_2_count} variante**
            """)
            
            # Prepare output text
            output_lines = []
            for v in top_variants:
                line = f"{v['id']}, {' '.join(map(str, v['numbers']))}"
                output_lines.append(line)
            
            output_text = '\n'.join(output_lines)
            
            # Download button
            st.download_button(
                label="📥 Download Variante Filtrate (.txt)",
                data=output_text,
                file_name="variante_filtrate.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Preview
            with st.expander("👁️ Preview primele 20 variante filtrate"):
                for v in top_variants[:20]:
                    st.text(f"{v['id']}, {' '.join(map(str, v['numbers']))}")

# Footer
st.markdown("---")
st.markdown("*Dezvoltat cu Streamlit | Algoritm Hibrid de Filtrare*")

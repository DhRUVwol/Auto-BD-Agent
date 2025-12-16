import random
import pandas as pd
import streamlit as st

def generate_mock_leads():
    titles = [
        "Director of Toxicology", "Safety Scientist", "Head of Hepatic Safety", 
        "3D Model Specialist", "Junior Scientist", "Research Associate", 
        "Lab Technician", "VP of Oncology", "Data Analyst", "CEO"
    ]
    companies = [
        "LiverTech", "PharmaBig", "BioStart", "SafeMeds", "ToxSolutions", 
        "GenericPharma", "TechBio", "HealthCorp", "UniLabs", "MediCare"
    ]
    funding_stages = ["Series A", "Series B", "Seed", "IPO", "Bootstrapped", "Series C"]
    locations = [
        "Boston, MA", "Cambridge, MA", "San Francisco, Bay Area", "Basel, Switzerland", 
        "London, UK (Golden Triangle)", "Austin, TX", "New York, NY", "Remote", "Chicago, IL"
    ]
    papers = [
        "Drug-Induced Liver Injury in 3D Models", "DILI prediction using organoids", 
        "Novel cancer therapies", "General toxicology review", 
        "Machine Learning in Biology", "Effects of aspirin", 
        "Hepatic toxicity markers", "None", "Climate change in biology"
    ]
    
    leads = [
        {
            "Name": "Dr. Sarah Chen",
            "Job Title": "Director of Toxicology",
            "Company": "BioLiver Systems",
            "Company Funding Stage": "Series B",
            "Person Location": "Boston, MA",
            "Company HQ": "Cambridge, MA",
            "Recent Papers": "Mechanisms of Drug-Induced Liver Injury (DILI)",
            "Email": "sarah.chen@bioliver.com",
            "Technographics": "Uses In-vitro models"
        },
        {
            "Name": "James Smith",
            "Job Title": "Head of Hepatic Safety",
            "Company": "Hepatox Inc",
            "Company Funding Stage": "Series A",
            "Person Location": "Bay Area",
            "Company HQ": "San Francisco, CA",
            "Recent Papers": "Predicting DILI with NAMs",
            "Email": "j.smith@hepatox.io",
            "Technographics": "Uses NAMs"
        },
        {
            "Name": "Mike Jones",
            "Job Title": "Junior Scientist",
            "Company": "BioConsult",
            "Company Funding Stage": "Bootstrapped",
            "Person Location": "Remote",
            "Company HQ": "Austin, TX",
            "Recent Papers": "None",
            "Email": "mike@bioconsult.com",
            "Technographics": "None"
        },
        {
            "Name": "Emily White",
            "Job Title": "Marketing Manager",
            "Company": "HealthCorp",
            "Company Funding Stage": "IPO",
            "Person Location": "New York, NY",
            "Company HQ": "New York, NY",
            "Recent Papers": "Marketing strategies for pharma",
            "Email": "emily@healthcorp.com",
            "Technographics": "Standard CRM"
        }
    ]

    while len(leads) < 20:
        leads.append({
            "Name": f"User {len(leads)+1}",
            "Job Title": random.choice(titles),
            "Company": random.choice(companies),
            "Company Funding Stage": random.choice(funding_stages),
            "Person Location": random.choice(locations),
            "Company HQ": random.choice(locations),
            "Recent Papers": random.choice(papers),
            "Email": f"user{len(leads)+1}@example.com",
            "Technographics": random.choice(["Uses NAMs", "Uses In-vitro models", "Standard Lab Equip", "None"])
        })
        
    return pd.DataFrame(leads)

def calculate_propensity_score(row):
    score = 0
    
    # Role Fit
    title_upper = str(row['Job Title']).upper()
    if any(k in title_upper for k in ["TOXICOLOGY", "SAFETY", "HEPATIC", "3D"]):
        score += 30
        
    # Company Intent
    if str(row['Company Funding Stage']) in ["Series A", "Series B"]:
        score += 20
        
    # Location
    target_locs = ["BOSTON", "CAMBRIDGE", "BAY AREA", "BASEL", "UK GOLDEN TRIANGLE"]
    loc_person = str(row['Person Location']).upper()
    loc_hq = str(row['Company HQ']).upper()
    if any(l in loc_person for l in target_locs) or any(l in loc_hq for l in target_locs):
        score += 15
        
    # Scientific Intent
    papers = str(row['Recent Papers']).upper()
    if "DRUG-INDUCED LIVER INJURY" in papers or "DILI" in papers:
        score += 40
        
    # Technographic
    tech = str(row.get('Technographics', '')).upper()
    if "NAMS" in tech or "IN-VITRO MODELS" in tech:
        score += 10
        
    return min(score, 100)

st.set_page_config(page_title="Auto-BD: Intelligent Lead Scorer", layout="wide")
st.title("Auto-BD: Intelligent Lead Scorer")
st.markdown("### Identify & Score B2B Buyers for 3D In-Vitro Models")

if 'data' not in st.session_state:
    st.session_state.data = generate_mock_leads()

df = st.session_state.data.copy()
df['Probability Score'] = df.apply(calculate_propensity_score, axis=1)

# Sidebar
st.sidebar.header("Filter Controls")
min_score = st.sidebar.slider("Filter by Minimum Score", 0, 100, 0)
df = df[df['Probability Score'] >= min_score]

all_locations = sorted(list(set(df['Person Location'].unique())))
selected_locs = st.sidebar.multiselect("Filter by Location", all_locations, default=all_locations)
if selected_locs:
    df = df[df['Person Location'].isin(selected_locs)]

# Metrics
if not df.empty:
    top_lead = df.loc[df['Probability Score'].idxmax()]
    st.metric("Top Qualified Lead", f"{top_lead['Name']}", f"{top_lead['Probability Score']}% Match")
    st.caption(f"{top_lead['Job Title']} at {top_lead['Company']}")
else:
    st.metric("Top Qualified Lead", "N/A", "0% Match")

col1, col2 = st.columns(2)
col1.metric("Total Leads Identified", len(df))
col2.metric("Average Propensity Score", round(df['Probability Score'].mean(), 1) if not df.empty else 0)

st.divider()

# Search and Display
search_term = st.text_input("Search", "")
if search_term:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    df = df[mask]

df = df.sort_values(by='Probability Score', ascending=False)
st.subheader("Lead Database")

styled_df = df.style.background_gradient(subset=['Probability Score'], cmap="Greens", vmin=0, vmax=100)

st.dataframe(
    styled_df,
    use_container_width=True,
    column_config={
        "Probability Score": st.column_config.ProgressColumn(
            "Propensity Score",
            format="%d",
            min_value=0,
            max_value=100,
        ),
    }
)

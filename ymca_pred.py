import streamlit as st
import plotly.graph_objects as go

st.title("YMCA Revenue Calculator")

st.sidebar.header("User Input Features")

#Ergs
ergs = st.sidebar.selectbox("Ergs (10 - 14)", list(range(10, 15)))

# YMCA Participants
ymca_participants = st.sidebar.number_input("YMCA Participants ($60)", min_value=0, max_value=ergs, value=5, step=1)

# Non-YMCA Participants
non_ymca_participants = st.sidebar.number_input("Non-YMCA Participants ($70)", min_value=0, max_value=ergs, value=0, step=1)

# Sessions
sessions = st.sidebar.selectbox("Sessions (1 - 4)", [1, 2, 3, 4])

# Months
months = st.sidebar.selectbox("Months (1 - 2)", [1, 2])

# Coach Fee %
coach_fee_percentage = st.sidebar.slider("Coach Fee Percentage", min_value=0, max_value=100, value=50, step=1)
asst_fee_percentage = st.sidebar.slider("Assistant Coach Fee Percentage", min_value=0, max_value=100-coach_fee_percentage, value=10, step=1)
gem_city_fee_percentage = 100 - (coach_fee_percentage + asst_fee_percentage)

# Cost calculation
ymca_cost = 60
non_ymca_cost = 70

total_participants = (ymca_participants + non_ymca_participants) * sessions * months
total_rev = (ymca_participants * ymca_cost + non_ymca_participants * non_ymca_cost) * sessions * months

# Revenue breakdown visualization
st.header("Revenue Breakdown")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Calculated Cost")
    st.write(f"Total Participants: {total_participants}")
    st.write(f"Youth Participants: {(ymca_participants*sessions*months)/2}")
    st.write(f"Gross Revenue: ${total_rev:,.2f}")
    st.write(f"YMCA Fee (40%): ${total_rev * 0.40:,.2f}")
    st.write(f"Gem City Fee (60%): ${total_rev * 0.60:,.2f}")
    st.write(f"Head Coach Fee ({coach_fee_percentage}%): ${(total_rev * .6) *(coach_fee_percentage / 100):,.2f}")
    st.write(f"Assistant Coach Fee ({asst_fee_percentage}%): ${(total_rev * .6) *(asst_fee_percentage / 100):,.2f}")
    st.write(f"Gem City Revenue ({gem_city_fee_percentage}%): ${(total_rev * .6) * (gem_city_fee_percentage / 100):,.2f}")

with col1:
    # Calculate individual components
    ymca_fee = total_rev * 0.40
    gem_city_fee = total_rev * 0.60
    head_coach_fee = (total_rev * .6) * (coach_fee_percentage / 100)
    asst_coach_fee = (total_rev * .6) * (asst_fee_percentage / 100)
    gem_city_revenue = (total_rev * .6) * (gem_city_fee_percentage / 100)

    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[total_participants],
        y=[total_rev],
        name='Gross Revenue',
        marker_color='lightblue'
    ))

    fig.add_trace(go.Bar(
        x=[total_participants],
        y=[gem_city_fee],
        name='Gem City Fee (60%)',
        marker_color='orange'
    ))

    fig.add_trace(go.Bar(
        x=[total_participants],
        y=[head_coach_fee],
        name=f'Head Coach Fee ({coach_fee_percentage}%)',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=[total_participants],
        y=[asst_coach_fee],
        name=f'Assistant Coach Fee ({asst_fee_percentage}%)',
        marker_color='purple'
    ))

    fig.add_trace(go.Bar(
        x=[total_participants],
        y=[gem_city_revenue],
        name=f'Gem City Revenue ({gem_city_fee_percentage}%)',
        marker_color='red'
    ))

    fig.update_layout(
        title=f'Revenue Components by {total_participants} Total Participants',
        # xaxis_title='Total Participants',
        yaxis_title='Revenue ($)',
        barmode='group',
        hovermode='x unified',
        showlegend=True,
        xaxis=dict(showticklabels=False)
    )

    st.plotly_chart(fig, use_container_width=True)

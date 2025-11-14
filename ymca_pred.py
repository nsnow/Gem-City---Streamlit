import streamlit as st
import plotly.graph_objects as go

st.title("YMCA Revenue Calculator")

st.sidebar.header("User Input Features")

#Ergs
ergs = st.sidebar.slider("Ergs (10 - 14)", min_value=10, max_value=14, value=10, step=1)

# YMCA Participants
ymca_participants = st.sidebar.slider("YMCA Participants ($60)", min_value=0, max_value=ergs, value=5, step=1)

# Non-YMCA Participants
non_ymca_participants = st.sidebar.slider("Non-YMCA Participants ($70)", min_value=0, max_value=ergs, value=0, step=1)

# Sessions
sessions = st.sidebar.slider("Sessions (1 - 4)", min_value=1, max_value=4, value=1, step=1)

# Months
months = st.sidebar.slider("Months (1 - 2)", min_value=1, max_value=2, value=1, step=1)

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
        marker_color='#9BFF00'
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
        xaxis=dict(showticklabels=False),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

# Line graph showing revenue progression
st.header("Revenue Progression")

# Create data for line graph from 0 to total_participants
participants_range = list(range(0, total_participants + 1))

# Calculate revenue for each participant count
# Assuming proportional distribution between YMCA and non-YMCA participants
if total_participants > 0:
    ymca_ratio = (ymca_participants * sessions * months) / total_participants
    non_ymca_ratio = (non_ymca_participants * sessions * months) / total_participants
else:
    ymca_ratio = 0
    non_ymca_ratio = 0

gem_city_fee_line = []
head_coach_fee_line = []
asst_coach_fee_line = []
gem_city_revenue_line = []

for p in participants_range:
    # Calculate revenue for p participants
    ymca_p = p * ymca_ratio
    non_ymca_p = p * non_ymca_ratio
    rev = (ymca_p * ymca_cost + non_ymca_p * non_ymca_cost)
    
    gem_city_fee_val = rev * 0.60
    head_coach_fee_val = (rev * .6) * (coach_fee_percentage / 100)
    asst_coach_fee_val = (rev * .6) * (asst_fee_percentage / 100)
    gem_city_revenue_val = (rev * .6) * (gem_city_fee_percentage / 100)
    
    gem_city_fee_line.append(gem_city_fee_val)
    head_coach_fee_line.append(head_coach_fee_val)
    asst_coach_fee_line.append(asst_coach_fee_val)
    gem_city_revenue_line.append(gem_city_revenue_val)

# Create line graph
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=participants_range,
    y=gem_city_fee_line,
    mode='lines',
    name='Gem City Fee (60%)',
    line=dict(color='#9BFF00', width=2)
))

fig2.add_trace(go.Scatter(
    x=participants_range,
    y=head_coach_fee_line,
    mode='lines',
    name=f'Head Coach Fee ({coach_fee_percentage}%)',
    line=dict(color='green', width=2)
))

fig2.add_trace(go.Scatter(
    x=participants_range,
    y=asst_coach_fee_line,
    mode='lines',
    name=f'Assistant Coach Fee ({asst_fee_percentage}%)',
    line=dict(color='purple', width=2)
))

fig2.add_trace(go.Scatter(
    x=participants_range,
    y=gem_city_revenue_line,
    mode='lines',
    name=f'Gem City Revenue ({gem_city_fee_percentage}%)',
    line=dict(color='red', width=2)
))

fig2.update_layout(
    title='Revenue Progression by Participants',
    xaxis_title='Total Participants',
    yaxis_title='Revenue ($)',
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

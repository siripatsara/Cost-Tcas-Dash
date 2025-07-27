import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# อ่านข้อมูล
df = pd.read_csv('tcas_cleaned.csv')

# ทำความสะอาดข้อมูล
df['ค่าใช้จ่ายต่อภาค'] = pd.to_numeric(df['ค่าใช้จ่ายต่อภาค'], errors='coerce')
df['ค่าใช้จ่ายตลอดหลักสูตร'] = pd.to_numeric(
    df['ค่าใช้จ่ายตลอดหลักสูตร'], errors='coerce')

# สร้างตัวแปรสำหรับการจัดกลุ่มมหาวิทยาลัย


def categorize_university(uni_name):
    if 'จุฬาลงกรณ์' in uni_name:
        return 'Top Tier'
    elif any(x in uni_name for x in ['เกษตรศาสตร์', 'ขอนแก่น', 'เชียงใหม่', 'ธรรมศาสตร์', 'มหิดล', 'สงขลานครินทร์']):
        return 'Public Research'
    elif 'เทคโนโลยี' in uni_name or 'สถาบัน' in uni_name:
        return 'Technology Institute'
    elif 'ราชภัฏ' in uni_name or 'ราชมงคล' in uni_name:
        return 'Regional Public'
    else:
        return 'Private'


df['University_Category'] = df['มหาวิทยาลัย'].apply(categorize_university)

# สร้าง Dash app
app = dash.Dash(__name__)

# ธีมสีหลัก
THEME_COLORS = {
    'primary': '#2E86AB',        # น้ำเงินเข้ม
    'secondary': '#A23B72',      # ม่วงแดง
    'accent': '#F18F01',         # ส้ม
    'success': '#C73E1D',        # แดง
    'background': '#F5F7FA',     # เทาอ่อน
    'surface': '#FFFFFF',        # ขาว
    'text_primary': '#2D3748',   # เทาเข้ม
    'text_secondary': '#718096',  # เทาอ่อน
    'border': '#E2E8F0'          # เทาขอบ
}

# สไตล์สำหรับการ์ด
card_style = {
    'backgroundColor': THEME_COLORS['surface'],
    'border': f'1px solid {THEME_COLORS["border"]}',
    'borderRadius': '16px',
    'padding': '25px',
    'margin': '15px 10px',
    'boxShadow': '0 8px 25px rgba(0,0,0,0.1)',
    'transition': 'all 0.3s ease',
    'position': 'relative',
    'overflow': 'hidden'
}

# สไตล์สำหรับ dropdown
dropdown_style = {
    'backgroundColor': THEME_COLORS['surface'],
    'border': f'2px solid {THEME_COLORS["border"]}',
    'borderRadius': '12px',
    'fontSize': '16px',
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
}

# สไตล์สำหรับหัวข้อหลัก
main_title_style = {
    'textAlign': 'center',
    'color': THEME_COLORS['primary'],
    'marginBottom': '15px',
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    'fontWeight': '700',
    'fontSize': '3.2rem',
    'background': f'linear-gradient(135deg, {THEME_COLORS["primary"]}, {THEME_COLORS["secondary"]})',
    'backgroundClip': 'text',
    'WebkitBackgroundClip': 'text',
    'WebkitTextFillColor': 'transparent',
    'letterSpacing': '1px'
}

# สไตล์สำหรับหัวข้อรอง
section_title_style = {
    'textAlign': 'center',
    'color': THEME_COLORS['text_primary'],
    'marginBottom': '25px',
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    'fontWeight': '600',
    'fontSize': '2.2rem',
    'position': 'relative',
    'paddingBottom': '15px'
}

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("🎓 University Engineering Programs Analysis",
                    style=main_title_style),
            html.P("Comprehensive Analysis of Computer Science & AI Engineering Programs in Thailand",
                   style={
                       'textAlign': 'center',
                       'color': THEME_COLORS['text_secondary'],
                       'marginBottom': '0',
                       'fontSize': '1.3rem',
                       'fontFamily': 'Inter, sans-serif',
                       'fontWeight': '400',
                       'maxWidth': '800px',
                       'margin': '0 auto'
                   })
        ], style={'maxWidth': '1200px', 'margin': '0 auto'})
    ], style={
        'padding': '40px 20px',
        'background': f'linear-gradient(135deg, {THEME_COLORS["background"]}, #E6FFFA)',
        'marginBottom': '30px',
        'position': 'relative'
    }),

    # Key Metrics Row
    html.Div([
        html.Div([
            html.Div([
                html.H3(f"{len(df)}", style={
                    'color': THEME_COLORS['primary'],
                    'fontSize': '3rem',
                    'margin': '0',
                    'fontWeight': '700'
                }),
                html.P("Total Programs", style={
                    'color': THEME_COLORS['text_secondary'],
                    'margin': '8px 0',
                    'fontSize': '1rem',
                    'fontWeight': '500'
                })
            ], style={
                **card_style,
                'textAlign': 'center',
                'width': '22%',
                'display': 'inline-block',
                'background': f'linear-gradient(135deg, {THEME_COLORS["primary"]}15, {THEME_COLORS["primary"]}05)'
            }),

            html.Div([
                html.H3(f"{df['มหาวิทยาลัย'].nunique()}", style={
                    'color': THEME_COLORS['secondary'],
                    'fontSize': '3rem',
                    'margin': '0',
                    'fontWeight': '700'
                }),
                html.P("Universities", style={
                    'color': THEME_COLORS['text_secondary'],
                    'margin': '8px 0',
                    'fontSize': '1rem',
                    'fontWeight': '500'
                })
            ], style={
                **card_style,
                'textAlign': 'center',
                'width': '22%',
                'display': 'inline-block',
                'background': f'linear-gradient(135deg, {THEME_COLORS["secondary"]}15, {THEME_COLORS["secondary"]}05)'
            }),

            html.Div([
                html.H3(f"฿{df['ค่าใช้จ่ายต่อภาค'].mean():,.0f}", style={
                    'color': THEME_COLORS['accent'],
                    'fontSize': '3rem',
                    'margin': '0',
                    'fontWeight': '700'
                }),
                html.P("Avg. Cost/Semester", style={
                    'color': THEME_COLORS['text_secondary'],
                    'margin': '8px 0',
                    'fontSize': '1rem',
                    'fontWeight': '500'
                })
            ], style={
                **card_style,
                'textAlign': 'center',
                'width': '22%',
                'display': 'inline-block',
                'background': f'linear-gradient(135deg, {THEME_COLORS["accent"]}15, {THEME_COLORS["accent"]}05)'
            }),

            html.Div([
                html.H3(f"{df['สาขาวิชา'].nunique()}", style={
                    'color': THEME_COLORS['success'],
                    'fontSize': '3rem',
                    'margin': '0',
                    'fontWeight': '700'
                }),
                html.P("Specialized Fields", style={
                    'color': THEME_COLORS['text_secondary'],
                    'margin': '8px 0',
                    'fontSize': '1rem',
                    'fontWeight': '500'
                })
            ], style={
                **card_style,
                'textAlign': 'center',
                'width': '22%',
                'display': 'inline-block',
                'background': f'linear-gradient(135deg, {THEME_COLORS["success"]}15, {THEME_COLORS["success"]}05)'
            })
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'textAlign': 'center'})
    ], style={'marginBottom': '40px'}),

    # Controls Section
    html.Div([
        html.Div([
            html.H3("Program Comparison", style={
                **section_title_style,
                'marginBottom': '30px'
            }),

            html.Div([
                # University 1 Selection
                html.Div([
                    html.Label("Select First University:", style={
                        'fontWeight': '600',
                        'color': THEME_COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block',
                        'fontSize': '1rem'
                    }),
                    dcc.Dropdown(
                        id='university-1-dropdown',
                        options=[{'label': uni, 'value': uni}
                                 for uni in sorted(df['มหาวิทยาลัย'].unique())],
                        value=df['มหาวิทยาลัย'].iloc[0] if len(
                            df) > 0 else None,
                        style={
                            **dropdown_style,
                            'zIndex': '999'  # เพิ่ม z-index
                        },
                        optionHeight=40,
                        maxHeight=200  # จำกัดความสูงของ dropdown list
                    )
                ], style={
                    'width': '30%',
                    'display': 'inline-block',
                    'marginRight': '3%',
                    'position': 'relative',  # เพิ่ม position relative
                    'zIndex': '999'  # เพิ่ม z-index สำหรับ container
                }),

                # Program 1 Selection
                html.Div([
                    html.Label("Select First Program:", style={
                        'fontWeight': '600',
                        'color': THEME_COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block',
                        'fontSize': '1rem'
                    }),
                    dcc.Dropdown(
                        id='program-1-dropdown',
                        style={
                            **dropdown_style,
                            'zIndex': '998'  # เพิ่ม z-index
                        },
                        optionHeight=40,
                        maxHeight=200
                    )
                ], style={
                    'width': '30%',
                    'display': 'inline-block',
                    'marginRight': '3%',
                    'position': 'relative',
                    'zIndex': '998'
                }),

                # Cost Type Selection
                html.Div([
                    html.Label("Cost Type:", style={
                        'fontWeight': '600',
                        'color': THEME_COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block',
                        'fontSize': '1rem',
                    }),
                    dcc.RadioItems(
                        id='cost-type',
                        options=[
                            {'label': 'Per Semester', 'value': 'ค่าใช้จ่ายต่อภาค'},
                            {'label': 'Total Program',
                                'value': 'ค่าใช้จ่ายตลอดหลักสูตร'}
                        ],
                        value='ค่าใช้จ่ายต่อภาค',
                        style={'marginTop': '10px'},
                        labelStyle={
                            'display': 'block',
                            'marginBottom': '8px',
                            'fontSize': '0.95rem',
                            'color': THEME_COLORS['text_primary']
                        }
                    )
                ], style={'width': '30%', 'display': 'inline-block'})
            ], style={
                'marginBottom': '50px',  # เพิ่ม margin bottom ให้มากขึ้น
                'overflow': 'visible'  # เพิ่ม overflow visible
            }),

            html.Div([
                # University 2 Selection
                html.Div([
                    html.Label("Select Second University:", style={
                        'fontWeight': '600',
                        'color': THEME_COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block',
                        'fontSize': '1rem'
                    }),
                    dcc.Dropdown(
                        id='university-2-dropdown',
                        options=[{'label': uni, 'value': uni}
                                 for uni in sorted(df['มหาวิทยาลัย'].unique())],
                        value=df['มหาวิทยาลัย'].iloc[1] if len(df) > 1 else (
                            df['มหาวิทยาลัย'].iloc[0] if len(df) > 0 else None),
                        style={
                            **dropdown_style,
                            'zIndex': '997'
                        },
                        optionHeight=40,
                        maxHeight=200
                    )
                ], style={
                    'width': '30%',
                    'display': 'inline-block',
                    'marginRight': '3%',
                    'position': 'relative',
                    'zIndex': '997'
                }),

                # Program 2 Selection
                html.Div([
                    html.Label("Select Second Program:", style={
                        'fontWeight': '600',
                        'color': THEME_COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block',
                        'fontSize': '1rem'
                    }),
                    dcc.Dropdown(
                        id='program-2-dropdown',
                        style={
                            **dropdown_style,
                            'zIndex': '996'
                        },
                        optionHeight=40,
                        maxHeight=200
                    )
                ], style={
                    'width': '30%',
                    'display': 'inline-block',
                    'marginRight': '3%',
                    'position': 'relative',
                    'zIndex': '996'
                })
            ], style={
                'overflow': 'visible'  # เพิ่ม overflow visible
            })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'overflow': 'visible'  # เพิ่ม overflow visible
        })
    ], style={
        **card_style,
        'marginBottom': '40px',
        'overflow': 'visible',  # เพิ่ม overflow visible
        'position': 'relative'  # เพิ่ม position relative
    }),

    # Charts Row 1 - Comparison Chart
    html.Div([
        html.Div([
            dcc.Graph(id='comparison-chart')
        ], style={
            **card_style,
            'width': '80%',
            'margin': '20px auto',
            'display': 'block'
        })
    ]),

    # Charts Row 2: Average Cost by Field
    html.Div([
        html.Div([
            html.H3("Average Cost by Field of Study", style={
                **section_title_style,
                'marginBottom': '25px'
            }),

            html.Div([
                html.Label("Filter by Program Type:", style={
                    'fontWeight': '600',
                    'color': THEME_COLORS['text_primary'],
                    'marginBottom': '15px',
                    'display': 'block',
                    'fontSize': '1.1rem',
                    'textAlign': 'center'
                }),
                html.Div([
                    dcc.RadioItems(
                        id='program-type-filter',
                        options=[{'label': pt, 'value': pt} for pt in sorted(df['ประเภทหลักสูตร'].dropna().unique())] + [
                            {'label': 'All Programs', 'value': 'all'}
                        ],
                        value='all',
                        labelStyle={
                            'display': 'inline-block',
                            'marginRight': '25px',
                            'fontSize': '1rem',
                            'color': THEME_COLORS['text_primary'],
                            'fontWeight': '500'
                        },
                        inputStyle={'marginRight': '8px'},
                        style={'textAlign': 'center'}
                    )
                ], style={'textAlign': 'center', 'marginBottom': '25px'})
            ]),

            dcc.Graph(id='field-average-cost-bar')
        ], style={'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={**card_style, 'marginBottom': '40px'}),

    # Charts Row 3: Cost Heatmap by Campus and Field
    html.Div([
        html.Div([
            html.H3("Campus vs Field of Study", style={
                **section_title_style,
                'marginBottom': '25px'
            }),
            dcc.Graph(id='cost-heatmap-campus-field')
        ], style={'maxWidth': '1400px', 'margin': '0 auto'})
    ], style={**card_style, 'marginBottom': '40px'}),

    # Key Insights
    html.Div([
        html.Div([
            html.H3("Key Insights & Recommendations", style={
                **section_title_style,
                'marginBottom': '30px'
            }),
            html.Div(id='insights-content')
        ], style={'maxWidth': '1200px', 'margin': '0 auto'})
    ], style={**card_style, 'marginBottom': '40px'})

], style={
    'backgroundColor': THEME_COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    'padding': '0',
    'marginLeft': '500',
    'justifyContent': 'center',  # แนวนอน
    'alignItems': 'center',      # แนวตั้ง
})


# Callbacks


@callback(
    [Output('program-1-dropdown', 'options'),
     Output('program-1-dropdown', 'value')],
    Input('university-1-dropdown', 'value')
)
def update_program_1_options(selected_university):
    try:
        if selected_university and selected_university in df['มหาวิทยาลัย'].values:
            programs = df[df['มหาวิทยาลัย'] ==
                          selected_university]['ชื่อหลักสูตร'].unique()
            options = [{'label': prog, 'value': prog}
                       for prog in programs if pd.notna(prog)]
            value = options[0]['value'] if len(options) > 0 else None
            return options, value
    except Exception as e:
        print(f"Error in program 1 options: {e}")
    return [], None


@callback(
    [Output('program-2-dropdown', 'options'),
     Output('program-2-dropdown', 'value')],
    Input('university-2-dropdown', 'value')
)
def update_program_2_options(selected_university):
    try:
        if selected_university and selected_university in df['มหาวิทยาลัย'].values:
            programs = df[df['มหาวิทยาลัย'] ==
                          selected_university]['ชื่อหลักสูตร'].unique()
            options = [{'label': prog, 'value': prog}
                       for prog in programs if pd.notna(prog)]
            value = options[0]['value'] if len(options) > 0 else None
            return options, value
    except Exception as e:
        print(f"Error in program 2 options: {e}")
    return [], None


@callback(
    Output('comparison-chart', 'figure'),
    [Input('university-1-dropdown', 'value'),
     Input('program-1-dropdown', 'value'),
     Input('university-2-dropdown', 'value'),
     Input('program-2-dropdown', 'value'),
     Input('cost-type', 'value')],
    prevent_initial_call=False
)
def update_comparison_chart(uni1, prog1, uni2, prog2, cost_type):
    # Create empty figure first
    fig = go.Figure()

    try:
        # Check if we have all required inputs
        if not all([uni1, prog1, uni2, prog2, cost_type]):
            fig.add_annotation(
                text="Please select universities and programs",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
        else:
            # Filter data
            data1 = df[(df['มหาวิทยาลัย'] == uni1) &
                       (df['ชื่อหลักสูตร'] == prog1)]
            data2 = df[(df['มหาวิทยาลัย'] == uni2) &
                       (df['ชื่อหลักสูตร'] == prog2)]

            if not data1.empty and not data2.empty and cost_type in df.columns:
                # Get costs safely
                cost1 = 0
                cost2 = 0

                if not data1[cost_type].empty and pd.notna(data1[cost_type].iloc[0]):
                    try:
                        cost1 = float(
                            str(data1[cost_type].iloc[0]).replace(',', ''))
                    except:
                        cost1 = 0

                if not data2[cost_type].empty and pd.notna(data2[cost_type].iloc[0]):
                    try:
                        cost2 = float(
                            str(data2[cost_type].iloc[0]).replace(',', ''))
                    except:
                        cost2 = 0

                # Create bar chart
                universities = [uni1[:25] + "..." if len(uni1) > 25 else uni1,
                                uni2[:25] + "..." if len(uni2) > 25 else uni2]
                costs = [cost1, cost2]

                fig.add_trace(go.Bar(
                    x=universities,
                    y=costs,
                    text=[f"฿{c:,.0f}" for c in costs],
                    textposition='auto',
                    marker_color=[THEME_COLORS['primary'],
                                  THEME_COLORS['secondary']],
                    name='Cost Comparison'
                ))
            else:
                fig.add_annotation(
                    text="No data available for selected programs",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=16)
                )
    except Exception as e:
        print(f"Error in comparison chart: {e}")
        fig.add_annotation(
            text="Error loading chart data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color='red')
        )

    # Update layout
    fig.update_layout(
        # title="Program Cost Comparison",
        xaxis_title="University",
        yaxis_title="Cost (THB)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        height=500,
        showlegend=False,
        margin=dict(t=80, l=60, r=40, b=80)
    )

    return fig


@callback(
    Output('field-average-cost-bar', 'figure'),
    Input('program-type-filter', 'value'),
    prevent_initial_call=False
)
def update_field_average_bar(program_type):
    fig = go.Figure()

    try:
        # Filter data
        if program_type == 'all':
            filtered_df = df.copy()
        else:
            if 'ประเภทหลักสูตร' in df.columns:
                filtered_df = df[df['ประเภทหลักสูตร'] == program_type]
            else:
                filtered_df = df.copy()

        # Check required columns
        if 'ค่าใช้จ่ายต่อภาค' not in filtered_df.columns or 'สาขาวิชา' not in filtered_df.columns:
            fig.add_annotation(
                text="Required data columns not found",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16, color='red')
            )
        else:
            # Clean data
            clean_df = filtered_df.dropna(
                subset=['สาขาวิชา', 'ค่าใช้จ่ายต่อภาค'])

            # Convert cost to numeric
            clean_df = clean_df.copy()
            clean_df['cost_numeric'] = pd.to_numeric(
                clean_df['ค่าใช้จ่ายต่อภาค'].astype(str).str.replace(',', ''),
                errors='coerce'
            )
            clean_df = clean_df.dropna(subset=['cost_numeric'])

            if not clean_df.empty:
                # Calculate averages
                avg_costs = clean_df.groupby(
                    'สาขาวิชา')['cost_numeric'].mean().sort_values(ascending=False)

                if not avg_costs.empty:
                    fields = avg_costs.index.tolist()
                    costs = avg_costs.values.tolist()

                    # Create beautiful gradient colors
                    n_bars = len(costs)
                    gradient_colors = []

                    # Beautiful color palette - from deep blue to bright cyan
                    base_colors = [
                        '#1e3a8a',  # Deep blue
                        '#3b82f6',  # Blue
                        '#06b6d4',  # Cyan
                        '#10b981',  # Emerald
                        '#f59e0b',  # Amber
                        '#ef4444',  # Red
                        '#8b5cf6',  # Violet
                        '#ec4899'   # Pink
                    ]

                    # Create gradient for each bar
                    for i in range(n_bars):
                        color_idx = i % len(base_colors)
                        gradient_colors.append(base_colors[color_idx])

                    # Create bar chart with beautiful styling
                    fig.add_trace(go.Bar(
                        x=fields,
                        y=costs,
                        text=[f"฿{c:,.0f}" for c in costs],
                        textposition='outside',
                        textfont=dict(
                            size=11,
                            color='#374151',
                            family='Arial Black'
                        ),
                        marker=dict(
                            color=gradient_colors,
                            line=dict(
                                color='rgba(255,255,255,0.8)',
                                width=2
                            ),
                            # Add gradient effect
                            pattern=dict(
                                shape="",
                                bgcolor="rgba(255,255,255,0.1)"
                            )
                        ),
                        name='Average Cost',
                        # Add hover template
                        hovertemplate="<b>%{x}</b><br>" +
                                      "Average Cost: ฿%{y:,.0f}<br>" +
                                      "<extra></extra>",
                        # Add animation effect
                        marker_opacity=0.85
                    ))

                    # Add shadow effect using a second trace
                    fig.add_trace(go.Bar(
                        x=fields,
                        # Slightly lower for shadow
                        y=[c * 0.95 for c in costs],
                        marker=dict(
                            color='rgba(0,0,0,0.1)',  # Semi-transparent black
                            line=dict(width=0)
                        ),
                        showlegend=False,
                        hoverinfo='skip',
                        yaxis='y2'
                    ))

                    # Reorder traces so shadow appears behind
                    fig.data = fig.data[::-1]

                else:
                    fig.add_annotation(
                        text="No valid cost data found",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False, font=dict(size=16)
                    )
            else:
                fig.add_annotation(
                    text="No data available for selected filter",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=16)
                )

    except Exception as e:
        print(f"Error in field average chart: {e}")
        fig.add_annotation(
            text="Error loading chart data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color='red')
        )

    # Update layout with beautiful styling
    fig.update_layout(
        xaxis_title=dict(
            text="Field of Study",
            font=dict(size=14, color='#374151', family='Arial Black')
        ),
        yaxis_title=dict(
            text="Average Cost (THB)",
            font=dict(size=14, color='#374151', family='Arial Black')
        ),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=11, color='#6b7280'),
            # gridcolor='rgba(107, 114, 128, 0.1)',
            linecolor='#e5e7eb',
            linewidth=2
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='#6b7280'),
            # gridcolor='rgba(107, 114, 128, 0.1)',
            linecolor='#e5e7eb',
            linewidth=2,
            tickformat=',.0f'
        ),
        # Add second y-axis for shadow (hidden)
        yaxis2=dict(
            overlaying='y',
            side='right',
            # showgrid=False,
            showticklabels=False,
            showline=False
        ),
        # Beautiful background
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='white',
        font=dict(family="Inter, Arial, sans-serif", size=12),
        height=600,
        showlegend=False,
        margin=dict(t=80, l=80, r=80, b=120),
        # Add subtle border
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="rgba(107, 114, 128, 0.2)", width=1)
            )
        ]
    )

    # Add beautiful animations
    fig.update_traces(
        selector=dict(type='bar'),
        marker_line_width=2,
        marker_line_color='rgba(255,255,255,0.8)'
    )

    return fig


@callback(
    Output('cost-heatmap-campus-field', 'figure'),
    Input('cost-type', 'value'),
    prevent_initial_call=False
)
def update_cost_heatmap(cost_type):
    fig = go.Figure()

    try:
        # ตรวจสอบว่ามี column ที่จำเป็นหรือไม่
        required_cols = [cost_type, 'ชื่อวิทยาเขต', 'สาขาวิชา']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            fig.add_annotation(
                text=f"Missing required columns: {', '.join(missing_cols)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16, color='red')
            )
        else:
            # ทำความสะอาดข้อมูล - ลบ NaN values
            clean_df = df.dropna(
                subset=[cost_type, 'ชื่อวิทยาเขต', 'สาขาวิชา'])

            # แปลงค่าใช้จ่ายเป็นตัวเลข
            clean_df = clean_df.copy()
            clean_df['cost_numeric'] = pd.to_numeric(
                clean_df[cost_type].astype(str).str.replace(',', ''),
                errors='coerce'
            )
            clean_df = clean_df.dropna(subset=['cost_numeric'])

            if not clean_df.empty:
                # สร้าง pivot table สำหรับ heatmap
                heatmap_data = clean_df.groupby(['ชื่อวิทยาเขต', 'สาขาวิชา'])[
                    'cost_numeric'].mean().reset_index()
                pivot_table = heatmap_data.pivot(
                    index='สาขาวิชา', columns='ชื่อวิทยาเขต', values='cost_numeric')

                # เติมค่า NaN ด้วย 0 เพื่อการแสดงผลที่ดีขึ้น
                pivot_table = pivot_table.fillna(0)

                if not pivot_table.empty:
                    # สร้างสีแบบ custom (อ่อนไปเข้มสำหรับราคาต่ำไปสูง)
                    colorscale = [
                        [0.0, '#fef7ed'],  # ครีมอ่อน
                        [0.1, '#fed7aa'],  # ส้มอ่อนมาก
                        [0.2, '#fdba74'],  # ส้มอ่อน
                        [0.3, '#fb923c'],  # ส้มปานกลาง
                        [0.4, '#f97316'],  # ส้มสด
                        [0.5, '#ea580c'],  # ส้มเข้ม
                        [0.6, '#dc2626'],  # แดงส้ม
                        [0.7, '#b91c1c'],  # แดงเข้ม
                        [0.8, '#991b1b'],  # แดงเข้มกว่า
                        [0.9, '#7f1d1d'],  # แดงเลือดหมู
                        [1.0, '#450a0a']   # แดงเกือบดำ
                    ]

                    # สร้าง heatmap
                    fig.add_trace(go.Heatmap(
                        z=pivot_table.values,
                        x=pivot_table.columns,
                        y=pivot_table.index,
                        colorscale=colorscale,
                        showscale=True,
                        colorbar=dict(
                            title=dict(
                                text="Cost (THB)",
                                font=dict(size=14, color='#374151',
                                          family='Arial Black')
                            ),
                            tickformat=',.0f',
                            tickfont=dict(size=11, color='#6b7280'),
                            len=0.8,
                            thickness=20,
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='#e5e7eb',
                            borderwidth=1
                        ),
                        hoverongaps=False,
                        hovertemplate="<b>Campus:</b> %{x}<br>" +
                        "<b>Field:</b> %{y}<br>" +
                        "<b>Average Cost:</b> ฿%{z:,.0f}<br>" +
                        "<extra></extra>",
                        # เพิ่ม text annotations บนแต่ละช่อง
                        text=[[f"฿{val:,.0f}" if val > 0 else "" for val in row]
                              for row in pivot_table.values],
                        texttemplate="%{text}",
                        textfont=dict(
                            size=9,
                            color='gray',
                            family='Arial Black'
                        ),
                        # จัดการค่า 0 ให้โปร่งใส
                        zmid=pivot_table.values.max()/2 if pivot_table.values.max() > 0 else 0
                    ))

                    # เพิ่มขอบสำหรับแต่ละช่องที่มีข้อมูล
                    shapes = []
                    for i in range(len(pivot_table.index)):
                        for j in range(len(pivot_table.columns)):
                            if pivot_table.iloc[i, j] > 0:  # เฉพาะช่องที่มีข้อมูล
                                shapes.append(dict(
                                    type="rect",
                                    x0=j-0.5, y0=i-0.5, x1=j+0.5, y1=i+0.5,
                                    line=dict(
                                        color="rgba(255,255,255,0.3)", width=1),
                                    fillcolor="rgba(0,0,0,0)"
                                ))

                else:
                    fig.add_annotation(
                        text="No data available to create heatmap",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
                        showarrow=False, font=dict(size=16)
                    )
            else:
                fig.add_annotation(
                    text="No valid data found for heatmap",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=16)
                )

    except Exception as e:
        print(f"Error in heatmap: {e}")
        fig.add_annotation(
            text="Error creating heatmap",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color='red')
        )

    # อัพเดท layout ด้วยการจัดแต่งที่สวยงาม
    fig.update_layout(
        xaxis_title=dict(
            text="Campus (ชื่อวิทยาเขต)",
            font=dict(size=14, color='#374151', family='Arial Black')
        ),
        yaxis_title=dict(
            text="Field of Study (สาขาวิชา)",
            font=dict(size=14, color='#374151', family='Arial Black')
        ),
        xaxis=dict(
            tickangle=-30,
            tickfont=dict(size=10, color='#6b7280'),
            linecolor="#d2d5da",
            linewidth=2,
            side='bottom'
        ),
        yaxis=dict(
            tickfont=dict(size=10, color='#6b7280'),
            linecolor="#d2d5da",
            linewidth=2,
            autorange='reversed'  # กลับด้านเพื่อให้เหมือน heatmap ปกติ
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, Arial, sans-serif", size=12),
        height=600,
        margin=dict(t=80, l=150, r=120, b=100),
        # เพิ่มขอบเส้นบาง ๆ
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="rgba(107, 114, 128, 0.2)", width=1),
                fillcolor="rgba(0,0,0,0)"
            )
        ]
    )

    return fig


@callback(
    Output('insights-content', 'children'),
    [Input('cost-type', 'value'),
     Input('program-type-filter', 'value')]
)
def update_insights(cost_type, program_type_filter):
    # Filter data by program type
    if program_type_filter == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['ประเภทหลักสูตร'] == program_type_filter]

    # Remove NaN values for calculations
    filtered_df = filtered_df.dropna(subset=[cost_type])

    if filtered_df.empty:
        return [html.P("No data available for selected filters",
                       style={'color': THEME_COLORS['success'], 'fontSize': '16px', 'textAlign': 'center'})]

    # Calculate statistics by field
    field_stats = filtered_df.groupby('สาขาวิชา')[cost_type].agg(
        ['mean', 'count', 'min', 'max']).round(0)

    # Calculate overall insights
    avg_cost = filtered_df[cost_type].mean()
    total_programs = len(filtered_df)
    total_universities = filtered_df['มหาวิทยาลัย'].nunique()

    # Find most expensive and cheapest programs
    if not filtered_df.empty:
        most_expensive = filtered_df.loc[filtered_df[cost_type].idxmax()]
        cheapest = filtered_df.loc[filtered_df[cost_type].idxmin()]

    insights = [
        html.Div([
            html.Div([
                html.H4("Cost Analysis Overview",
                        style={
                            'color': THEME_COLORS['primary'],
                            'marginBottom': '20px',
                            'fontSize': '1.5rem',
                            'fontWeight': '600',
                            'borderBottom': f'3px solid {THEME_COLORS["primary"]}',
                            'paddingBottom': '10px'
                        }),
                html.Div([
                    html.P(f" Total Programs: {total_programs} from {total_universities} universities",
                           style={'margin': '10px 0', 'fontSize': '1.1rem'}),
                    html.P(f" Average Cost: ฿{avg_cost:,.0f}",
                           style={'margin': '10px 0', 'fontSize': '1.1rem', 'fontWeight': '600', 'color': THEME_COLORS['accent']}),
                    html.P(f" Most Expensive: {most_expensive['ชื่อหลักสูตร'][:50]}{'...' if len(most_expensive['ชื่อหลักสูตร']) > 50 else ''}",
                           style={'margin': '10px 0', 'fontSize': '1rem'}),
                    html.P(f"    {most_expensive['มหาวิทยาลัย']} (฿{most_expensive[cost_type]:,.0f})",
                           style={'margin': '5px 0 10px 20px', 'fontSize': '0.95rem', 'color': THEME_COLORS['text_secondary']}),
                    html.P(f" Most Affordable: {cheapest['ชื่อหลักสูตร'][:50]}{'...' if len(cheapest['ชื่อหลักสูตร']) > 50 else ''}",
                           style={'margin': '10px 0', 'fontSize': '1rem'}),
                    html.P(f"    {cheapest['มหาวิทยาลัย']} (฿{cheapest[cost_type]:,.0f})",
                           style={'margin': '5px 0 10px 20px', 'fontSize': '0.95rem', 'color': THEME_COLORS['text_secondary']})
                ], style={'lineHeight': '1.6'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': f'{THEME_COLORS["primary"]}08',
                'borderRadius': '12px',
                'border': f'1px solid {THEME_COLORS["primary"]}20'
            }),

            html.Div([
                html.H4(" Field Breakdown",
                        style={
                            'color': THEME_COLORS['secondary'],
                            'marginBottom': '20px',
                            'fontSize': '1.5rem',
                            'fontWeight': '600',
                            'borderBottom': f'3px solid {THEME_COLORS["secondary"]}',
                            'paddingBottom': '10px'
                        }),
                html.Div([
                    html.Div([
                        html.P(f" {field}: {int(row['count'])} programs",
                               style={'margin': '8px 0', 'fontSize': '1rem', 'fontWeight': '600'}),
                        html.P(f"    Average: ฿{row['mean']:,.0f} | Range: ฿{row['min']:,.0f} - ฿{row['max']:,.0f}",
                               style={'margin': '5px 0 15px 20px', 'fontSize': '0.9rem', 'color': THEME_COLORS['text_secondary']})
                    ]) for field, row in field_stats.head(5).iterrows()
                ], style={'lineHeight': '1.5'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': f'{THEME_COLORS["secondary"]}08',
                'borderRadius': '12px',
                'border': f'1px solid {THEME_COLORS["secondary"]}20'
            })
        ], style={
            'display': 'flex',
            'gap': '30px',
            'textAlign': 'left'
        })
    ]

    return insights


if __name__ == '__main__':
    app.run(debug=True)

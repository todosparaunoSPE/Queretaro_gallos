# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 14:46:56 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

# Configuración de la página
st.set_page_config(
    page_title="Querétaro FC - Gestión de Ticketing",
    page_icon="⚽",
    layout="wide"
)

# Título principal
st.title("⚽ Querétaro FC - Sistema de Gestión de Ticketing")
st.markdown("**Manager, Ticket Sales & Service**")

# Inicializar session state
if 'abonados' not in st.session_state:
    st.session_state.abonados = pd.DataFrame({
        'ID': [1, 2, 3],
        'Nombre': ['Juan Pérez García', 'María López Sánchez', 'Carlos Ramírez'],
        'Email': ['juan.perez@email.com', 'maria.lopez@email.com', 'carlos.ramirez@email.com'],
        'Teléfono': ['4421234567', '4427654321', '4429876543'],
        'Tipo_Abono': ['Premium', 'General', 'Premium'],
        'Fecha_Renovación': ['2025-12-01', '2025-11-15', '2026-01-30'],
        'Estado': ['Activo', 'Activo', 'Por Renovar']
    })

if 'leads_b2b' not in st.session_state:
    st.session_state.leads_b2b = pd.DataFrame({
        'ID': [1, 2],
        'Empresa': ['Grupo Industrial QRO', 'Tech Solutions MX'],
        'Contacto': ['Ing. Roberto Martínez', 'Lic. Ana Gutiérrez'],
        'Email': ['rmartinez@grupoindustrial.com', 'agutiérrez@techsolutions.mx'],
        'Teléfono': ['4421112233', '4425556677'],
        'Interés': ['Palcos Corporativos', 'Paquetes Grupales'],
        'Estado': ['Negociación', 'Prospecto'],
        'Fecha_Contacto': ['2025-09-15', '2025-09-28']
    })

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Gestión de Abonados", "🏢 Leads B2B"])

# TAB 1: DASHBOARD
with tab1:
    st.header("Dashboard de Ticketing")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Abonados", len(st.session_state.abonados))
    
    with col2:
        activos = len(st.session_state.abonados[st.session_state.abonados['Estado'] == 'Activo'])
        st.metric("Abonados Activos", activos)
    
    with col3:
        st.metric("Leads B2B", len(st.session_state.leads_b2b))
    
    with col4:
        negociacion = len(st.session_state.leads_b2b[st.session_state.leads_b2b['Estado'] == 'Negociación'])
        st.metric("En Negociación", negociacion)
    
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Distribución por Tipo de Abono")
        tipo_counts = st.session_state.abonados['Tipo_Abono'].value_counts()
        st.bar_chart(tipo_counts)
    
    with col_b:
        st.subheader("Estado de Leads B2B")
        lead_counts = st.session_state.leads_b2b['Estado'].value_counts()
        st.bar_chart(lead_counts)

# TAB 2: GESTIÓN DE ABONADOS
with tab2:
    st.header("Gestión de Base de Datos de Abonados")
    
    subtab1, subtab2, subtab3 = st.tabs(["Ver Abonados", "Agregar Abonado", "Plan de Puntos de Contacto"])
    
    with subtab1:
        st.subheader("Lista de Abonados y Aficionados")
        
        # Filtros
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_tipo = st.multiselect(
                "Filtrar por Tipo de Abono",
                options=st.session_state.abonados['Tipo_Abono'].unique(),
                default=st.session_state.abonados['Tipo_Abono'].unique()
            )
        
        with col_f2:
            filtro_estado = st.multiselect(
                "Filtrar por Estado",
                options=st.session_state.abonados['Estado'].unique(),
                default=st.session_state.abonados['Estado'].unique()
            )
        
        # Aplicar filtros
        df_filtrado = st.session_state.abonados[
            (st.session_state.abonados['Tipo_Abono'].isin(filtro_tipo)) &
            (st.session_state.abonados['Estado'].isin(filtro_estado))
        ]
        
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
        
        # Descargar datos
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos en CSV",
            data=csv,
            file_name=f'abonados_queretaro_fc_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    with subtab2:
        st.subheader("Agregar Nuevo Abonado")
        
        with st.form("form_abonado"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre Completo*")
                email = st.text_input("Email*")
                telefono = st.text_input("Teléfono*")
            
            with col2:
                tipo_abono = st.selectbox("Tipo de Abono*", ["General", "Premium", "VIP"])
                fecha_renovacion = st.date_input("Fecha de Renovación*")
                estado = st.selectbox("Estado*", ["Activo", "Por Renovar", "Inactivo"])
            
            submitted = st.form_submit_button("➕ Agregar Abonado")
            
            if submitted:
                if nombre and email and telefono:
                    nuevo_id = st.session_state.abonados['ID'].max() + 1
                    nuevo_abonado = pd.DataFrame({
                        'ID': [nuevo_id],
                        'Nombre': [nombre],
                        'Email': [email],
                        'Teléfono': [telefono],
                        'Tipo_Abono': [tipo_abono],
                        'Fecha_Renovación': [fecha_renovacion.strftime('%Y-%m-%d')],
                        'Estado': [estado]
                    })
                    st.session_state.abonados = pd.concat([st.session_state.abonados, nuevo_abonado], ignore_index=True)
                    st.success(f"✅ Abonado {nombre} agregado exitosamente!")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor completa todos los campos obligatorios")
    
    with subtab3:
        st.subheader("Plan de Puntos de Contacto con Abonados")
        
        st.markdown("""
        **Estrategia de comunicación institucional para abonados:**
        
        1. **Comunicación Pre-Temporada** (Julio-Agosto)
           - Email de bienvenida y renovación
           - Beneficios exclusivos del abono
           - Calendario de partidos
        
        2. **Durante la Temporada** (Septiembre-Mayo)
           - Recordatorios de partido (3 días antes)
           - Encuestas de satisfacción post-partido
           - Ofertas exclusivas en tienda oficial
        
        3. **Comunicación de Renovación** (Mayo-Junio)
           - Campaña de renovación temprana
           - Descuentos por fidelidad
           - Eventos exclusivos para abonados
        """)
        
        st.divider()
        
        st.subheader("📧 Enviar Comunicación Masiva")
        
        with st.form("form_comunicacion"):
            segmento = st.multiselect(
                "Segmento de Abonados",
                options=st.session_state.abonados['Tipo_Abono'].unique()
            )
            
            asunto = st.text_input("Asunto del Email")
            mensaje = st.text_area("Mensaje", height=150)
            
            enviado = st.form_submit_button("📤 Enviar Comunicación")
            
            if enviado and segmento and asunto and mensaje:
                destinatarios = st.session_state.abonados[
                    st.session_state.abonados['Tipo_Abono'].isin(segmento)
                ]
                st.success(f"✅ Comunicación enviada a {len(destinatarios)} abonados del segmento {', '.join(segmento)}")

# TAB 3: LEADS B2B
with tab3:
    st.header("Generación de Leads B2B")
    
    subtab1, subtab2 = st.tabs(["Ver Leads", "Agregar Lead"])
    
    with subtab1:
        st.subheader("Base de Datos de Leads B2B")
        
        # Filtro por estado
        filtro_lead = st.multiselect(
            "Filtrar por Estado",
            options=st.session_state.leads_b2b['Estado'].unique(),
            default=st.session_state.leads_b2b['Estado'].unique()
        )
        
        df_leads_filtrado = st.session_state.leads_b2b[
            st.session_state.leads_b2b['Estado'].isin(filtro_lead)
        ]
        
        st.dataframe(df_leads_filtrado, use_container_width=True, hide_index=True)
        
        # Descargar leads
        csv_leads = df_leads_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Leads en CSV",
            data=csv_leads,
            file_name=f'leads_b2b_queretaro_fc_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    with subtab2:
        st.subheader("Agregar Nuevo Lead B2B")
        
        st.markdown("**Mercado Local y Regional - Querétaro**")
        
        with st.form("form_lead"):
            col1, col2 = st.columns(2)
            
            with col1:
                empresa = st.text_input("Nombre de la Empresa*")
                contacto = st.text_input("Nombre del Contacto*")
                email_lead = st.text_input("Email*")
                telefono_lead = st.text_input("Teléfono*")
            
            with col2:
                interes = st.selectbox(
                    "Interés*",
                    ["Palcos Corporativos", "Paquetes Grupales", "Patrocinio", "Eventos Empresariales", "Hospitalidad VIP"]
                )
                estado_lead = st.selectbox("Estado*", ["Prospecto", "Contactado", "Negociación", "Cerrado", "Descartado"])
                fecha_contacto = st.date_input("Fecha de Contacto*", value=date.today())
            
            notas = st.text_area("Notas adicionales", height=100)
            
            submitted_lead = st.form_submit_button("➕ Agregar Lead")
            
            if submitted_lead:
                if empresa and contacto and email_lead and telefono_lead:
                    nuevo_id_lead = st.session_state.leads_b2b['ID'].max() + 1
                    nuevo_lead = pd.DataFrame({
                        'ID': [nuevo_id_lead],
                        'Empresa': [empresa],
                        'Contacto': [contacto],
                        'Email': [email_lead],
                        'Teléfono': [telefono_lead],
                        'Interés': [interes],
                        'Estado': [estado_lead],
                        'Fecha_Contacto': [fecha_contacto.strftime('%Y-%m-%d')]
                    })
                    st.session_state.leads_b2b = pd.concat([st.session_state.leads_b2b, nuevo_lead], ignore_index=True)
                    st.success(f"✅ Lead de {empresa} agregado exitosamente!")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor completa todos los campos obligatorios")

# Footer
st.markdown("---")
st.markdown("**Querétaro FC** | Manager, Ticket Sales & Service | Sistema de Gestión de Ticketing")
st.caption("Octubre 2025")
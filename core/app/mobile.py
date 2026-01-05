import streamlit as st


def enforce_mobile_safety():
    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

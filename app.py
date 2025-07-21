from __future__ import annotations

import json
import requests
from collections import defaultdict
from urllib.parse import quote_plus

import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie

# ──────────────────────────────── LOGIC ────────────────────────────────
class FintechNavigator:
    def __init__(self) -> None:
        self.bank_urls = self._load_bank_urls()
        self.keyword_bank_map = self._load_keyword_bank_map()
        self.df_mappings = self._create_dataframe_mappings()
        self.keyword_to_banks = self._create_keyword_to_banks()

    @staticmethod
    def _load_bank_urls() -> dict[str, str]:
        return {
            "State Bank of India": "sbi.co.in",
            "Union Bank of India": "unionbankofindia.co.in",
            "Indian Overseas Bank": "iob.in",
            "Bank of Baroda": "bankofbaroda.in",
            "ICICI Bank": "icicibank.com",
            "Yes Bank": "yesbank.in",
            "HDFC Bank": "hdfcbank.com",
            "IndusInd Bank": "indusind.com",
            "Axis Bank": "axisbank.com",
            "Punjab National Bank": "pnbindia.in",
            "CANARA Bank": "canarabank.in",
            "INDIAN Bank": "indianbank.in",
            "IDFC Bank": "idfcfirstbank.com",
        }

    def _load_keyword_bank_map(self) -> list[str]:
        return [
            "Data Analytics + State bank of India", "Fintech + State bank of India",
            "Cloud banking + State bank of India", "Blockchain + State bank of India",
            "AI + State bank of India", "Digital India + State bank of India",
            "Facial KYC + State bank of India", "Bharat QR + State bank of India",
            "Robo Advisor + State bank of India", "Chatbots + State bank of India",
            "Al Based credit scoring + State bank of India", "E- Rupee + State bank of India",
            "Mobile banking app + State bank of India", "Digital first banks + State bank of India",
            "Net banking + State bank of India", "Cloud Platforms + State bank of India",
            "Internet + State bank of India", "4G/5G Banking + State bank of India",
            "UPI apps + State bank of India", "IMPS + State bank of India",
            "Mobile wallets + State bank of India", "Cloud Flash Online payment + State bank of India",
            "Payment Aggregators + State bank of India", "Google Pay/ Phone Pay + State bank of India",
            "Instant Loan app + State bank of India", "Supply chain Financing + State bank of India",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + State bank of India",
            "Digital lending platforms + State bank of India", "Financial Inclusion + State bank of India",
            "Online Insurance + State bank of India",
            "Data Analytics + Union Bank of India", "Fintech + Union bank of India",
            "Cloud banking + Union bank of India", "Blockchain + Union bank of India",
            "AI + Union bank of India", "Digital India + Union bank of India",
            "Facial KYC + Union bank of India", "Bharat QR + Union bank of India",
            "Robo Advisor + Union bank of India", "Chatbots + Union bank of India",
            "Al Based credit scoring + Union bank of India", "E- Rupee + Union bank of India",
            "Mobile banking app + Union bank of India", "Digital first banks + Union bank of India",
            "Net banking + Union bank of India", "Cloud Platforms + Union bank of India",
            "Internet + Union bank of India", "4G/5G Banking + Union bank of India",
            "UPI apps + Union bank of India", "IMPS + Union bank of India",
            "Mobile wallets + Union bank of India", "Cloud Flash Online payment + Union bank of India",
            "Payment Aggregators + Union bank of India", "Google Pay/ Phone Pay + Union bank of India",
            "Instant Loan app + Union bank of India", "Supply chain Financing + Union bank of India",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Union bank of India",
            "Digital lending platforms + Union bank of India", "Financial Inclusion + Union bank of India",
            "Online Insurance + Union bank of India",
            "Data Analytics + Indian Overseas Bank", "Fintech + Indian Overseas Bank",
            "Cloud banking Indian Overseas Bank", "Blockchain + Indian Overseas Bank",
            "AI + Indian Overseas Bank", "Digital India + Indian Overseas Bank",
            "Facial KYC + Indian Overseas Bank", "Bharat QR + Indian Overseas Bank",
            "Robo Advisor + Indian Overseas Bank", "Chatbots + Indian Overseas Bank",
            "Al Based credit scoring + Indian Overseas Bank", "E- Rupee + Indian Overseas Bank",
            "Mobile banking app + Indian Overseas Bank", "Digital first banks + Indian Overseas Bank",
            "Mobile banking app + Indian Overseas Bank", "Digital first banks + Indian Overseas Bank",
            "Net banking + Indian Overseas Bank", "Cloud Platforms + Indian Overseas Bank",
            "Internet + Indian Overseas Bank", "4G/5G Banking + Indian Overseas Bank",
            "UPI apps + Indian Overseas Bank", "IMPS + Indian Overseas Bank",
            "Mobile wallets + Indian Overseas Bank", "Cloud Flash Online payment + Indian Overseas Bank",
            "Payment Aggregators + Indian Overseas Bank", "Google Pay/ Phone Pay + Indian Overseas Bank",
            "Instant Loan app + Indian Overseas Bank", "Supply chain Financing + Indian Overseas Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Indian Overseas Bank",
            "Digital lending platforms + Indian Overseas Bank", "Financial Inclusion + Indian Overseas Bank",
            "Online Insurance + Indian Overseas Bank",
            "Data Analytics + Bank of Baroda", "Fintech + Bank of Baroda",
            "Cloud banking + Bank of Baroda", "Blockchain + Bank of Baroda",
            "AI + Bank of Baroda", "Digital India + Bank of Baroda",
            "Facial KYC + Bank of Baroda", "Bharat QR + Bank of Baroda", # Corrected line
            "Robo Advisor + Bank of Baroda", "Chatbots + Bank of Baroda",
            "Al Based credit scoring + Bank of Baroda", "E- Rupee + Bank of Baroda",
            "Mobile banking app + Bank of Baroda", "Digital first banks + Bank of Baroda",
            "Net banking + Bank of Baroda", "Cloud Platforms + Bank of Baroda",
            "Internet + Bank of Baroda", "4G/5G Banking + Bank of Baroda",
            "UPI apps + Bank of Baroda", "IMPS + Bank of Baroda",
            "Mobile wallets + Bank of Baroda", "Cloud Flash Online payment + Bank of Baroda",
            "Payment Aggregators + Bank of Baroda", "Google Pay/ Phone Pay + Bank of Baroda",
            "Instant Loan app + Bank of Baroda", "Supply chain Financing + Bank of Baroda",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Bank of Baroda",
            "Digital lending platforms + Bank of Baroda", "Financial Inclusion + Bank of Baroda",
            "Online Insurance + Bank of Baroda",
            "Data Analytics + ICICI Bank", "Fintech + ICICI Bank",
            "Cloud banking + ICICI Bank", "Blockchain + ICICI Bank",
            "AI + ICICI Bank", "Digital India + ICICI Bank",
            "Facial KYC + ICICI Bank", "Bharat QR + ICICI Bank",
            "Robo Advisor + ICICI Bank", "Chatbots + ICICI Bank",
            "Al Based credit scoring + ICICI Bank", "E- Rupee + ICICI Bank",
            "Mobile banking app + ICICI Bank", "Digital first banks + ICICI Bank",
            "Net banking + ICICI Bank", "Cloud Platforms + ICICI Bank",
            "Internet + ICICI Bank", "4G/5G Banking + ICICI Bank",
            "UPI apps + ICICI Bank", "IMPS + ICICI Bank",
            "Mobile wallets + ICICI Bank", "Cloud Flash Online payment + ICICI Bank",
            "Payment Aggregators + ICICI Bank", "Google Pay/ Phone Pay + ICICI Bank",
            "Instant Loan app + ICICI Bank", "Supply chain Financing + ICICI Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + ICICI Bank",
            "Digital lending platforms + ICICI Bank", "Financial Inclusion + ICICI Bank",
            "Online Insurance + ICICI Bank",
            "Data Analytics + Yes Bank", "Fintech + Yes Bank",
            "Cloud banking + Yes Bank", "Blockchain + Yes Bank",
            "AI + Yes Bank", "Digital India + Yes Bank",
            "Facial KYC + Yes Bank", "Bharat QR + Yes Bank",
            "Robo Advisor + Yes Bank", "Chatbots + Yes Bank",
            "Al Based credit scoring + Yes Bank", "E- Rupee + Yes Bank",
            "Mobile banking app + Yes Bank", "Digital first banks + Yes Bank",
            "Net banking + Yes Bank", "Cloud Platforms + Yes Bank",
            "Internet + Yes Bank", "4G/5G Banking + Yes Bank",
            "UPI apps + Yes Bank", "IMPS + Yes Bank",
            "Mobile wallets + Yes Bank", "Cloud Flash Online payment + Yes Bank",
            "Payment Aggregators + Yes Bank", "Google Pay/ Phone Pay + Yes Bank",
            "Instant Loan app + Yes Bank", "Supply chain Financing + Yes Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Yes Bank",
            "Digital lending platforms + Yes Bank", "Financial Inclusion + Yes Bank",
            "Online Insurance + Yes Bank",
            "Data Analytics + HDFC Bank", "Fintech + HDFC Bank",
            "Cloud banking + HDFC Bank", "Blockchain + HDFC Bank",
            "AI + HDFC Bank", "Digital India + HDFC Bank",
            "Facial KYC + HDFC Bank", "Bharat QR + HDFC Bank",
            "Robo Advisor + HDFC Bank", "Chatbots + HDFC Bank",
            "Al Based credit scoring + HDFC Bank", "E- Rupee + HDFC Bank",
            "Mobile banking app + HDFC Bank", "Digital first banks + HDFC Bank",
            "Net banking + HDFC Bank", "Cloud Platforms + HDFC Bank",
            "Internet + HDFC Bank", "4G/5G Banking + HDFC Bank",
            "UPI apps + HDFC Bank", "IMPS + HDFC Bank",
            "Mobile wallets + HDFC Bank", "Cloud Flash Online payment + HDFC Bank",
            "Payment Aggregators + HDFC Bank", "Google Pay/ Phone Pay + HDFC Bank",
            "Instant Loan app + HDFC Bank", "Supply chain Financing + HDFC Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + HDFC Bank",
            "Digital lending platforms + HDFC Bank", "Financial Inclusion + HDFC Bank",
            "Online Insurance + HDFC Bank",
            "Data Analytics + Induslnd Bank", "Fintech + Induslnd Bank",
            "Cloud banking + Induslnd Bank", "Blockchain + Induslnd Bank",
            "AI + Induslnd Bank", "Digital India + Induslnd Bank",
            "Facial KYC + Induslnd Bank", "Bharat QR + Induslnd Bank",
            "Robo Advisor + Induslnd Bank", "Chatbots + Induslnd Bank",
            "Al Based credit scoring + Induslnd Bank", "E- Rupee + Induslnd Bank",
            "Mobile banking app + Induslnd Bank", "Digital first banks + Induslnd Bank",
            "Net banking + Induslnd Bank", "Cloud Platforms + Induslnd Bank",
            "Internet + Induslnd Bank", "4G/5G Banking + Induslnd Bank",
            "UPI apps + Induslnd Bank", "IMPS + Induslnd Bank",
            "Mobile wallets + Induslnd Bank", "Cloud Flash Online payment + Induslnd Bank",
            "Payment Aggregators + Induslnd Bank", "Google Pay/ Phone Pay + Induslnd Bank",
            "Instant Loan app + Induslnd Bank", "Supply chain Financing + Induslnd Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Induslnd Bank",
            "Digital lending platforms + Induslnd Bank", "Financial Inclusion + Induslnd Bank",
            "Online Insurance + Induslnd Bank",
            "Data Analytics + Axis Bank", "Fintech + Axis Bank",
            "Cloud banking + Axis Bank", "Blockchain + Axis Bank",
            "AI + Axis Bank", "Digital India + Axis Bank",
            "Facial KYC + Axis Bank", "Bharat QR + Axis Bank",
            "Robo Advisor + Axis Bank", "Chatbots + Axis Bank",
            "Al Based credit scoring + Axis Bank", "E- Rupee + Axis Bank",
            "Mobile banking app + Axis Bank", "Digital first banks + Axis Bank",
            "Net banking + Axis Bank", "Cloud Platforms + Axis Bank",
            "Internet + Axis Bank", "4G/5G Banking + Axis Bank",
            "UPI apps + Axis Bank", "IMPS + Axis Bank",
            "Mobile wallets + Axis Bank", "Cloud Flash Online payment + Axis Bank",
            "Payment Aggregators + Axis Bank", "Google Pay/ Phone Pay + Axis Bank",
            "Instant Loan app + Axis Bank", "Supply chain Financing + Axis Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Axis Bank",
            "Digital lending platforms + Axis Bank", "Financial Inclusion + Axis Bank",
            "Online Insurance + Axis Bank",
            "Data Analytics + Punjab National Bank", "Fintech + Punjab National Bank",
            "Cloud banking + Punjab National Bank", "Blockchain + Punjab National Bank",
            "AI + Punjab National Bank", "Digital India + Punjab National Bank",
            "Facial KYC + Punjab National Bank", "Bharat QR + Punjab National Bank",
            "Robo Advisor + Punjab National Bank", "Chatbots + Punjab National Bank",
            "Al Based credit scoring + Punjab National Bank", "E- Rupee + Punjab National Bank",
            "Mobile banking app + Punjab National Bank", "Digital first banks + Punjab National Bank",
            "Net banking + Punjab National Bank", "Cloud Platforms + Punjab National Bank",
            "Internet + Punjab National Bank", "4G/5G Banking + Punjab National Bank",
            "UPI apps + Punjab National Bank", "IMPS + Punjab National Bank",
            "Mobile wallets + Punjab National Bank", "Cloud Flash Online payment + Punjab National Bank",
            "Payment Aggregators + Punjab National Bank", "Google Pay/ Phone Pay + Punjab National Bank",
            "Instant Loan app + Punjab National Bank", "Supply chain Financing + Punjab National Bank",
            "TReDS platforms (M1xchange, RXIL, Invoice mart) + Punjab National Bank",
            "Digital lending platforms + Punjab National Bank", "Financial Inclusion + Punjab National Bank",
            "Online Insurance + Punjab National Bank",
        ]

    @staticmethod
    def _normalize(text: str) -> str:
        return text.lower().strip()

    def _create_dataframe_mappings(self) -> pd.DataFrame:
        rows: list[dict[str, str]] = []
        for entry in self.keyword_bank_map:
            parts = entry.split(" + ")
            if len(parts) >= 2:
                keyword = " + ".join(parts[:-1]).strip()
                bank = parts[-1].strip()
                rows.append({"Keyword": self._normalize(keyword), "Bank": self._normalize(bank)})
        return pd.DataFrame(rows)

    def _create_keyword_to_banks(self) -> dict[str, list[str]]:
        rev: defaultdict[str, list[str]] = defaultdict(list)
        for _, r in self.df_mappings.iterrows():
            rev[r["Keyword"]].append(r["Bank"])
        return dict(rev)

    def get_banks_for_keyword(self, keyword: str) -> list[str]:
        return self.keyword_to_banks.get(self._normalize(keyword), [])

    def construct_search_url(self, keyword: str, bank: str) -> str | None:
        actual_bank = next((b for b in self.bank_urls if self._normalize(b) == bank), None)
        if not actual_bank:
            return None
        domain = self.bank_urls[actual_bank]
        q = quote_plus(f"{keyword} {actual_bank}")
        return f"https://www.google.com/search?q=site:{domain}+{q}"


# ──────────────────────────────── UI ────────────────────────────────
def load_lottie(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def main():
    st.set_page_config(page_title="Fintech Index Navigator", page_icon="💸", layout="centered")

    # Instantiate FintechNavigator early in main()
    if "nav" not in st.session_state:
     st.session_state["nav"] = FintechNavigator()
    fintech_nav = st.session_state["nav"] 

    st.markdown(
        """
        <style>
        .gradient-header {
            background: linear-gradient(to right, #667eea, #764ba2);
            padding: 2rem;
            border-radius: 1rem;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            animation: fadeInDown 0.6s ease-out;
        }
        @keyframes fadeInDown {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .stButton>button {
            background: #6c5ce7;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: #5a4fcf;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 0.75rem;
            padding: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-align: center;
            background: #fff;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        a {
        color: white;
        text-decoration: none;
        }
        a:hover {
        text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="gradient-header"><h1>Fintech Navigator</h1><p>Type a fintech keyword to discover related banks</p></div>', unsafe_allow_html=True)

    lottie_json = load_lottie("https://assets7.lottiefiles.com/packages/lf20_zrqthn6o.json")
    if lottie_json:
        st_lottie(lottie_json, height=180, key="search_anim")

    fintech_nav = st.session_state.get("navigator") or FintechNavigator()
    st.session_state["navigator"] = fintech_nav

    keyword = st.text_input("🔍 Enter Fintech Keyword", placeholder="e.g., AI, UPI apps, Blockchain")
    if st.button("Search") and keyword:
        banks = fintech_nav.get_banks_for_keyword(keyword)
        if banks:
            st.success(f"{len(banks)} bank(s) found for '{keyword.title()}'")
            cols = st.columns(3)
            for idx, bank in enumerate(banks):
                url = fintech_nav.construct_search_url(keyword, bank)
                with cols[idx % 3]:
                    st.markdown(
                       f"""
                        <div class="bank-card">
                        <h4 style="margin-bottom: 0.5rem;">{bank.title()}</h4>
                        <a href="{url}" target="_blank" style="
                        display: inline-block;
                        padding: 0.5rem 1rem;
                        margin-top: 0.5rem;
                        background-color: #2563eb;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: 600;
                        transition: background 0.2s ease;">
                        Explore ↗
                        </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
        

    )

if __name__ == "__main__":
    main()

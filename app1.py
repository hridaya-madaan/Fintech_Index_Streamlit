import streamlit as st
import pandas as pd
import time
import random
import re
from urllib.parse import quote_plus

class FintechNavigator:
    """
    A sophisticated navigator for fintech-related information across various Indian banks.

    This class provides a robust mechanism to map user-provided keywords to
    specific bank websites and initiate targeted searches within those domains.
    It leverages a predefined index of fintech topics and banks, offering a
    more focused and efficient way to access relevant information than
    general web searches.
    """

    def __init__(self):
        """
        Initializes the FintechNavigator with bank URLs and the keyword-bank mapping.
        """
        self.bank_urls = self._load_bank_urls()
        self.keyword_bank_map = self._load_keyword_bank_map()
        self.df_mappings = self._create_dataframe_mappings()
        self.bank_specific_keywords = self.get_bank_specific_keywords()
        print("FintechNavigator initialized. Ready to assist your research.")

    def _load_bank_urls(self) -> dict:
        """
        Loads the base URLs (domains) for the supported banks.
        These domains are used for site-specific Google searches or direct redirection.

        Returns:
            dict: A dictionary mapping bank names to their base domain URLs.
        """
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
            "IDFC Bank": "idfcfirstbank.com"
        }

    def _load_keyword_bank_map(self) -> list:
        """
        Loads the raw keyword-bank mappings provided in the initial comprehensive list.

        Returns:
            list: A list of strings, each representing a keyword + bank mapping.
        """
        # The extensive list provided by the user in the initial prompt
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
            "Online Insurance + Punjab National Bank"
        ]

    def _create_dataframe_mappings(self) -> pd.DataFrame:
        """
        Processes the raw keyword-bank mappings into a Pandas DataFrame for efficient lookup.

        The DataFrame will have columns for 'Full Phrase', 'Keyword', and 'Bank'.

        Returns:
            pd.DataFrame: A DataFrame containing the parsed mappings.
        """
        data = []
        for entry in self.keyword_bank_map:
            parts = entry.split(' + ')
            if len(parts) == 2:
                keyword = parts[0].strip()
                bank = parts[1].strip()
                data.append({'Full Phrase': entry.lower(), 'Keyword': keyword.lower(), 'Bank': bank.lower()})
            elif len(parts) > 2: # Handle cases like "TReDS platforms (M1xchange, RXIL, Invoice mart) + State bank of India"
                bank = parts[-1].strip()
                keyword = ' + '.join(parts[:-1]).strip()
                data.append({'Full Phrase': entry.lower(), 'Keyword': keyword.lower(), 'Bank': bank.lower()})
            else:
                print(f"Warning: Could not parse entry '{entry}'. Skipping.")
        return pd.DataFrame(data)

    def _normalize_input(self, user_input: str) -> str:
        """
        Normalizes user input for consistent matching.

        Args:
            user_input (str): The raw input string from the user.

        Returns:
            str: The normalized (lowercase, stripped) input string.
        """
        return user_input.lower().strip()

    def find_bank_only_match(self, user_query: str) -> str | None:
        """
        Checks if the user query is primarily a bank name.

        Args:
            user_query (str): The normalized query string from the user.

        Returns:
            str | None: The normalized bank name if found, otherwise None.
        """
        user_query_normalized = self._normalize_input(user_query)
        for bank_name_key in self.bank_urls.keys():
            if user_query_normalized == self._normalize_input(bank_name_key):
                return self._normalize_input(bank_name_key)
        return None

    def find_best_match(self, user_query: str) -> tuple[str | None, str | None]:
        """
        Attempts to find the best matching keyword and bank from the predefined index.

        It prioritizes exact matches of the full phrase, then tries to find a bank
        and a keyword within the query.

        Args:
            user_query (str): The normalized query string provided by the user.

        Returns:
            tuple[str | None, str | None]: A tuple containing the identified keyword
                                           and bank name (both normalized), or (None, None) if no match.
        """
        user_query_normalized = self._normalize_input(user_query)

        # 1. Try to find an exact match for the full phrase (e.g., "Fintech + State bank of India")
        exact_match = self.df_mappings[self.df_mappings['Full Phrase'] == user_query_normalized]
        if not exact_match.empty:
            keyword = exact_match['Keyword'].iloc[0]
            bank = exact_match['Bank'].iloc[0]
            print(f"Exact full phrase match found: Keyword='{keyword}', Bank='{bank}'")
            return keyword, bank

        # 2. Try to find a bank and then a keyword within the query (e.g., "AI for HDFC Bank")
        found_bank = None
        for bank_name_key, _ in self.bank_urls.items():
            if self._normalize_input(bank_name_key) in user_query_normalized:
                found_bank = self._normalize_input(bank_name_key)
                break

        if found_bank:
            bank_specific_mappings = self.df_mappings[self.df_mappings['Bank'] == found_bank]
            
            best_keyword_match = None
            max_keyword_len = 0
            for _, row in bank_specific_mappings.iterrows():
                keyword_in_map = row['Keyword']
                if keyword_in_map in user_query_normalized:
                    if len(keyword_in_map) > max_keyword_len:
                        best_keyword_match = keyword_in_map
                        max_keyword_len = len(keyword_in_map)
            
            if best_keyword_match:
                print(f"Inferred keyword/bank match: Keyword='{best_keyword_match}', Bank='{found_bank}'")
                return best_keyword_match, found_bank

        print(f"No direct or inferred keyword/bank match found for query: '{user_query}'")
        return None, None

    def construct_search_url(self, keyword: str, bank_name: str) -> str | None:
        """
        Constructs a Google search URL to perform a site-specific search.

        Args:
            keyword (str): The keyword to search for.
            bank_name (str): The name of the bank.

        Returns:
            str | None: The constructed Google search URL, or None if the bank URL is not found.
        """
        # Find the actual bank name from self.bank_urls keys to get the correct domain
        actual_bank_name = None
        for key in self.bank_urls:
            if self._normalize_input(key) == self._normalize_input(bank_name):
                actual_bank_name = key
                break

        bank_url_domain = self.bank_urls.get(actual_bank_name)
        if not bank_url_domain:
            print(f"Error: Could not find domain for bank '{bank_name}'.")
            return None

        # Sanitize keyword for URL
        search_query_encoded = quote_plus(f"{keyword} {actual_bank_name}")
        
        # Construct the Google site-specific search URL
        google_search_url = f"https://www.google.com/search?q=site:{bank_url_domain}+{search_query_encoded}"
        return google_search_url

    def get_bank_specific_keywords(self) -> dict[str, list[str]]:
        """
        Generates a dictionary mapping each bank to a list of its associated unique keywords.

        This method processes the comprehensive df_mappings DataFrame to provide
        a bank-centric view of the keywords.

        Returns:
            dict: A dictionary where keys are bank names (normalized) and values are
                  lists of unique keywords (normalized) associated with that bank.
        """
        bank_to_keywords = {}
        for _, row in self.df_mappings.iterrows():
            bank = row['Bank']
            keyword = row['Keyword']
            if bank not in bank_to_keywords:
                bank_to_keywords[bank] = []
            if keyword not in bank_to_keywords[bank]: # Ensure unique keywords per bank
                bank_to_keywords[bank].append(keyword)
        return bank_to_keywords

# Initialize the FintechNavigator globally for the Streamlit app
fintech_navigator = FintechNavigator()

def main():
    st.set_page_config(layout="centered", page_title="Fintech Index Navigator")

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f5;
            font-family: 'Inter', sans-serif;
        }
        .container {
            max-width: 800px;
            margin: auto;
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4c51bf;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            transition: background-color 0.3s ease;
            width: 100%; /* Make button full width */
        }
        .stButton>button:hover {
            background-color: #3e4396;
        }
        .stTextInput>div>div>input {
            border: 1px solid #d1d5db;
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            width: 100%;
        }
        .message-box {
            background-color: #fee2e2;
            color: #ef4444;
            border: 1px solid #ef4444;
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
        }
        .bank-keywords-section {
            margin-top: 2.5rem;
            padding-top: 2.5rem;
            border-top: 1px solid #e5e7eb;
        }
        .keyword-tag {
            display: inline-block;
            background-color: #e0e7ff;
            color: #4338ca;
            padding: 0.25rem 0.75rem;
            border-radius: 0.75rem;
            font-size: 0.875rem;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1 class="text-4xl font-bold text-center text-gray-800 mb-6">Fintech Index Navigator</h1>', unsafe_allow_html=True)
    st.markdown("""
        <p class="text-lg text-center text-gray-600 mb-8">
            Enter a fintech topic and a bank name (e.g., <span class="font-semibold text-indigo-700">'AI + HDFC Bank'</span>)
            or just a bank name (e.font-semibold text-indigo-700.g., <span class="font-semibold text-indigo-700">'State Bank of India'</span>).
            We'll redirect you to the bank's official website or a targeted search.
        </p>
        """, unsafe_allow_html=True)

    # Display messages
    if 'message' in st.session_state and st.session_state.message:
        st.markdown(f'<div class="message-box">{st.session_state.message}</div>', unsafe_allow_html=True)
        st.session_state.message = "" # Clear message after display

    user_query = st.text_input(
        "Your Query:",
        placeholder="e.g., State Bank of India or Fintech + ICICI Bank",
        key="query_input"
    )

    if st.button("Navigate"):
        if not user_query:
            st.session_state.message = "Please enter a query."
            st.experimental_rerun()
            return

        user_query_normalized = fintech_navigator._normalize_input(user_query)

        # First, check if the query is *only* a bank name
        bank_only_match = fintech_navigator.find_bank_only_match(user_query)
        if bank_only_match:
            actual_bank_name = None
            for key in fintech_navigator.bank_urls:
                if fintech_navigator._normalize_input(key) == bank_only_match:
                    actual_bank_name = key
                    break
            
            if actual_bank_name:
                direct_bank_url = f"https://www.{fintech_navigator.bank_urls[actual_bank_name]}"
                st.markdown(f"Redirecting directly to bank website: [{actual_bank_name}]({direct_bank_url})", unsafe_allow_html=True)
                # Streamlit doesn't directly redirect the browser like Flask.
                # Instead, we provide a clickable link.
                st.markdown(f'<meta http-equiv="refresh" content="0; url={direct_bank_url}">', unsafe_allow_html=True)
                # webbrowser.open_new_tab(direct_bank_url) # This would open a new tab on the server side, not ideal for web app
            else:
                st.session_state.message = f"Could not find a direct URL for '{user_query}'. Please check the bank name."
                st.experimental_rerun()
            return

        # If not a bank-only query, proceed with keyword + bank search
        keyword, bank = fintech_navigator.find_best_match(user_query)

        if keyword and bank:
            search_url = fintech_navigator.construct_search_url(keyword, bank)
            if search_url:
                st.markdown(f"Redirecting to targeted search: [{keyword.title()} on {bank.title()}]({search_url})", unsafe_allow_html=True)
                st.markdown(f'<meta http-equiv="refresh" content="0; url={search_url}">', unsafe_allow_html=True)
                # webbrowser.open_new_tab(search_url) # This would open a new tab on the server side, not ideal for web app
            else:
                st.session_state.message = "Could not construct a valid search URL. Please check the bank name and keyword."
                st.experimental_rerun()
        else:
            st.session_state.message = "No matching fintech topic and bank found in the index for your query. Please try again."
            st.experimental_rerun()

    st.markdown('<div class="bank-keywords-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Keywords by Bank</h2>', unsafe_allow_html=True)
    
    bank_keywords_display = {
        bank.title(): [kw.title() for kw in keywords]
        for bank, keywords in fintech_navigator.bank_specific_keywords.items()
    }

    for bank, keywords in bank_keywords_display.items():
        st.markdown(f'<span class="bank-name">{bank}:</span>', unsafe_allow_html=True)
        keyword_html = '<div class="flex flex-wrap mt-2">'
        for keyword in keywords:
            keyword_html += f'<span class="keyword-tag">{keyword}</span>'
        keyword_html += '</div>'
        st.markdown(keyword_html, unsafe_allow_html=True)
        st.markdown("---") # Separator for readability

    st.markdown("""
        <div class="mt-10 text-center text-gray-500 text-sm">
            <p>&copy; 2025 Fintech Navigator. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Close container div

if __name__ == "__main__":
    main()

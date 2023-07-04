import streamlit as st
import datetime
import requests
import time

st.set_page_config(page_title='Nebulous CC Validator', page_icon='cc.png', layout="centered", initial_sidebar_state="auto", menu_items=None)



def validate_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")

    if not card_number.isnumeric():
        return False

    digits = list(map(int, card_number))
    checksum = sum(digits[-2::-2] + [sum(divmod(2 * d, 10)) for d in digits[-1::-2]])

    return checksum % 10 == 0

def check_credit_card_validity(card_number, month, year, cvv):
    if validate_credit_card(card_number):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        b = datetime.datetime.strptime(month, "%B").month
        c = int(year)

        if c < current_year or (c == current_year and b < current_month):
            return "The Credit Card has EXPIRED!"
        else:
            return "Credit Card is VALID!"
    else:
        return "Credit Card is Invalid!"

def check_credit_cards(card_infos):
    valid_results = []
    invalid_results = []
    for card_info in card_infos:
        card_parts = card_info.split("|")
        if len(card_parts) == 4:
            card_number = card_parts[0]
            exp_month = card_parts[1]
            exp_year = card_parts[2]
            cvv = card_parts[3]
            if validate_credit_card(card_number):
                valid_results.append(f"{card_info}")
            else:
                invalid_results.append(f"{card_info}")
        else:
            invalid_results.append(f"Invalid Card Information Format: {card_info}")
    return valid_results, invalid_results

def page_home():
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 14px;'>Enter Credit Card Information to Check its Validity(GATE-1)</h1></center>",
        unsafe_allow_html=True)

    def main():
        card_number = st.text_input("Credit Card Number")

        col1, col2, col3 = st.columns(3)

        with col1:
            month = st.selectbox('Month', ['Select One', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        with col2:
            year = st.selectbox('Year', ['Select One', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032'])

        with col3:
            if card_number.startswith('3'):
                cvv = st.text_input("CVV (4 digits)")
            else:
                cvv = st.text_input("CVV (3 digits)")

        if st.button("Check"):
            if month == 'Select One' or year == 'Select One':
                st.warning("Please select a valid month and year.")
            elif not cvv or (card_number.startswith('3') and len(cvv) != 4) or (not card_number.startswith('3') and len(cvv) != 3):
                st.warning("Invalid CVV!")
            else:
                # Display loading spinner
                with st.spinner("Checking..."):
                    time.sleep(2)
                    result = check_credit_card_validity(card_number, month, year, cvv)
                    if "VALID" in result:
                        st.success(result)
                    elif "EXPIRED" in result:
                        st.warning(result)
                    else:
                        st.error(result)

    main()

def page_about():
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 14px;'>Enter Credit Card Information to Check its Validity(GATE-2)</h1></center>",
        unsafe_allow_html=True)

    def luhn_checksum(card_number):
        digits = [int(x) for x in str(card_number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for digit in even_digits:
            total += sum(divmod(digit * 2, 10))
        return total % 10

    def is_luhn_valid(card_number):
        return luhn_checksum(card_number) == 0

    def check_credit_cards(card_infos):
        valid_results = []
        invalid_results = []
        for card_info in card_infos:
            card_parts = card_info.split("|")
            if len(card_parts) == 4:
                card_number = card_parts[0]
                exp_month = card_parts[1]
                exp_year = card_parts[2]
                cvv = card_parts[3]
                card_number = card_number.replace(" ", "")
                if card_number.isdigit() and is_luhn_valid(card_number):
                    valid_results.append(f"{card_info}")
                else:
                    invalid_results.append(f"{card_info}")
            else:
                invalid_results.append(f"Invalid Card Information Format: {card_info}")
        return valid_results, invalid_results

    card_infos = st.text_area("Credit Card Information", height=200)
    card_infos = card_infos.split("\n")
    card_infos = [card.strip() for card in card_infos if card.strip() != ""]

    if st.button("Check"):
        if len(card_infos) > 0:
            with st.spinner("Checking credit card information..."):
                time.sleep(3)
                valid_results, invalid_results = check_credit_cards(card_infos)

            st.markdown(
                "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Valid Credit Cards</h1></center>",
                unsafe_allow_html=True)
            valid_output = "\n".join(valid_results)
            st.text_area("Valid Credit Card Details", value=valid_output, height=200)

            st.markdown(
                "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Invalid Credit Cards</h1></center>",
                unsafe_allow_html=True)
            invalid_output = "\n".join(invalid_results)
            st.text_area("Invalid Credit Card Details", value=invalid_output, height=200)

            num_valid = len(valid_results)
            num_invalid = len(invalid_results)

            st.success(f"Number of Valid Credit Cards: {num_valid}")
            st.error(f"Number of Invalid Credit Cards: {num_invalid}")
        else:
            st.write("No credit card information entered.")


def page_contact():
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 14px;'>Enter Credit Card Information to Check its Validity(GATE-3)</h1></center>",
        unsafe_allow_html=True)

    card_infos = st.text_area("Credit Card Information", height=200, key="contact_card_infos")

    if st.button("Check"):
        if len(card_infos) > 0:
            with st.spinner("Processing..."):
                time.sleep(3)

                valid_results, invalid_results = check_credit_cards(card_infos.split("\n"))

                st.markdown(
                    "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Valid Credit Cards</h1></center>",
                    unsafe_allow_html=True)
                valid_output = "\n".join(valid_results)
                st.text_area("Valid Credit Card Details", value=valid_output, height=200)

                st.markdown(
                    "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Invalid Credit Cards</h1></center>",
                    unsafe_allow_html=True)
                invalid_output = "\n".join(invalid_results)
                st.text_area("Invalid Credit Card Details", value=invalid_output, height=200)

                num_valid = len(valid_results)
                num_invalid = len(invalid_results)

                st.success(f"Number of Valid Credit Cards: {num_valid}")
                st.error(f"Number of Invalid Credit Cards: {num_invalid}")
        else:
            st.write("No credit card information entered.")



def bin():
    API_ENDPOINT = "https://api.apilayer.com/bincheck/"
    API_KEY = "5W24uhlSqks0B6E2OnGUl4q5OI6Fxnod"

    def verify_bin(bin_number):
        headers = {
            "apikey": API_KEY
        }
        response = requests.get(API_ENDPOINT + bin_number, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>BIN Checker</h1></center>",
            unsafe_allow_html=True)
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 18px;'>Enter a BIN (Bank "
            "Identification Number) to verify it</h1></center>",
            unsafe_allow_html=True)

        bin_number = st.text_input("BIN Number")

        if st.button("Verify"):
            if bin_number:
                with st.spinner("Please wait..."):
                    time.sleep(2)
                    bin_info = verify_bin(bin_number)
                if bin_info:
                    st.success("Verification Result")
                    st.write(f"Bank: **{bin_info['bank_name']}**")
                    st.write(f"BIN: **{bin_info['bin']}**")
                    st.write(f"Country: **{bin_info['country']}**")
                    st.write(f"Scheme: **{bin_info['scheme']}**")
                    st.write(f"Type: **{bin_info['type']}**")
                    if bin_info['url']:
                        st.write(f"URL: **{bin_info['url']}**")
                    else:
                        st.write("URL: **Bank URL not found**")
                else:
                    st.warning("BIN verification failed.")
            else:
                st.warning("Please enter a BIN number.")

    if __name__ == "__main__":
        main()


def main():
    st.sidebar.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Validator</h1></center>",
        unsafe_allow_html=True)
    st.sidebar.image("https://media.istockphoto.com/id/531236924/photo/group-of-credit-cards-on-computer-keyboard.jpg?s=612x612&w=0&k=20&c=5iAuEH7ipVgVDI9TkgzTC8Xx0roMhvDlT79UzRiSzcE=", use_column_width=True)
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 600; font-size: 32px;'>Nebulous Credit Card Validator</h1></center>",
        unsafe_allow_html=True)
    pages = ["Gate-1", "Gate-2", "Gate-3","Bin Checker"]
    selected_page = st.sidebar.radio("Please Select One", pages)

    if selected_page == "Gate-1":
        page_home()
    elif selected_page == "Gate-2":
        page_about()
    elif selected_page == "Gate-3":
        page_contact()
    elif selected_page == "Bin Checker":
        bin()

if __name__ == '__main__':
    main()

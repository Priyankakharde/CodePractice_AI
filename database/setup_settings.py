import os
import hashlib
import secrets

import streamlit as st
import psycopg2
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Settings | CodePractice AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


# ============================================================
# CURRENT USER
# ============================================================

# The Login page will set this when a user logs in:
#
# st.session_state["user_id"] = logged_in_user_id
#
# For now, if Login has not been connected yet,
# user ID 1 is used.

if "user_id" not in st.session_state:
    st.session_state["user_id"] = 1

USER_ID = st.session_state["user_id"]


# ============================================================
# CREATE PASSWORD COLUMN IF NEEDED
# ============================================================

def ensure_password_column():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN IF NOT EXISTS password_hash TEXT;
            """
        )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        st.error(
            f"Could not prepare database: {error}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


ensure_password_column()


# ============================================================
# PASSWORD HASH
# ============================================================

def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


# ============================================================
# GET USER
# ============================================================

def get_user():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                created_at
            FROM users
            WHERE id = %s
            LIMIT 1;
            """,
            (USER_ID,),
        )

        return cursor.fetchone()

    except Exception as error:

        st.error(
            f"Could not load profile: {error}"
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# UPDATE USER
# ============================================================

def update_user(
    first_name,
    surname,
    email,
    new_password=None,
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        full_name = (
            f"{first_name.strip()} "
            f"{surname.strip()}"
        ).strip()

        # ----------------------------------------------------
        # UPDATE WITH PASSWORD
        # ----------------------------------------------------

        if new_password:

            password_hash = hash_password(
                new_password
            )

            cursor.execute(
                """
                UPDATE users
                SET
                    name = %s,
                    email = %s,
                    password_hash = %s
                WHERE id = %s;
                """,
                (
                    full_name,
                    email.strip(),
                    password_hash,
                    USER_ID,
                ),
            )

        # ----------------------------------------------------
        # UPDATE WITHOUT PASSWORD
        # ----------------------------------------------------

        else:

            cursor.execute(
                """
                UPDATE users
                SET
                    name = %s,
                    email = %s
                WHERE id = %s;
                """,
                (
                    full_name,
                    email.strip(),
                    USER_ID,
                ),
            )

        connection.commit()

        return True

    except psycopg2.errors.UniqueViolation:

        if connection:
            connection.rollback()

        st.error(
            "This email / Login ID is already being used."
        )

        return False

    except Exception as error:

        if connection:
            connection.rollback()

        st.error(
            f"Could not update profile: {error}"
        )

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# DELETE USER
# ============================================================

def delete_user():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s;
            """,
            (USER_ID,),
        )

        deleted_rows = cursor.rowcount

        connection.commit()

        return deleted_rows > 0

    except Exception as error:

        if connection:
            connection.rollback()

        st.error(
            f"Could not delete account: {error}"
        )

        return False

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN
       ====================================================== */

    .stApp {
        background: #050b14;
        color: #e8f1ff;
    }

    [data-testid="stAppViewContainer"] {
        background: #050b14;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1400px;
        padding: 30px 40px 50px;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #071426 0%,
            #07111e 100%
        );

        border-right: 1px solid #132840;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 20px 18px;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 40px;
        border: 1px solid transparent;
        border-radius: 8px;
        background: transparent;
        color: #aabbd0;
        text-align: left;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 12px;
        margin: 3px 0;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #0d2138;
        border-color: #17385c;
        color: #ffffff;
    }

    .sidebar-brand {
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .sidebar-tagline {
        color: #6e87a5;
        font-size: 12px;
        margin-bottom: 28px;
    }

    .sidebar-divider {
        height: 1px;
        background: #1f334a;
        margin: 20px 0;
    }

    .sidebar-settings-active {
        color: #60a5fa;
        font-size: 14px;
        font-weight: 700;
        padding: 8px 10px;
    }


    /* ======================================================
       PAGE HEADER
       ====================================================== */

    .settings-title {
        color: #f8fafc;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .settings-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 30px;
    }


    /* ======================================================
       PROFILE WINDOW
       ====================================================== */

    .profile-card {
        background: #111827;
        border: 1px solid #243244;
        border-radius: 14px;
        padding: 26px;
        margin-bottom: 28px;
    }

    .profile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #243244;
        padding-bottom: 20px;
        margin-bottom: 25px;
    }

    .profile-name {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 700;
    }

    .profile-description {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    .close-symbol {
        color: #64748b;
        font-size: 22px;
    }


    /* ======================================================
       PROFILE PICTURE
       ====================================================== */

    .profile-picture {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(
            145deg,
            #273b59,
            #101a2a
        );
        border: 2px solid #344b6e;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        color: #8da5c9;
        margin-bottom: 12px;
    }

    .picture-description {
        color: #7188a8;
        font-size: 13px;
        margin-bottom: 10px;
    }


    /* ======================================================
       INFORMATION
       ====================================================== */

    .info-box {
        background: #0b1422;
        border: 1px solid #243754;
        border-radius: 8px;
        padding: 16px 18px;
        min-height: 72px;
        margin-bottom: 15px;
    }

    .info-label {
        color: #64748b;
        font-size: 12px;
        margin-bottom: 7px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .info-value {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 600;
        word-break: break-word;
    }

    .password-value {
        color: #dce5f4;
        font-size: 17px;
        letter-spacing: 3px;
        font-weight: 600;
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    [data-testid="stTextInput"] label {
        color: #cbd5e1 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    [data-testid="stTextInput"] input {
        background: #0b1422 !important;
        color: #f8fafc !important;
        border: 1px solid #243b55 !important;
        border-radius: 8px !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #318dff !important;
        box-shadow: 0 0 0 1px #318dff !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    div.stButton > button {
        border-radius: 8px;
        min-height: 42px;
        font-weight: 700;
    }

    button[kind="primary"] {
        background: #2b83f6 !important;
        border: 1px solid #4092ff !important;
        color: white !important;
    }


    /* ======================================================
       DANGER ZONE
       ====================================================== */

    .danger-card {
        background: #171014;
        border: 1px solid #54232b;
        border-radius: 14px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .danger-title {
        color: #ff6b72;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .danger-text {
        color: #a78b91;
        font-size: 13px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            &lt;/&gt; CodePractice
        </div>

        <div class="sidebar-tagline">
            Learn. Practice. Grow.
        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "←  Dashboard",
        key="settings_dashboard",
        use_container_width=True,
    ):

        if "dashboard_page" in st.session_state:

            st.switch_page(
                st.session_state["dashboard_page"]
            )

        else:

            st.switch_page("app.py")


    st.markdown(
        """
        <div class="sidebar-divider"></div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="sidebar-settings-active">
            ⚙️ Settings
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD USER
# ============================================================

user = get_user()

if not user:

    st.error(
        "User profile could not be loaded from PostgreSQL."
    )

    st.stop()


# ============================================================
# USER DATA
# ============================================================

user_id = user[0]
full_name = user[1] or ""
email = user[2] or ""
password_hash = user[3]
created_at = user[4]


# ============================================================
# SPLIT NAME
# ============================================================

name_parts = full_name.strip().split()

if len(name_parts) == 0:

    first_name = ""
    surname = ""

elif len(name_parts) == 1:

    first_name = name_parts[0]
    surname = ""

else:

    first_name = name_parts[0]
    surname = " ".join(name_parts[1:])


# ============================================================
# SESSION STATE
# ============================================================

if "edit_profile" not in st.session_state:

    st.session_state["edit_profile"] = False


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="settings-title">
        ⚙️ Settings
    </div>

    <div class="settings-subtitle">
        Manage your CodePractice AI profile.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PROFILE CARD
# ============================================================

st.markdown(
    '<div class="profile-card">',
    unsafe_allow_html=True,
)


# ============================================================
# PROFILE HEADER
# ============================================================

st.markdown(
    f"""
    <div class="profile-header">

        <div>

            <div class="profile-name">
                {full_name}
            </div>

            <div class="profile-description">
                CodePractice AI Account
            </div>

        </div>

        <div class="close-symbol">
            ×
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PROFILE PICTURE
# ============================================================

picture_col, picture_info_col = st.columns(
    [1, 5]
)


with picture_col:

    st.markdown(
        """
        <div class="profile-picture">
            👤
        </div>
        """,
        unsafe_allow_html=True,
    )


with picture_info_col:

    st.markdown(
        """
        <div style="
            color:#f8fafc;
            font-size:15px;
            font-weight:600;
            margin-top:10px;
        ">
            Profile Picture
        </div>

        <div class="picture-description">
            Your CodePractice AI profile picture
        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "CHANGE PICTURE",
        key="change_picture",
    ):

        st.info(
            "Profile picture upload will be added later."
        )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# EDIT MODE
# ============================================================

if st.session_state["edit_profile"]:

    st.markdown(
        """
        <div style="
            color:#ffffff;
            font-size:21px;
            font-weight:700;
            margin-bottom:18px;
        ">
            Edit Profile
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # FIRST NAME + SURNAME
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        edit_first_name = st.text_input(
            "First Name",
            value=first_name,
            key="edit_first_name",
        )


    with col2:

        edit_surname = st.text_input(
            "Surname",
            value=surname,
            key="edit_surname",
        )


    # --------------------------------------------------------
    # EMAIL + USER ID
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        edit_email = st.text_input(
            "Email / Login ID",
            value=email,
            key="edit_email",
        )


    with col2:

        st.text_input(
            "User ID",
            value=str(user_id),
            disabled=True,
            key="edit_user_id",
        )


    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    new_password = st.text_input(
        "New Password",
        type="password",
        placeholder="Leave blank to keep current password",
        key="edit_password",
    )


    st.caption(
        "Your current password is never displayed."
    )


    # --------------------------------------------------------
    # SAVE / CANCEL
    # --------------------------------------------------------

    save_col, cancel_col = st.columns(2)


    with save_col:

        if st.button(
            "💾 SAVE PROFILE",
            type="primary",
            use_container_width=True,
            key="save_profile",
        ):

            if not edit_first_name.strip():

                st.error(
                    "First Name cannot be empty."
                )

            elif not edit_email.strip():

                st.error(
                    "Email / Login ID cannot be empty."
                )

            else:

                success = update_user(
                    first_name=edit_first_name,
                    surname=edit_surname,
                    email=edit_email,
                    new_password=(
                        new_password
                        if new_password
                        else None
                    ),
                )


                if success:

                    # Keep login session updated.
                    st.session_state[
                        "user_email"
                    ] = edit_email.strip()


                    st.session_state[
                        "edit_profile"
                    ] = False


                    st.success(
                        "Profile updated successfully!"
                    )


                    st.rerun()


    with cancel_col:

        if st.button(
            "CANCEL",
            use_container_width=True,
            key="cancel_profile",
        ):

            st.session_state[
                "edit_profile"
            ] = False

            st.rerun()


# ============================================================
# VIEW MODE
# ============================================================

else:

    # --------------------------------------------------------
    # FIRST NAME + SURNAME
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    First Name
                </div>

                <div class="info-value">
                    {first_name}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    Surname
                </div>

                <div class="info-value">
                    {surname if surname else "-"}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # EMAIL + LOGIN ID
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    Email / Login ID
                </div>

                <div class="info-value">
                    {email}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    User ID
                </div>

                <div class="info-value">
                    {user_id}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # PASSWORD + ACCOUNT CREATED
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    Password
                </div>

                <div class="password-value">
                    ••••••••••
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        if created_at:

            created_text = created_at.strftime(
                "%d %B %Y"
            )

        else:

            created_text = "Not available"


        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    Account Created
                </div>

                <div class="info-value">
                    {created_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # EDIT PROFILE BUTTON
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)


    if st.button(
        "✏️ EDIT PROFILE",
        key="edit_profile_button",
    ):

        st.session_state[
            "edit_profile"
        ] = True

        st.rerun()


# ============================================================
# CLOSE PROFILE CARD
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# ACCOUNT SECTION
# ============================================================

st.markdown(
    """
    <div style="
        color:#f8fafc;
        font-size:21px;
        font-weight:700;
        margin-top:25px;
        margin-bottom:5px;
    ">
        🗑️ Account
    </div>

    <div style="
        color:#64748b;
        font-size:13px;
        margin-bottom:15px;
    ">
        Permanently manage your CodePractice AI account.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DELETE ACCOUNT
# ============================================================

st.markdown(
    """
    <div class="danger-card">

        <div class="danger-title">
            Delete Account
        </div>

        <div class="danger-text">
            This will permanently delete your CodePractice AI
            account and connected learning data.
            This action cannot be undone.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


confirm_delete = st.checkbox(
    "I understand that this action cannot be undone.",
    key="confirm_delete_account",
)


if st.button(
    "🗑️ DELETE ACCOUNT",
    key="delete_account",
):

    if not confirm_delete:

        st.warning(
            "Please confirm before deleting your account."
        )

    else:

        deleted = delete_user()

        if deleted:

            st.session_state.clear()

            st.success(
                "Account deleted successfully."
            )

            st.info(
                "Please return to the Login page."
            )

            st.stop()

        else:

            st.error(
                "Account could not be deleted."
            )
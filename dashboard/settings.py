import os
import hashlib
import secrets
import html

import psycopg2
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Profile | CodePractice AI",
    page_icon="👤",
    layout="wide",
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
# SESSION STATE
# ============================================================

if "selected_user_id" not in st.session_state:
    st.session_state["selected_user_id"] = None

if "edit_user_id" not in st.session_state:
    st.session_state["edit_user_id"] = None

if "show_create" not in st.session_state:
    st.session_state["show_create"] = False


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.sha256(
        (salt + password).encode("utf-8")
    ).hexdigest()

    return f"{salt}${password_hash}"


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()

    except Exception as error:

        st.error(
            f"Users could not be loaded from PostgreSQL: {error}"
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )

        return cursor.fetchone()

    except Exception as error:

        st.error(
            f"Profile could not be loaded: {error}"
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    name,
    email,
    password,
    confirm_password,
):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Please enter your name."

    if not email:
        return False, "Please enter your Mail ID."

    if not password:
        return False, "Please enter a password."

    if len(password) < 6:
        return (
            False,
            "Password must contain at least 6 characters.",
        )

    if password != confirm_password:
        return False, "Passwords do not match."

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        if cursor.fetchone():

            return (
                False,
                "An account with this Mail ID already exists.",
            )

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            RETURNING id
            """,
            (
                name,
                email,
                password_hash,
            ),
        )

        cursor.fetchone()

        connection.commit()

        return (
            True,
            "Account created successfully.",
        )

    except Exception as error:

        if connection:
            connection.rollback()

        return (
            False,
            f"Could not create account: {error}",
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# UPDATE USER
# ============================================================

def update_user(
    user_id,
    name,
    email,
    password,
):

    name = name.strip()
    email = email.strip().lower()
    password = password.strip()

    if not name:
        return False, "Please enter your name."

    if not email:
        return False, "Please enter your Mail ID."

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # ----------------------------------------------------
        # CHECK DUPLICATE EMAIL
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            AND id != %s
            """,
            (
                email,
                user_id,
            ),
        )

        if cursor.fetchone():

            return (
                False,
                "This Mail ID is already in use.",
            )

        # ----------------------------------------------------
        # UPDATE WITH PASSWORD
        # ----------------------------------------------------

        if password:

            if len(password) < 6:

                return (
                    False,
                    "Password must contain at least 6 characters.",
                )

            password_hash = hash_password(password)

            cursor.execute(
                """
                UPDATE users
                SET
                    name = %s,
                    email = %s,
                    password_hash = %s
                WHERE id = %s
                """,
                (
                    name,
                    email,
                    password_hash,
                    user_id,
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
                WHERE id = %s
                """,
                (
                    name,
                    email,
                    user_id,
                ),
            )

        if cursor.rowcount == 0:

            connection.rollback()

            return (
                False,
                "Account could not be updated.",
            )

        connection.commit()

        return (
            True,
            "Profile updated successfully.",
        )

    except Exception as error:

        if connection:
            connection.rollback()

        return (
            False,
            f"Could not update profile: {error}",
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# DELETE USER
# ============================================================

def delete_user(user_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            (user_id,),
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

/* =========================================================
   MAIN APPLICATION
   ========================================================= */

.stApp {
    background: #030912;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #071426;
}

.brand-title {
    font-size: 25px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
}

.brand-subtitle {
    color: #6f9ed3;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 45px;
}


/* =========================================================
   PAGE HEADER
   ========================================================= */

.page-title {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 4px;
}

.page-subtitle {
    color: #7898bc;
    font-size: 14px;
    margin-bottom: 22px;
}


/* =========================================================
   ACCOUNTS CARD
   ========================================================= */

.accounts-card {
    background: #081525;
    border: 1px solid #1b3551;
    border-radius: 10px;
    padding: 17px 20px;
    margin-top: 12px;
    margin-bottom: 14px;
}

.accounts-title {
    color: white;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 4px;
}

.accounts-description {
    color: #6f96bf;
    font-size: 13px;
}


/* =========================================================
   TABLE
   ========================================================= */

.table-header {
    background: #086da9;
    color: white;
    font-size: 14px;
    font-weight: 700;
    padding: 13px 12px;
    min-height: 46px;
    display: flex;
    align-items: center;
}

.table-header-left {
    border-radius: 6px 0 0 0;
}

.table-header-right {
    border-radius: 0 6px 0 0;
}

.account-cell {
    background: #081525;
    border-bottom: 1px solid #1b3551;
    min-height: 55px;
    padding: 8px 12px;
    display: flex;
    align-items: center;
}

.account-name {
    color: #ffffff;
    font-size: 14px;
    font-weight: 650;
}

.account-email {
    color: #79a9d9;
    font-size: 14px;
}


/* =========================================================
   PROFILE CARD
   ========================================================= */

.profile-card {
    background: #081525;
    border: 1px solid #1b3551;
    border-radius: 12px;
    padding: 22px 24px;
    margin-top: 25px;
    margin-bottom: 18px;
}

.profile-card-title {
    color: white;
    font-size: 22px;
    font-weight: 750;
    margin-bottom: 5px;
}

.profile-card-subtitle {
    color: #7198c0;
    font-size: 13px;
}

.profile-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: #162b48;
    border: 2px solid #31547d;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    margin-bottom: 12px;
}

.profile-name {
    color: white;
    font-size: 24px;
    font-weight: 750;
}

.profile-email {
    color: #6f9ed3;
    font-size: 14px;
    margin-top: 4px;
}


/* =========================================================
   INFORMATION
   ========================================================= */

.info-box {
    background: #071321;
    border: 1px solid #1b3551;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 12px;
}

.info-label {
    color: #658bb4;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .7px;
    margin-bottom: 5px;
}

.info-value {
    color: white;
    font-size: 15px;
    font-weight: 650;
}


/* =========================================================
   CREATE ACCOUNT
   ========================================================= */

.create-card {
    background: #081525;
    border: 1px solid #294564;
    border-radius: 12px;
    padding: 20px 22px;
    margin-top: 25px;
    margin-bottom: 18px;
}

.create-title {
    color: white;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 5px;
}

.create-description {
    color: #7198c0;
    font-size: 13px;
}


/* =========================================================
   FORM INPUTS
   ========================================================= */

div[data-baseweb="input"] {
    background: #111a2a;
    border: 1px solid #263b55;
    border-radius: 7px;
}

div[data-baseweb="input"]:focus-within {
    border-color: #1688d1;
}

div[data-baseweb="input"] input {
    color: white;
}

label {
    color: #d9e6f5 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button {
    border-radius: 7px;
    min-height: 40px;
    font-weight: 600;
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
        '<div class="brand-title">&lt;/&gt; CodePractice</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">Learn. Practice. Grow.</div>',
        unsafe_allow_html=True,
    )

    # Dashboard Back Button
    if st.button(
        "←  Dashboard",
        key="settings_dashboard_back",
        use_container_width=True,
    ):
        st.switch_page(st.session_state["dashboard_page"])

    # Navigation is controlled by app.py.
    # Do NOT add st.page_link("app.py") here.

    st.markdown(
        """
<hr style="
    border:0;
    border-top:1px solid #203753;
    margin:35px 0;
">
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="
    color:#4ea3ff;
    font-size:16px;
    font-weight:700;
    padding:8px 0;
">
    👤 Profile / Accounts
</div>
""",
        unsafe_allow_html=True,
    )
# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="page-title">👤 Profile / Account Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="page-subtitle">
    Manage CodePractice AI profiles and accounts.
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CREATE ACCOUNT BUTTON
# ============================================================

empty_col, create_col = st.columns([5, 1.7])

with create_col:

    if st.button(
        "＋ Create Account",
        type="primary",
        use_container_width=True,
        key="create_top",
    ):

        st.session_state["show_create"] = True
        st.session_state["selected_user_id"] = None
        st.session_state["edit_user_id"] = None

        st.rerun()


# ============================================================
# ACCOUNTS CARD
# ============================================================

st.markdown(
    """
<div class="accounts-card">
    <div class="accounts-title">Accounts</div>
    <div class="accounts-description">
        View and manage CodePractice AI accounts.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD USERS
# ============================================================

users = get_all_users()


# ============================================================
# TABLE HEADER
# ============================================================

(
    header_name,
    header_email,
    header_view,
    header_edit,
    header_delete,
) = st.columns(
    [2.4, 3.2, 0.8, 0.8, 0.8]
)


with header_name:

    st.markdown(
        """
<div class="table-header table-header-left">
    Name
</div>
""",
        unsafe_allow_html=True,
    )


with header_email:

    st.markdown(
        """
<div class="table-header">
    Mail ID
</div>
""",
        unsafe_allow_html=True,
    )


with header_view:

    st.markdown(
        """
<div class="table-header">
    View
</div>
""",
        unsafe_allow_html=True,
    )


with header_edit:

    st.markdown(
        """
<div class="table-header">
    Edit
</div>
""",
        unsafe_allow_html=True,
    )


with header_delete:

    st.markdown(
        """
<div class="table-header table-header-right">
    Delete
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# ACCOUNT ROWS
# ============================================================

if not users:

    st.info(
        "No accounts found. Click 'Create Account' to add an account."
    )

else:

    for account in users:

        user_id = account[0]
        name = account[1] or ""
        email = account[2] or ""

        safe_name = html.escape(str(name))
        safe_email = html.escape(str(email))

        # ====================================================
        # ROW COLUMNS
        # ====================================================

        (
            col_name,
            col_email,
            col_view,
            col_edit,
            col_delete,
        ) = st.columns(
            [2.4, 3.2, 0.8, 0.8, 0.8]
        )

        # ====================================================
        # NAME
        # ====================================================

        with col_name:

            st.markdown(
                f"""
<div class="account-cell">
    <div class="account-name">
        {safe_name}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ====================================================
        # MAIL ID
        # ====================================================

        with col_email:

            st.markdown(
                f"""
<div class="account-cell">
    <div class="account-email">
        {safe_email}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ====================================================
        # VIEW
        # ====================================================

        with col_view:

            if st.button(
                "👁",
                key=f"view_{user_id}",
                help="View profile",
                use_container_width=True,
            ):

                st.session_state["selected_user_id"] = user_id
                st.session_state["edit_user_id"] = None
                st.session_state["show_create"] = False

                st.rerun()

        # ====================================================
        # EDIT
        # ====================================================

        with col_edit:

            if st.button(
                "✏️",
                key=f"edit_{user_id}",
                help="Edit profile",
                use_container_width=True,
            ):

                st.session_state["edit_user_id"] = user_id
                st.session_state["selected_user_id"] = None
                st.session_state["show_create"] = False

                st.rerun()

        # ====================================================
        # DELETE
        # ====================================================

        with col_delete:

            if st.button(
                "🗑️",
                key=f"delete_{user_id}",
                help="Delete account",
                use_container_width=True,
            ):

                deleted = delete_user(user_id)

                if deleted:

                    st.session_state["selected_user_id"] = None
                    st.session_state["edit_user_id"] = None
                    st.session_state["show_create"] = False

                    st.rerun()

                else:

                    st.error(
                        "Account could not be deleted."
                    )

# ============================================================
# VIEW PROFILE
# ============================================================

selected_user_id = st.session_state.get("selected_user_id")

if selected_user_id:

    selected_user = get_user_by_id(selected_user_id)

    if selected_user:

        user_id = selected_user[0]
        name = selected_user[1] or ""
        email = selected_user[2] or ""

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        st.markdown("---")

        profile_title_col, close_col = st.columns([5, 1])

        with profile_title_col:

            st.subheader("👤 Profile Details")

            st.caption(
                "Account information"
            )

        with close_col:

            if st.button(
                "✕ Close",
                use_container_width=True,
                key="close_profile",
            ):

                st.session_state["selected_user_id"] = None

                st.rerun()


        # ----------------------------------------------------
        # PROFILE SUMMARY
        # ----------------------------------------------------

        avatar_col, profile_col = st.columns([1, 5])

        with avatar_col:

            st.markdown(
                """
<div style="
    width:72px;
    height:72px;
    border-radius:50%;
    background:#162b48;
    border:2px solid #31547d;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:32px;
    margin-top:8px;
">
    👤
</div>
""",
                unsafe_allow_html=True,
            )

        with profile_col:

            st.markdown(
                f"### {html.escape(str(name))}"
            )

            st.markdown(
                f"""
<span style="
    color:#6fa6dc;
    font-size:14px;
">
    {html.escape(str(email))}
</span>
""",
                unsafe_allow_html=True,
            )


        # ----------------------------------------------------
        # ACCOUNT INFORMATION
        # ----------------------------------------------------

        st.markdown("")

        name_col, email_col = st.columns(2)

        with name_col:

            st.markdown("**Name**")

            st.markdown(
                f"""
<div style="
    background:#111a2a;
    border:1px solid #263b55;
    border-radius:7px;
    padding:12px 14px;
    color:#d9e6f5;
    min-height:20px;
">
    {html.escape(str(name))}
</div>
""",
                unsafe_allow_html=True,
            )

        with email_col:

            st.markdown("**Mail ID**")

            st.markdown(
                f"""
<div style="
    background:#111a2a;
    border:1px solid #263b55;
    border-radius:7px;
    padding:12px 14px;
    color:#6fa6dc;
    min-height:20px;
">
    {html.escape(str(email))}
</div>
""",
                unsafe_allow_html=True,
            )


        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        st.markdown("")

        _, edit_col, _ = st.columns([3, 1.4, 3])

        with edit_col:

            if st.button(
                "✏️ Edit Profile",
                use_container_width=True,
                key=f"view_edit_{user_id}",
            ):

                st.session_state["edit_user_id"] = user_id
                st.session_state["selected_user_id"] = None
                st.session_state["show_create"] = False

                st.rerun()


# ============================================================
# EDIT PROFILE
# ============================================================

edit_user_id = st.session_state.get("edit_user_id")

if edit_user_id:

    edit_user = get_user_by_id(edit_user_id)

    if edit_user:

        user_id = edit_user[0]
        current_name = edit_user[1] or ""
        current_email = edit_user[2] or ""

        st.markdown("---")

        title_col, close_col = st.columns([5, 1])

        with title_col:
            st.subheader("✏️ Edit Profile")
            st.caption("Update your account information.")

        with close_col:

            if st.button(
                "✕ Close",
                use_container_width=True,
                key=f"close_edit_{user_id}",
            ):
                st.session_state["edit_user_id"] = None
                st.rerun()

        # Profile summary
        avatar_col, profile_col = st.columns([1, 5])

        with avatar_col:

            st.markdown(
                """
<div style="
    width:68px;
    height:68px;
    border-radius:50%;
    background:#162b48;
    border:2px solid #31547d;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
">
    👤
</div>
""",
                unsafe_allow_html=True,
            )

        with profile_col:

            st.markdown(
                f"### {html.escape(str(current_name))}"
            )

            st.caption(
                html.escape(str(current_email))
            )

        st.markdown("")

        # Name and email
        name_col, email_col = st.columns(2)

        with name_col:

            edit_name = st.text_input(
                "Name",
                value=current_name,
                placeholder="Enter full name",
                key=f"edit_name_{user_id}",
            )

        with email_col:

            edit_email = st.text_input(
                "Mail ID",
                value=current_email,
                placeholder="Enter email address",
                key=f"edit_email_{user_id}",
            )

        # Password
        edit_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Leave empty to keep current password",
            help="Enter a password only if you want to change it.",
            key=f"edit_password_{user_id}",
        )

        st.markdown("")

        # Buttons
        empty_col, save_col, cancel_col = st.columns(
            [4.5, 1.4, 1.0]
        )

        with save_col:

            if st.button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True,
                key=f"save_changes_{user_id}",
            ):

                success, message = update_user(
                    user_id,
                    edit_name,
                    edit_email,
                    edit_password,
                )

                if success:

                    st.session_state["edit_user_id"] = None

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

        with cancel_col:

            if st.button(
                "Cancel",
                use_container_width=True,
                key=f"cancel_edit_{user_id}",
            ):

                st.session_state["edit_user_id"] = None
                st.rerun()                
                
# ============================================================
# CREATE NEW ACCOUNT
# ============================================================

if st.session_state.get("show_create", False):

    st.markdown("---")

    st.subheader("＋ Create New Account")

    st.caption(
        "Add a new CodePractice AI account."
    )

    st.markdown("")

    # --------------------------------------------------------
    # FORM ROW 1
    # --------------------------------------------------------

    name_col, email_col = st.columns(2)

    with name_col:

        new_name = st.text_input(
            "Name",
            placeholder="Enter full name",
            key="new_account_name",
        )

    with email_col:

        new_email = st.text_input(
            "Mail ID",
            placeholder="Enter email address",
            key="new_account_email",
        )

    # --------------------------------------------------------
    # FORM ROW 2
    # --------------------------------------------------------

    password_col, confirm_col = st.columns(2)

    with password_col:

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters",
            key="new_account_password",
        )

    with confirm_col:

        new_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Enter password again",
            key="new_account_confirm",
        )

    st.markdown("")

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    empty_col, create_col, cancel_col = st.columns(
        [5, 1.4, 1]
    )

    with create_col:

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True,
            key="create_account_submit",
        ):

            success, message = create_user(
                new_name,
                new_email,
                new_password,
                new_confirm,
            )

            if success:

                st.session_state["show_create"] = False

                for key in [
                    "new_account_name",
                    "new_account_email",
                    "new_account_password",
                    "new_account_confirm",
                ]:
                    st.session_state.pop(
                        key,
                        None,
                    )

                st.success(message)

                st.rerun()

            else:

                st.error(message)

    with cancel_col:

        if st.button(
            "Cancel",
            use_container_width=True,
            key="cancel_create",
        ):

            st.session_state["show_create"] = False

            for key in [
                "new_account_name",
                "new_account_email",
                "new_account_password",
                "new_account_confirm",
            ]:
                st.session_state.pop(
                    key,
                    None,
                )

            st.rerun()
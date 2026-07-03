function NavBar() {
    return (
        <nav>
            <button
                onClick={() => {

                    localStorage.removeItem("token");
                    window.location.reload();
                }}
            >
                Logout
            </button>
        </nav>
    )
}

export default NavBar
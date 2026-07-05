type Props = {
    currentPage: string;
    onNavigate: (page: string) => void;
}

function NavBar({ currentPage, onNavigate }: Props) {
    return (
        <nav>
            <button onClick={() => onNavigate("home")} disabled={currentPage === "home"}>Home</button>
            <button onClick={() => onNavigate("chat")} disabled={currentPage === "chat"}>Chat</button>
            <button onClick={() => onNavigate("resume")} disabled={currentPage === "resume"}>Resume</button>
            <button onClick={() => onNavigate("jobmatch")} disabled={currentPage === "jobmatch"}>Job Match</button>
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
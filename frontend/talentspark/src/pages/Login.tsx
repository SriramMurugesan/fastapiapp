import {useState} from "react";
import {login} from "../Services/AuthService";

type Props = {
    onLogin: (token: string) => void;
    onSwitchToRegister: () => void;
}

function Login({onLogin, onSwitchToRegister}: Props){
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await login({email,password});
            onLogin(response.access_token);
        } catch (error) {
            console.error("Error during login:", error);
            alert("Login failed");
        }
    }   
    return(
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Email" required/>
            <br />
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password" required/>
            <br />
            <button type="submit">Login</button>
            <p>Don't have an account? <button type="button" onClick={onSwitchToRegister}>Register</button></p>
        </form>
    )
}

export default Login;